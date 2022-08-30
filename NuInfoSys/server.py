"""
Provides optional API functionality for web / backend modularity
"""
from typing import List, Optional
import subprocess
from fastapi import FastAPI
from . import betabrite
import pathlib
"""
NuInfoSys Middleware
Handles NuInfoSyte's web/api - NuInfoSys inter-operations
"""


app = FastAPI()
_ANIMATIONS: List[betabrite.Animation] = []

@app.put("/add-animation")
def add_animation(text: Optional[str] = None, mode: Optional[str] = None, color: Optional[str] = None) -> None:
    """
    Add animation
    """
    _ANIMATIONS.append(betabrite.Animation(text, mode, color))

@app.put("/remove-animation")
def remove_animation(text: Optional[str] = None, mode: Optional[str] = None, color: Optional[str] = None) -> None:
    """
    Remove animation TO BE DONE NOT FINISHED
    """
    for animation in _ANIMATIONS:
        if animation.text == text and not mode and not color:
            _ANIMATIONS.remove(animation)
        else:
            (animation.text == text and animation.mode == mode and animation.color == color)

@app.put("/send-animations")
def send_animations() -> None:
    """
    Send animation
    """
    betabrite.send_animations(_ANIMATIONS)

@app.get("/modes")
def get_modes() -> List:
    """
    Get modes
    """
    return sorted(betabrite.ANIMATION_MODE_DICT.keys())

@app.get("/colors")
def get_colors() -> List:
    """
    Get colors
    """
    return sorted(betabrite.ANIMATION_COLOR_DICT.keys())

@app.get("/positions")
def get_positions() -> List:
    """
    Get positions
    """
    return sorted(betabrite.ANIMATION_POS_DICT.keys())

@app.put("/supreme-mode")
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

@app.put("/snowflake-mode")
def snowflake_mode() -> None:
    add_animation("Welcome to Computer Science House!", "cmprsrot", "rainbow2")
    add_animation("", "cherrybomb", None)
    add_animation("Est. 1976", "sparkle", "amber")
    add_animation("", "sparkle", None)
    send_animations()

@app.put("/based-mode")
def based_mode() -> None:
    add_animation("", "drinkdrive", "")
    add_animation("@channel in #general", "sparkle", "amber")
    add_animation("", "nosmoking", "")
    add_animation("message brewer for a packet signature",
                    "cherrybomb", "rainbow2")
    send_animations()
    
def start_main(port=3001):
    p = subprocess.Popen(["uvicorn", "server:app", "--port", str(port),  "--app-dir", pathlib.Path(__file__).parent.resolve(), "--reload"])
        
def start(port=3001):
    p = subprocess.Popen(["uvicorn", "server:app", "--port", str(port), "--app-dir", pathlib.Path(__file__).parent.resolve(), "--reload"])
    
if __name__=="__main__":
    start_main()