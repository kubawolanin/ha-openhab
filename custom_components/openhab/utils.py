"""Utils"""


def strip_ip(url: str):
    """Strip IP/Hostname from URL"""
    return url.split("/")[2].split(":")[0]
