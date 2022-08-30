"""Introduction, purpose, and other notes
This project is a remake of the existing InfoSys project, with the goal
of being easier to read, maintain, and use.

This code is moderately based on Jonathan Koren's betabrite.py script,
so credit goes to him for a good portion of this. Most of this was
written fairly hastily so it is not the nicest code, but she gets
the job done, and I'll try and make it nicer over time.

~brewer
"""
import time
from datetime import datetime
from typing import Union, List, Dict
import random
from serial import Serial
from framecontrolbytes import FrameControlBytes

'''
Configurables
'''
CLI_ALLOW_TRANSMISSION = True
CLI_TERMINAL_AND = "-"  # Animation separator
CLI_ANIMATION_PROPERTY_SEPARATOR = ","  # Animation property separator
SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0"
'''
Nonconfigurables
'''
DOTS_TEST_ARROW = b"00000080000\r00000088000\r08888888800\r08888888880\r08888888800\r00000088000\r00000080000\r"
# Note that on the BetaBrite, position does not matter at all, so setting any of these does nothing
# IT IS still required to be sent in the message packet, however
ANIMATION_POS_DICT: Dict[str, FrameControlBytes] = {
    'middle': FrameControlBytes.TEXT_POS_MIDDLE,
    'top': FrameControlBytes.TEXT_POS_TOP,
    'bottom': FrameControlBytes.TEXT_POS_BOTTOM,
    'fill': FrameControlBytes.TEXT_POS_FILL
}

ANIMATION_COLOR_DICT: Dict[str, FrameControlBytes] = {
    'red': FrameControlBytes.TEXT_COLOR_RED,
    'green': FrameControlBytes.TEXT_COLOR_GREEN,
    'amber': FrameControlBytes.TEXT_COLOR_AMBER,
    'dimred': FrameControlBytes.TEXT_COLOR_DIMRED,
    'brown': FrameControlBytes.TEXT_COLOR_BROWN,
    'orange': FrameControlBytes.TEXT_COLOR_ORANGE,
    'yellow': FrameControlBytes.TEXT_COLOR_YELLOW,
    'rainbow1': FrameControlBytes.TEXT_COLOR_RAINBOW1,
    'rainbow2': FrameControlBytes.TEXT_COLOR_RAINBOW2,
    'mix': FrameControlBytes.TEXT_COLOR_MIX,
    'autocolor': FrameControlBytes.TEXT_COLOR_AUTO
}

ANIMATION_MODE_DICT: Dict[str, FrameControlBytes] = {
    'rotate': FrameControlBytes.MODE_ROTATE,
    'hold': FrameControlBytes.MODE_HOLD,
    'flash': FrameControlBytes.MODE_FLASH,
    'rollup': FrameControlBytes.MODE_ROLLUP,
    'rolldown': FrameControlBytes.MODE_ROLLDOWN,
    'rollleft': FrameControlBytes.MODE_ROLLLEFT,
    'rollright': FrameControlBytes.MODE_ROLLRIGHT,
    'wipeup': FrameControlBytes.MODE_WIPEUP,
    'wipedown': FrameControlBytes.MODE_WIPEDOWN,
    'wipeleft': FrameControlBytes.MODE_WIPELEFT,
    'wiperight': FrameControlBytes.MODE_WIPERIGHT,
    'scroll': FrameControlBytes.MODE_SCROLL,
    'automode': FrameControlBytes.MODE_AUTO,
    'rollin': FrameControlBytes.MODE_ROLLIN,
    'rollout': FrameControlBytes.MODE_ROLLOUT,
    'wipein': FrameControlBytes.MODE_WIPEIN,
    'wipeout': FrameControlBytes.MODE_WIPEOUT,
    'cmprsrot': FrameControlBytes.MODE_CMPRSROT,
    'twinkle': FrameControlBytes.MODE_TWINKLE,
    'sparkle': FrameControlBytes.MODE_SPARKLE,
    'snow': FrameControlBytes.MODE_SNOW,
    'interlock': FrameControlBytes.MODE_INTERLOCK,
    'switch': FrameControlBytes.MODE_SWITCH,
    'spray': FrameControlBytes.MODE_SPRAY,
    'starburst': FrameControlBytes.MODE_STARBURST,
    'welcome': FrameControlBytes.MODE_WELCOME,
    'slotmachine': FrameControlBytes.MODE_SLOTMACHINE,
    'newsflash': FrameControlBytes.MODE_NEWSFLASH,
    'trumpet': FrameControlBytes.MODE_TRUMPET,
    'thankyou': FrameControlBytes.MODE_THANKYOU,
    'nosmoking': FrameControlBytes.MODE_NOSMOKING,
    'drinkdrive': FrameControlBytes.MODE_DRINKDRIVE,
    'animal': FrameControlBytes.MODE_ANIMAL,
    'fish': FrameControlBytes.MODE_FISH,
    'fireworks': FrameControlBytes.MODE_FIREWORKS,
    'turbocar': FrameControlBytes.MODE_TURBOCAR,
    'balloons': FrameControlBytes.MODE_BALLOONS,
    'cherrybomb': FrameControlBytes.MODE_CHERRYBOMB
}


class Animation:
    """
    Object designed to represent normal animations
    """

    @staticmethod
    def _validate_parameter(parameter: Union[str, bytes], dictionary: Dict[str, bytes],
                            default_on_fail: Union[str, bytes]):
        if type(parameter) == str and parameter in dictionary.keys():
            return dictionary[parameter]
        elif parameter in dictionary.values():
            return parameter
        else:
            print(f"Invalid parameter provided to 'Animation' class constructor: parameter='{parameter}', "
                  f"defaulted to '{default_on_fail}'")
            return default_on_fail

    def __init__(self, text="", mode=FrameControlBytes.MODE_AUTO, color=FrameControlBytes.TEXT_COLOR_AUTO,
                 position=FrameControlBytes.TEXT_POS_MIDDLE):
        self.text = text
        self.mode = self._validate_parameter(mode, ANIMATION_MODE_DICT, FrameControlBytes.MODE_AUTO)
        self.color = self._validate_parameter(color, ANIMATION_COLOR_DICT, FrameControlBytes.TEXT_COLOR_AUTO)
        self.position = self._validate_parameter(position, ANIMATION_POS_DICT, FrameControlBytes.TEXT_POS_MIDDLE)

    def __str__(self):
        return f"Animation: text='{self.text}' mode={self.mode} color={self.color} position={self.position}"

    def __repr__(self):
        return self.__str__()

    def _is_valid_operand(self, other):
        return (hasattr(other, "lastname") and
                hasattr(other, "firstname"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return False

    def reset(self):
        self.text = ""
        self.mode = FrameControlBytes.MODE_AUTO
        self.color = FrameControlBytes.TEXT_COLOR_AUTO
        self.position = FrameControlBytes.TEXT_POS_MIDDLE

    def randomize(self):
        self.mode = random.choice(list(ANIMATION_MODE_DICT.values()))
        self.color = random.choice(list(ANIMATION_COLOR_DICT.values()))
        self.position = random.choice(list(ANIMATION_POS_DICT.values()))

    def display(self):
        _transmit(_write_file(self), ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)

    def bytestr(self):
        return FrameControlBytes.SOM + self.position + self.mode + self.color + _transcode(self.text)


def _transmit(payload: bytes, addr=FrameControlBytes.SIGN_ADDRESS_BROADCAST,
              ttype=FrameControlBytes.SIGN_TYPE_BETABRITE, port: str = SERIAL_PORT) -> None:
    """
    Transmits a single packet
    :param payload: packet Command Code + Data Field to transmit
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    packet = FrameControlBytes.WAKEUP + FrameControlBytes.SOH + ttype + addr + FrameControlBytes.STX + payload + FrameControlBytes.EOT
    ser = Serial(port, 9600, timeout=10)
    ser.write(packet)
    ser.close()


def _transmit_multi(payloads: List[bytes], addr=FrameControlBytes.SIGN_ADDRESS_BROADCAST,
                    ttype=FrameControlBytes.SIGN_TYPE_BETABRITE) -> None:
    """
    [UNTESTED]
    Transmits multiple packets (in nested packet format, as per 5.1.3 in the specification)
    :param payloads: packet Command Code + Data Field to transmit, as a list, where each item is the combined bytestring
    of each Command Code and Data Field pair
    :param addr: packet Sign Address - the address of the sign. See the protocol write-up summary for more details.
    :param ttype: packet Type Code - describes the type of sign we're communicating to
    :return: None
    """
    # This would be a cool one liner to form the packet BUT we need to have 100ms delays after <STX>'s
    # packet = WAKEUP + SOH + ttype + addr + STX + (ETX+STX).join(payloads) + ETX + EOT
    ser = Serial(SERIAL_PORT, 9600, timeout=10)
    # Initial wakeup
    ser.write(FrameControlBytes.WAKEUP + FrameControlBytes.SOH + ttype + addr)
    for payload in payloads:
        ser.write(FrameControlBytes.STX)
        # 100ms wait + python's performance delay should be adequate here
        time.sleep(.1)
        ser.write(payload + FrameControlBytes.ETX)
    # Signal end of packet transmission
    ser.write(FrameControlBytes.EOT)
    ser.close()


def _write_file(animations: Union[List[Animation], Animation], file: bytes = FrameControlBytes.FILE_PRIORITY) -> bytes:
    """Writes the given animations (which could be a single animation) in the proper payload format
    If file is anything but FILE_PRIORITY, then memory needs to be allocated and dealt with before hand
    Maybe I'll add a memory configuration function that assigns memory per some sort of input specification
    :param animations:
    :param file:
    :return:
    """
    #   Many animations
    if isinstance(animations, list):
        payload = FrameControlBytes.COMMAND_WRITE_TEXT + file
        for x in range(len(animations)):
            animation = animations.pop(0)
            payload += animation.bytestr()
    #   One animation
    elif isinstance(animations, Animation):
        payload = FrameControlBytes.COMMAND_WRITE_TEXT + file + animations.bytestr()
    else:
        raise ValueError(f"Invalid argument given: animations='{animations}'")
    return payload


def _transcode(msg: str) -> bytes:
    """
    Transcodes the given msg to an appropriate bytes representation
    :param msg: string to transcode
    :return: the msg's bytes representation
    """
    b = bytes(msg, 'utf-8')
    b = b.replace(b'\xc2\xb0', FrameControlBytes.DEGREES.value)
    return b


def set_time(serial_port: str = SERIAL_PORT) -> None:
    """
    [UNTESTED]
    Sets the time of day (in 24-hour format) in the sign, in the format HhMm
    :return: None
    """
    _transmit(
        FrameControlBytes.COMMAND_WRITE_SPECIAL + FrameControlBytes.SET_TIME + bytes(datetime.now().strftime("%H%M"),
                                                                                     'utf-8'),
        ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)


def send_dots(dots_data: bytes, file: bytes = FrameControlBytes.FILE_PRIORITY, serial_port: str = SERIAL_PORT) -> None:
    """
    [UNTESTED]
    Sends a SMALL DOTS PICTURE file to the sign, as per 6.4.1 in the specification
    dots_data should be formatted as such:
    2 hex bytes for height + 2 hex bytes for width + row bit pattern + carriage return
    :param file: File label to write to
    :param dots_data: DOTS data to transmit
    :param serial_port: port to transmit data to
    :return: None
    """
    _transmit(FrameControlBytes.COMMAND_WRITE_DOTS + file + dots_data, ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)


def soft_reset(serial_port: str = SERIAL_PORT):
    _transmit(FrameControlBytes.COMMAND_WRITE_SPECIAL + b"\x2c", ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)


def send_animations(animations: List[Animation]):
    """
    Transmits the given list of animations to the betabrite sign
    :param animations: list of animations to transmit
    :return: None
    """
    #   If you want to send just one animation, you can use its 'display()' method
    # _transmit(SERIAL_PORT, _write_file(animations, file=FILE_NORMAL_RANGE[0]))
    _transmit(_write_file(animations, file=FrameControlBytes.FILE_PRIORITY),
              ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)


def _cli_parse_animations_from_string(animation_string: str) -> List[Animation]:
    """
    animation_string should be formatted as such:
    FrameControlBytes.TEXT ANIMATION_MODE ANIMATION_COLOR ANIMATION_POSITION$CLI_TERMINAL_AND$NEXT_ANIMATION
    e.g. chungus cherrybomb rainbow2 None-bingus None amber None
    where '-' is replaced with the CLI_TERMINAL_AND
    """
    return _cli_parse_animations(animation_string.split(CLI_TERMINAL_AND))


def _cli_parse_animations(animations: List[str]):
    parsed_animations = []
    while len(animations) != 0:
        animget = animations.pop(0).split(CLI_ANIMATION_PROPERTY_SEPARATOR)
        animget[0] = animget[0] if animget[0] != "None" else ""
        animget[1] = ANIMATION_MODE_DICT[animget[1]] if animget[1] != "None" else FrameControlBytes.MODE_AUTO
        animget[2] = ANIMATION_COLOR_DICT[animget[2]] if animget[2] != "None" else FrameControlBytes.TEXT_COLOR_AUTO
        animget[3] = ANIMATION_POS_DICT[animget[3]] if animget[3] != "None" else FrameControlBytes.TEXT_POS_MIDDLE
        parsed_animations.append(
            Animation(animget[0], animget[1], animget[2], animget[3]))

    return parsed_animations


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "messages",
        help=f"messages to send, structured like: \n"
             f"FrameControlBytes.TEXT ANIMATION_FrameControlBytes.MODE ANIMATION_COLOR ANIMATION_POSITION{CLI_TERMINAL_AND}[next message or EOL]",
        nargs='+')
    args = parser.parse_args()
    # display_DOTS(None)
    animations = ' '.join(args.messages)
    parsed_animations = _cli_parse_animations_from_string(animations)
    if CLI_ALLOW_TRANSMISSION:
        _transmit(_write_file(parsed_animations), ttype=FrameControlBytes.SIGN_TYPE_BETABRITE)
    else:
        print(f"Packet: {animations}")


if __name__ == '__main__':
    main()
