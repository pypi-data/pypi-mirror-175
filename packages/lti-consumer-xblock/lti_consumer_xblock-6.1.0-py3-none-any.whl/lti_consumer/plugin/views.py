"""
LTI consumer plugin passthrough views
"""
import logging
import urllib

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError
from django.http import JsonResponse, Http404
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import UsageKey
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from lti_consumer.api import get_lti_pii_sharing_state_for_course, validate_lti_1p3_launch_data
from lti_consumer.exceptions import LtiError
from lti_consumer.models import (
    LtiConfiguration,
    LtiAgsLineItem,
    LtiDlContentItem,
)

from lti_consumer.lti_1p3.exceptions import (
    Lti1p3Exception,
    LtiDeepLinkingContentTypeNotSupported,
    UnsupportedGrantType,
    MalformedJwtToken,
    MissingRequiredClaim,
    NoSuitableKeys,
    TokenSignatureExpired,
    UnknownClientId,
)
from lti_consumer.lti_1p3.extensions.rest_framework.constants import LTI_DL_CONTENT_TYPE_SERIALIZER_MAP
from lti_consumer.lti_1p3.extensions.rest_framework.serializers import (
    LtiAgsLineItemSerializer,
    LtiAgsScoreSerializer,
    LtiAgsResultSerializer,
    LtiNrpsContextMembershipBasicSerializer,
    LtiNrpsContextMembershipPIISerializer,
)
from lti_consumer.lti_1p3.extensions.rest_framework.permissions import (
    LtiAgsPermissions,
    LtiNrpsContextMembershipsPermissions,
)
from lti_consumer.lti_1p3.extensions.rest_framework.authentication import Lti1p3ApiAuthentication
from lti_consumer.lti_1p3.extensions.rest_framework.renderers import (
    LineItemsRenderer,
    LineItemRenderer,
    LineItemScoreRenderer,
    LineItemResultsRenderer,
    MembershipResultRenderer,
)
from lti_consumer.lti_1p3.extensions.rest_framework.parsers import (
    LineItemParser,
    LineItemScoreParser,
)
from lti_consumer.lti_1p3.extensions.rest_framework.utils import IgnoreContentNegotiation
from lti_consumer.plugin import compat
from lti_consumer.utils import _, get_lti_1p3_context_types_claim, get_data_from_cache
from lti_consumer.track import track_event


log = logging.getLogger(__name__)


def has_block_access(user, block, course_key):
    """
    Checks if a user has access to given xblock.

    ``has_access`` doesn't checks for course enrollment. On the otherhand, ``get_course_with_access``
    only checks for the course itself. There is no way to check access for specific xblock. This function
    has been created to perform a combination of check for both enrollment and access for specific xblock.

    Args:
        user: User Object
        block: xblock Object to check permission for
        course_key: A course_key specifying which course run this access is for.

    Returns:
        bool: True if user has access, False otherwise.
    """
    # Get the course
    course = compat.get_course_by_id(course_key)

    # Check if user is authenticated & enrolled
    course_access = compat.user_course_access(course, user, 'load', check_if_enrolled=True, check_if_authenticated=True)

    # Check if user has access to xblock
    block_access = compat.user_has_access(user, 'load', block, course_key)

    # Return True if the user has access to xblock and is enrolled in that specific course.
    return course_access and block_access


@require_http_methods(["GET"])
def public_keyset_endpoint(request, usage_id=None, lti_config_id=None):
    """
    Gate endpoint to fetch public keysets from a problem

    This is basically a passthrough function that uses the
    OIDC response parameter `login_hint` to locate the block
    and run the proper handler.
    """
    try:
        if usage_id:
            lti_config = LtiConfiguration.objects.get(location=UsageKey.from_string(usage_id))
        elif lti_config_id:
            lti_config = LtiConfiguration.objects.get(config_id=lti_config_id)

        if lti_config.version != lti_config.LTI_1P3:
            raise LtiError(
                "LTI Error: LTI 1.1 blocks do not have a public keyset endpoint."
            )

        # Retrieve block's Public JWK
        # The underlying method will generate a new Private-Public Pair if one does
        # not exist, and retrieve the values.
        response = JsonResponse(lti_config.lti_1p3_public_jwk)
        response['Content-Disposition'] = 'attachment; filename=keyset.json'
        return response
    except (LtiError, InvalidKeyError, ObjectDoesNotExist) as exc:
        log.info(
            "Error while retrieving keyset for usage_id (%r) or lit_config_id (%s): %s",
            usage_id,
            lti_config_id,
            exc,
            exc_info=True,
        )
        raise Http404 from exc


@require_http_methods(["GET", "POST"])
@xframe_options_exempt
def launch_gate_endpoint(request, suffix=None):  # pylint: disable=unused-argument
    """
    Gate endpoint that triggers LTI launch endpoint XBlock handler

    This uses the config_id key of the "lti_message_hint" query parameter
    to identify the LtiConfiguration and its consumer to generate the
    LTI 1.3 Launch Form.
    """
    # pylint: disable=too-many-statements
    request_params = request.GET if request.method == 'GET' else request.POST

    lti_message_hint = request_params.get('lti_message_hint')
    if not lti_message_hint:
        log.info('The lti_message_hint query param in the request is missing or empty.')
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    login_hint = request_params.get('login_hint')
    if not login_hint:
        log.info('The login_hint query param in the request is missing or empty.')
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    launch_data = get_data_from_cache(lti_message_hint)
    if not launch_data:
        log.warning(f'There was a cache miss during an LTI 1.3 launch when using the cache_key {lti_message_hint}.')
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    # Validate the Lti1p3LaunchData.
    is_valid, validation_messages = validate_lti_1p3_launch_data(launch_data)
    if not is_valid:
        validation_message = " ".join(validation_messages)
        log.error(
            f"The Lti1p3LaunchData is not valid. {validation_message}"
        )
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    config_id = launch_data.config_id
    try:
        lti_config = LtiConfiguration.objects.get(
            config_id=config_id
        )
    except (LtiConfiguration.DoesNotExist, ValidationError) as exc:
        log.error("Invalid config_id '%s' for LTI 1.3 Launch callback", config_id)
        raise Http404 from exc

    if lti_config.version != LtiConfiguration.LTI_1P3:
        log.error("The LTI Version of configuration %s is not LTI 1.3", lti_config)
        return render(request, 'html/lti_launch_error.html', status=HTTP_404_NOT_FOUND)

    context = {}

    try:
        lti_consumer = lti_config.get_lti_consumer()

        # Set sub and roles claims.
        user_id = launch_data.user_id
        user_role = launch_data.user_role
        lti_consumer.set_user_data(
            user_id=user_id,
            role=user_role,
        )

        # Set resource_link claim.
        lti_consumer.set_resource_link_claim(launch_data.resource_link_id)

        # Set launch_presentation claim.
        launch_presentation_target = launch_data.launch_presentation_document_target
        if launch_presentation_target:
            lti_consumer.set_launch_presentation_claim(launch_presentation_target)

        # Set optional context claim, if supplied.
        context_type = launch_data.context_type
        context_types_claim = None

        if context_type:
            try:
                context_types_claim = get_lti_1p3_context_types_claim(context_type)
            except ValueError:
                log.error(
                    "The context_type key %s in the launch data does not represent a valid context_type.",
                    context_type
                )
                return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

        lti_consumer.set_context_claim(
            launch_data.context_id,
            context_types_claim,
            launch_data.context_title,
            launch_data.context_label,
        )

        # Retrieve preflight response.
        preflight_response = request_params.dict()

        # Set LTI Launch URL.
        context.update({'launch_url': preflight_response.get("redirect_uri")})

        # Modify LTI Launch URL depending on launch type.
        # Deep Linking Launch - Configuration flow launched by
        # course creators to set up content.
        deep_linking_content_item_id = launch_data.deep_linking_content_item_id

        if lti_consumer.dl and launch_data.message_type == 'LtiDeepLinkingRequest':
            # Check if the user is staff before LTI doing deep linking launch.
            # If not, raise exception and display error page
            if user_role not in ['instructor', 'staff']:
                raise AssertionError('Deep Linking can only be performed by instructors and staff.')
            # Set deep linking launch
            context.update({'launch_url': lti_consumer.dl.deep_linking_launch_url})

        # Deep Linking ltiResourceLink content presentation
        # When content type is `ltiResourceLink`, the tool will be launched with
        # different parameters, set by instructors when running the DL configuration flow.
        elif lti_consumer.dl and deep_linking_content_item_id:
            # Retrieve Deep Linking parameters using the  parameter.
            content_item = lti_config.ltidlcontentitem_set.get(pk=deep_linking_content_item_id)
            # Only filter DL content item from content item set in the same LTI configuration.
            # This avoids a malicious user to input a random LTI id and perform LTI DL
            # content launches outside the scope of its configuration.
            dl_params = content_item.attributes

            # Modify LTI launch and set ltiResourceLink parameters
            lti_consumer.set_dl_content_launch_parameters(
                url=dl_params.get('url'),
                custom=dl_params.get('custom')
            )

        # Update context with LTI launch parameters
        context.update({
            "preflight_response": preflight_response,
            "launch_request": lti_consumer.generate_launch_request(
                preflight_response=preflight_response,
            )
        })
        event = {
            'lti_version': lti_config.version,
            'user_roles': user_role,
            'launch_url': context['launch_url']
        }
        track_event('xblock.launch_request', event)

        return render(request, 'html/lti_1p3_launch.html', context)
    except Lti1p3Exception as exc:
        resource_link_id = launch_data.resource_link_id
        log.warning(
            "Error preparing LTI 1.3 launch for resource with resource_link_id %r: %s",
            resource_link_id,
            exc,
            exc_info=True
        )
        return render(request, 'html/lti_launch_error.html', context, status=HTTP_400_BAD_REQUEST)
    except AssertionError as exc:
        resource_link_id = launch_data.resource_link_id
        log.warning(
            "Permission on resource with resource_link_id %r denied for user %r: %s",
            resource_link_id,
            user_id,
            exc,
            exc_info=True
        )
        return render(request, 'html/lti_1p3_permission_error.html', context, status=HTTP_403_FORBIDDEN)


@csrf_exempt
@require_http_methods(["POST"])
def access_token_endpoint(request, lti_config_id=None, usage_id=None):
    """
    Gate endpoint to enable tools to retrieve access tokens for the LTI 1.3 tool.

    This endpoint is only valid when a LTI 1.3 tool is being used.

    Arguments:
        lti_config_id (UUID): config_id of the LtiConfiguration
        usage_id (UsageKey): location of the Block

    Returns:
        JsonResponse or Http404

    References:
        Sucess: https://tools.ietf.org/html/rfc6749#section-4.4.3
        Failure: https://tools.ietf.org/html/rfc6749#section-5.2
    """

    try:
        if lti_config_id:
            lti_config = LtiConfiguration.objects.get(config_id=lti_config_id)
        else:
            usage_key = UsageKey.from_string(usage_id)
            lti_config = LtiConfiguration.objects.get(location=usage_key)
    except LtiConfiguration.DoesNotExist as exc:
        log.warning("Error getting the LTI configuration with id %r: %s", lti_config_id, exc, exc_info=True)
        raise Http404 from exc

    if lti_config.version != lti_config.LTI_1P3:
        return JsonResponse({"error": "invalid_lti_version"}, status=HTTP_404_NOT_FOUND)

    lti_consumer = lti_config.get_lti_consumer()
    try:
        token = lti_consumer.access_token(
            dict(urllib.parse.parse_qsl(
                request.body.decode('utf-8'),
                keep_blank_values=True
            ))
        )
        return JsonResponse(token)

    # Handle errors and return a proper response
    except MissingRequiredClaim:
        # Missing request attibutes
        return JsonResponse({"error": "invalid_request"}, status=HTTP_400_BAD_REQUEST)
    except (MalformedJwtToken, TokenSignatureExpired):
        # Triggered when a invalid grant token is used
        return JsonResponse({"error": "invalid_grant"}, status=HTTP_400_BAD_REQUEST)
    except (NoSuitableKeys, UnknownClientId):
        # Client ID is not registered in the block or
        # isn't possible to validate token using available keys.
        return JsonResponse({"error": "invalid_client"}, status=HTTP_400_BAD_REQUEST)
    except UnsupportedGrantType:
        return JsonResponse({"error": "unsupported_grant_type"}, status=HTTP_400_BAD_REQUEST)


# Post from external tool that doesn't
# have access to CSRF tokens
@csrf_exempt
# This URL should work inside an iframe
@xframe_options_sameorigin
# Post only, as required by LTI-DL Specification
@require_http_methods(["POST"])
def deep_linking_response_endpoint(request, lti_config_id=None):
    """
    Deep Linking response endpoint where tool can send back Deep Linking
    content selected by instructions in the tool's UI.

    For this feature to work, the LMS session cookies need to be Secure
    and have the `SameSite` attribute set to `None`, otherwise we won't
    be able to check user permissions.
    """
    try:
        # Retrieve LTI configuration
        lti_config = LtiConfiguration.objects.get(id=lti_config_id)

        # Get LTI consumer
        lti_consumer = lti_config.get_lti_consumer()

        # Validate Deep Linking return message and return decoded message
        content_items = lti_consumer.check_and_decode_deep_linking_token(
            request.POST.get("JWT")
        )

        # Check if the user has sufficient permissions to
        # save LTI Deep Linking content through the student.auth API.
        course_key = lti_config.location.course_key
        if not compat.user_has_studio_write_access(request.user, course_key):
            raise PermissionDenied()

        # On a transaction, clear older DeepLinking selections, then
        # verify and save each content item passed from the tool.
        with transaction.atomic():
            # Erase older deep linking selection
            LtiDlContentItem.objects.filter(lti_configuration=lti_config).delete()

            for content_item in content_items:
                content_type = content_item.get('type')

                # Retrieve serializer (or raise)
                # pylint: disable=consider-iterating-dictionary
                if content_type not in LTI_DL_CONTENT_TYPE_SERIALIZER_MAP.keys():
                    raise LtiDeepLinkingContentTypeNotSupported()
                serializer_cls = LTI_DL_CONTENT_TYPE_SERIALIZER_MAP[content_type]

                # Validate content item data
                serializer = serializer_cls(data=content_item)
                serializer.is_valid(raise_exception=True)

                # Save content item
                LtiDlContentItem.objects.create(
                    lti_configuration=lti_config,
                    content_type=content_type,
                    attributes=serializer.validated_data,
                )

        # Display sucess page to indicate that LTI DL Content was
        # saved successfully and auto-close after a few seconds.
        return render(request, 'html/lti-dl/dl_response_saved.html')

    # If LtiConfiguration doesn't exist, error with 404 status.
    except LtiConfiguration.DoesNotExist as exc:
        log.info("LtiConfiguration %r does not exist: %s", lti_config_id, exc)
        raise Http404 from exc
    # If the deep linking content type is not supported
    except LtiDeepLinkingContentTypeNotSupported as exc:
        log.info("One of the selected LTI Content Types is not supported: %s", exc)
        return render(
            request,
            'html/lti-dl/dl_response_error.html',
            {"error": _("The selected content type is not supported by Open edX.")},
            status=400
        )
    # Bad JWT message, invalid token, or any other message validation issues
    except (Lti1p3Exception, PermissionDenied) as exc:
        log.warning(
            "Permission on LTI Config %r denied for user %r: %s",
            lti_config,
            request.user,
            exc,
        )
        return render(
            request,
            'html/lti-dl/dl_response_error.html',
            {
                "error": _("You don't have access to save LTI Content Items."),
                "explanation": _("Please check that you have course staff permissions "
                                 "and double check this block's LTI settings."),
            },
            status=403
        )


@require_http_methods(['GET'])
@xframe_options_sameorigin
def deep_linking_content_endpoint(request, lti_config_id):
    """
    Deep Linking endpoint for rendering Deep Linking Content Items.
    """
    launch_data_key = request.GET.get("launch_data_key")
    if not launch_data_key:
        log.info('The launch_data_key query param in the request is missing or empty.')
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    launch_data = get_data_from_cache(launch_data_key)
    if not launch_data:
        log.warning(f'There was a cache miss during an LTI 1.3 launch when using the cache_key {launch_data_key}.')
        return render(request, 'html/lti_launch_error.html', status=HTTP_400_BAD_REQUEST)

    try:
        # Get LTI Configuration
        lti_config = LtiConfiguration.objects.get(id=lti_config_id)
    except LtiConfiguration.DoesNotExist as exc:
        log.info("LtiConfiguration %r does not exist: %s", lti_config_id, exc)
        raise Http404 from exc

    # check if user has proper access
    block = compat.load_block_as_user(lti_config.location)
    if not has_block_access(request.user, block, lti_config.location.course_key):
        log.warning(
            "Permission on LTI Config %r denied for user %r.",
            lti_config_id,
            request.user,
        )
        raise PermissionDenied

    # Get all LTI-DL contents
    content_items = LtiDlContentItem.objects.filter(lti_configuration=lti_config)

    # If no LTI-DL contents found for current configuration, throw 404 error
    if not content_items.exists():
        log.info("There's no Deep linking content for LTI configuration %s.", lti_config)
        raise Http404

    # Render LTI-DL contents
    return render(request, 'html/lti-dl/render_dl_content.html', {
        'content_items': content_items,
        'block': block,
        'launch_data': launch_data,
    })


class LtiAgsLineItemViewset(viewsets.ModelViewSet):
    """
    LineItem endpoint implementation from LTI Advantage.

    See full documentation at:
    https://www.imsglobal.org/spec/lti-ags/v2p0#line-item-service
    """
    serializer_class = LtiAgsLineItemSerializer
    pagination_class = None

    # Custom permission classes for LTI APIs
    authentication_classes = [Lti1p3ApiAuthentication]
    permission_classes = [LtiAgsPermissions]

    # Renderer/parser classes to accept LTI AGS content types
    renderer_classes = [
        LineItemsRenderer,
        LineItemRenderer,
    ]
    parser_classes = [LineItemParser]

    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'resource_link_id',
        'resource_id',
        'tag'
    ]

    def get_queryset(self):
        lti_configuration = self.request.lti_configuration

        # Return all LineItems related to the LTI configuration.
        # TODO:
        # Note that each configuration currently maps 1:1
        # to each resource link (block), and this filter needs
        # improved once we start reusing LTI configurations.
        return LtiAgsLineItem.objects.filter(
            lti_configuration=lti_configuration
        )

    def perform_create(self, serializer):
        lti_configuration = self.request.lti_configuration
        serializer.save(lti_configuration=lti_configuration)

    @action(
        detail=True,
        methods=['GET'],
        url_path='results/(?P<user_id>[^/.]+)?',
        renderer_classes=[LineItemResultsRenderer],
        content_negotiation_class=IgnoreContentNegotiation,
    )
    def results(self, request, user_id=None, **kwargs):
        """
        Return a Result list for an LtiAgsLineItem

        URL Parameters:
          * user_id (string): String external user id representation.

        Query Parameters:
          * limit (integer): The maximum number of records to return. Records are
                sorted with most recent timestamp first

        Returns:
          * An array of Result records, formatted by LtiAgsResultSerializer
                and returned with the media-type for LineItemResultsRenderer
        """
        line_item = self.get_object()
        scores = line_item.scores.filter(score_given__isnull=False).order_by('-timestamp')

        if user_id:
            scores = scores.filter(user_id=user_id)

        if request.query_params.get('limit'):
            scores = scores[:int(request.query_params.get('limit'))]

        serializer = LtiAgsResultSerializer(
            list(scores),
            context={'request': self.request},
            many=True,
        )

        return Response(serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        parser_classes=[LineItemScoreParser],
        renderer_classes=[LineItemScoreRenderer],
        content_negotiation_class=IgnoreContentNegotiation,
    )
    def scores(self, request, *args, **kwargs):
        """
        Create a Score record for an LtiAgsLineItem

        Data:
          * A JSON object capable of being serialized by LtiAgsScoreSerializer

        Returns:
          * An copy of the saved record, formatted by LtiAgsScoreSerializer
                and returned with the media-type for LineItemScoreRenderer
        """
        line_item = self.get_object()

        user_id = request.data.get('userId')

        # Using `filter` and `first` so that when a score does not exist,
        # `existing_score` is set to `None`. Using `get` will raise `DoesNotExist`
        existing_score = line_item.scores.filter(user_id=user_id).first()

        serializer = LtiAgsScoreSerializer(
            instance=existing_score,
            data=request.data,
            context={'request': self.request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(line_item=line_item)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LtiNrpsContextMembershipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    LTI NRPS Context Membership Service endpoint.

    See full documentation at:
    http://imsglobal.org/spec/lti-nrps/v2p0
    """

    # Custom permission classes for LTI APIs
    authentication_classes = [Lti1p3ApiAuthentication]
    permission_classes = [LtiNrpsContextMembershipsPermissions]

    # Renderer classes to accept LTI NRPS content types
    renderer_classes = [
        MembershipResultRenderer,
    ]

    def attach_external_user_ids(self, data):
        """
        Preprocess the output of `get_membership` method amd appends external ids to each user.
        """

        # batch get or create external ids for all users
        user_ids = data.keys()
        users = get_user_model().objects.prefetch_related('profile').filter(id__in=user_ids)

        # get external ids
        external_ids = compat.batch_get_or_create_externalids(users)

        for userid in user_ids:
            # append external ids to user
            data[userid]['external_id'] = external_ids[userid].external_user_id

    def get_serializer_class(self):
        """
        Overrides ModelViewSet's `get_serializer_class` method.
        Checks if PII fields can be exposed and returns appropiate serializer.
        """
        if get_lti_pii_sharing_state_for_course(self.request.lti_configuration.location.course_key):
            return LtiNrpsContextMembershipPIISerializer
        else:
            return LtiNrpsContextMembershipBasicSerializer

    def list(self, *args, **kwargs):
        """
        Overrides default list method of ModelViewSet. Calls LMS `get_course_members`
        API and returns result.
        """

        # get course key
        course_key = self.request.lti_configuration.location.course_key

        try:
            data = compat.get_course_members(course_key)
            self.attach_external_user_ids(data)

            # build correct format for the serializer
            result = {
                'id': self.request.build_absolute_uri(),
                'context': {
                    'id': course_key
                },
                'members': data.values(),
            }

            # Serialize and return data NRPS reponse.
            serializer = self.get_serializer_class()(result)
            return Response(serializer.data)

        except LtiError as ex:
            log.warning("LTI NRPS Error: %s", ex)
            return Response({
                "error": "above_response_limit",
                "explanation": "The number of retrieved users is bigger than the maximum allowed in the configuration.",
            }, status=HTTP_403_FORBIDDEN)
