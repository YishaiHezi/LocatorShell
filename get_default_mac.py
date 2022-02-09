import getmac
import netifaces


def get_router_mac():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    mac = getmac.get_mac_address(ip=default_gateway, network_request=True)

    return mac
