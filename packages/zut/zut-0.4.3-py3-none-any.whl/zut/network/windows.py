from __future__ import annotations
import logging, win32com.client, win32inetcon, pywintypes
from unittest import TestCase
from . import _proxy_configuration

logger = logging.getLogger(__name__)

def create_winhttp_request(timeout=None):
    winhttp_req = win32com.client.Dispatch('WinHTTP.WinHTTPRequest.5.1')

    if timeout:
        winhttp_req.SetTimeouts(str(timeout*1000), str(timeout*1000), str(timeout*1000), str(timeout*1000))

    if _proxy_configuration.hostport:
        # See: https://docs.microsoft.com/en-us/windows/win32/winhttp/iwinhttprequest-setproxy
        # NOTE: no need to pass credentials, this is handled directly by Windows
        HTTPREQUEST_PROXYSETTING_DEFAULT   = 0
        HTTPREQUEST_PROXYSETTING_PRECONFIG = 0
        HTTPREQUEST_PROXYSETTING_DIRECT    = 1
        HTTPREQUEST_PROXYSETTING_PROXY     = 2
        winhttp_req.SetProxy(HTTPREQUEST_PROXYSETTING_PROXY, _proxy_configuration.hostport, _proxy_configuration.winhttp_exclusions)
        winhttp_req.SetAutoLogonPolicy(HTTPREQUEST_PROXYSETTING_DEFAULT)

    return winhttp_req


def test_winhttp_request(case: TestCase, url: str, expected_regex: str, label=None, timeout: int = 2) -> str:
    if label is None:
        label = url
    msg=f"{label} winhttp"

    winhttp_req = create_winhttp_request(timeout=timeout)
    winhttp_req.Open('GET', url, False)
    try:
        winhttp_req.Send()
        winhttp_req.WaitForResponse()
        if winhttp_req.Status == 200:
            text = winhttp_req.ResponseText
            case.assertRegex(text, expected_regex, msg=msg)
        else:
            case.fail(f"{msg}: {winhttp_req.Status} {winhttp_req.StatusText}")
    except pywintypes.com_error as e:
        if e.excepinfo[5] + 2**32 & 0xffff == win32inetcon.ERROR_INTERNET_TIMEOUT:
            details = "timed out"
        else:
            details = e.excepinfo[2].strip()
        case.fail(f"{msg}: {details}")
