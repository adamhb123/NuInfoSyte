"""
NuInfoSys Middleware
Handles NuInfoSyte's web/api - NuInfoSys inter-operations
"""

from typing import List
from NuInfoSys import betabrite  # type: ignore

ANIMATIONS = []


def add_animation(text: str = None, mode: str = None, color: str = None, position: str = None) -> None:
    ANIMATIONS.append(betabrite.Animation(text, mode, color, position))


def send_animations() -> None:
    betabrite.send_animations(ANIMATIONS)


def get_modes(sort: bool = True) -> List:
    return sorted(betabrite.ANIMATION_MODE_DICT.keys()) if sort \
        else betabrite.ANIMATION_MODE_DICT.keys()


def get_colors(sort: bool = True) -> List:
    return sorted(betabrite.ANIMATION_COLOR_DICT.keys()) if sort \
        else betabrite.ANIMATION_COLOR_DICT.keys()


def get_positions(sort: bool = True) -> List:
    return sorted(betabrite.ANIMATION_POS_DICT.keys()) if sort \
        else betabrite.ANIMATION_POS_DICT.keys()


def supreme_mode() -> None:
    add_animation("Monster Energy presents...", "sparkle", "amber", None)
    add_animation("The Adam Brewer Memorial User Center", "cmprsrot", "rainbow2", None)
    add_animation("", "nosmoking", "", "")
    add_animation("", "drinkdrive", "", "")
    send_animations()


def snowflake_mode() -> None:
    add_animation("Welcome to Computer Science House!", "cmprsrot", "rainbow2", None)
    add_animation("", "cherrybomb", None, None)
    add_animation("Est. 1976", "sparkle", "amber", None)
    add_animation("", "sparkle", None, None)
    send_animations()


def based_mode() -> None:
    add_animation("", "drinkdrive", "", "")
    add_animation("@channel in #general", "sparkle", "amber", None)
    add_animation("", "nosmoking", "", "")
    add_animation("message brewer for a packet signature", "cherrybomb", "rainbow2", None)
    send_animations()


if __name__ == "__main__":
    based_mode()
