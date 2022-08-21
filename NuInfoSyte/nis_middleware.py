"""
NuInfoSys Middleware
Handles NuInfoSyte's web/api - NuInfoSys inter-operations
"""

import requests
from typing import List, Optional, Union, Callable, Dict
from dataclasses import dataclass, field


@dataclass
class APIAddress:
    protocol: Optional[str] = None
    ip: Optional[str] = None
    port: Optional[Union[str, int]] = None
    endpoints: Dict[str, str] = field(default_factory=lambda: {
        "send-animations": "send-animations",
        "add-animation": "add-animation",
        "remove-animation": "remove-animation",
        "get-colors": "colors",
        "get-modes": "modes",
        "get-positions": "positions"
    })

    def is_initialized(self):
        return all([self.protocol, self.ip])

    def __str__(self):
        return f"{APIADDRESS.protocol}{APIADDRESS.ip}:{APIADDRESS.port}"


APIADDRESS = APIAddress()


def InitVerifier(func: Callable):
    def wrapper(*args, **kwargs):
        if APIADDRESS.is_initialized:
            return func(*args, **kwargs)
        else:
            raise Exception("Address not initialized")

    return wrapper


@InitVerifier
def initialize(protocol: str, ip: str, port: Optional[Union[str, int]]):
    APIADDRESS.protocol = protocol
    APIADDRESS.ip = ip
    APIADDRESS.port = port


@InitVerifier
def add_animation(text: Optional[str] = None, mode: Optional[str] = None, color: Optional[str] = None) -> None:
    """
    Add animation
    """
    requests.put(f"{APIADDRESS}/add-animation", data={
        "text": text,
        "mode": mode,
        "color": color
    })


@InitVerifier
def remove_animation(text: Optional[str] = None, mode: Optional[str] = None, color: Optional[str] = None) -> None:
    """
    Remove animation TO BE DONE NOT FINISHED
    """
    # for animation in _ANIMATIONS:
    #     if animation.text == text and not mode and not color:
    #         _ANIMATIONS.remove(animation)
    #     else:
    #         (animation.text == text and animation.mode == mode and animation.color == color)
    requests.put(f"{APIADDRESS}/remove-animation", data={
        "text": text,
        "mode": mode,
        "color": color
    })


@InitVerifier
def send_animations() -> None:
    """
    Send animation
    """
    requests.put(f"{APIADDRESS}/remove-animation")


@InitVerifier
def get_modes() -> List:
    """
    Get modes
    """

    modes = requests.get(f"{APIADDRESS}/modes").json()
    if modes:
        return sorted(modes)


@InitVerifier
def get_colors() -> List:
    """
    Get colors
    """
    colors = requests.get(f"{APIADDRESS}/colors").json()
    if colors:
        return sorted(colors)


@InitVerifier
def get_positions() -> List:
    """
    Get positions
    """

    positions = requests.get(f"{APIADDRESS}/positions").json()
    if positions:
        return sorted(positions)


@InitVerifier
def supreme_mode() -> None:
    """
    Supreme mode
    """
    add_animation("Monster Energy presents...", "sparkle", "amber")
    add_animation("The Adam Brewer Memorial User Center",
                  "cmprsrot", "rainbow2")
    add_animation("", "nosmoking", "")
    add_animation("", "drinkdrive", "")
    send_animations()


@InitVerifier
def snowflake_mode() -> None:
    add_animation("Welcome to Computer Science House!", "cmprsrot", "rainbow2")
    add_animation("", "cherrybomb", None)
    add_animation("Est. 1976", "sparkle", "amber")
    add_animation("", "sparkle", None)
    send_animations()


@InitVerifier
def based_mode() -> None:
    add_animation("", "drinkdrive", "")
    add_animation("@channel in #general", "sparkle", "amber")
    add_animation("", "nosmoking", "")
    add_animation("message brewer for a packet signature",
                  "cherrybomb", "rainbow2")
    send_animations()


if __name__ == "__main__":
    based_mode()
