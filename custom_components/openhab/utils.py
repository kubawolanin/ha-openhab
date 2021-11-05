"""Utils"""


def strip_ip(url: str):
    """Strip IP/Hostname from URL"""
    return url.split("/")[2].split(":")[0]


def str_to_hsv(state: str) -> tuple[float, float, float]:
    """Convert state string to hsv tuple"""
    c = state.split(",")
    return [float(c[0]), float(c[1]), float(c[2])]


def hsv_to_str(hsv: tuple[float, float, float]) -> str:
    """Convert state string to hsv tuple"""
    return f"{round(hsv[0])},{round(hsv[1])},{round(hsv[2])}"
