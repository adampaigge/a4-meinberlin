from xml.etree import ElementTree
import zeep

from allauth.socialaccount import providers
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthError
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .provider import ServiceKontoProvider

SERVICE_KONTO_GET_USER_DATA_SUCCESS = 1


class ServiceKontoApiError(Exception):
    def __init__(self, exception=None, error=AuthError.UNKNOWN):
        self.exception = exception
        self.error = error


def login(request):
    SocialLogin.stash_state(request)
    return HttpResponseRedirect(settings.SERVICE_KONTO_LOGIN_URL)


@csrf_exempt
def callback(request):
    token = request.GET.get('Token', '')
    if not token:
        return render_authentication_error(
            request, ServiceKontoProvider.id, error=AuthError.UNKNOWN)

    try:
        login = complete_login(request, token)
    except ServiceKontoApiError as e:
        return render_authentication_error(
            request, ServiceKontoProvider.id,
            exception=e.exception, error=e.error)
    except ValueError as e:
        return render_authentication_error(
            request, ServiceKontoProvider.id,
            exception=e, error=AuthError.UNKNOWN)

    ret = complete_social_login(request, login)
    if not ret:
        ret = render_authentication_error(request, ServiceKontoProvider.id)

    return ret


def complete_login(request, token):
    user_data_xml = _get_service_konto_user_data_xml(request, token)
    user_data = _parse_user_data_xml(user_data_xml)

    provider = providers.registry.by_id(ServiceKontoProvider.id, request)
    login = provider.sociallogin_from_response(request, user_data)
    login.state = SocialLogin.unstash_state(request)
    return login


def _get_service_konto_user_data_xml(request, token):
    service_konto = zeep.Client(settings.SERVICE_KONTO_API_URL)

    result = service_konto.service.GetUserData(token)
    if not result.GetUserDataResult == SERVICE_KONTO_GET_USER_DATA_SUCCESS:
        raise ServiceKontoApiError(error=AuthError.DENIED)

    return result.strXMLUserData


def _parse_user_data_xml(xml: str) -> dict:
    root = ElementTree.fromstring(xml)

    hhgw = root.find('./HHGW')
    if hhgw is None:
        raise ValueError('Invalid data received.')

    user_data = dict()
    required_attributes = ['USERID', 'FIRSTNAME', 'LASTNAME', 'EMAIL']
    for attribute in required_attributes:
        user_data[attribute.lower()] = hhgw.get(attribute)

    if not _is_user_data_valid(user_data):
        raise ValueError('Invalid user data received.')
    return user_data


def _is_user_data_valid(user_data: dict) -> bool:
    is_valid = (user_data.get('userid') and
                user_data.get('firstname') and
                user_data.get('lastname') and
                user_data.get('email'))
    return is_valid