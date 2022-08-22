"""
Memory manager
Doesn't work lol
"""

from typing import Dict, Union
from enum import Enum
from dataclasses import dataclass
from .framecontrolbytes import FrameControlBytes

"""
The sum of all the file sizes (except for SMALL DOTS PICTURE and LARGE DOTS PICTURE files) plus 11 bytes of overhead
for each file should not exceed the total amount of available memory in the pool. A value of “0000” is a valid SIZE for
the last file in the Memory Configuration only if this last file is a TEXT file. This assigns all remaining memory to
the file."

As a result of this, I am capping the TOTAL_MEMORY allowed to be allocated to the below value. 
This was calculated by the following formula:

TRUE_MEMORY_SIZE (30000 bytes)
- PRIORITY_FILE_SIZE(125 bytes)
- OVERHEAD(11 bytes per file)*MAX_FILE_COUNT(65 message files)
- CAUSE_IT_MAKES_ME_FEEL_BETTER_BYTES(4160 bytes)
= 25000 bytes

TOTAL_MEMORY = 25000
"""

class MemoryConfigurationType(Enum):
    """
    Memory configuration settings
    ALL_FILES_EQUAL: indicates that each of the 100+ files should share an equal amount of memory
    FIRST_FILE_MAX: lazy method, indicates that the first (non-priority) file should have all the memory
    CUSTOM: indicates that memory allocation will be defined by some collection
    """
    ALL_FILES_EQUAL = 0
    FIRST_FILE_MAX = 1
    CUSTOM = 2


class Memory:
    """
    Handles memory, constructing it as described

    Here is what a custom memory map would look look like

    MemoryMap: Dict[bytes, int] = {
        FILE_NORMAL_RANGE[0]: 1000, # == 1000 bytes of data allocated to the first non-priority file
        FILE_NORMAL_RANGE[1]: 2000, # == 2000 bytes of data allocated to the second non-priority file
        .
        .
        .
    }
    """

    def __init__(self, memory_configuration: Union[
        MemoryConfigurationType, Dict[bytes, int]] = MemoryConfigurationType.FIRST_FILE_MAX):
        self.map: Dict[bytes, int] = self._memory_map_from_configuration(memory_configuration)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.map.__str__()

    def bytes(self) -> bytes:
        return b''.join([k for k, v in self.map.items()])

    @staticmethod
    def clear():
        """
        [UNTESTED]
        Clears the sign memory
        """
        return FrameControlBytes.COMMAND_WRITE_SPECIAL + FrameControlBytes.MODIFY_MEMORY

    def flash(self):
        """
        [UNTESTED]
        Flashes the memory map to the betabrite
        """
        # to be rewritten
        return FrameControlBytes.COMMAND_WRITE_SPECIAL + FrameControlBytes.MODIFY_MEMORY + b''.join(
            [b"%s%s%s%s%s" % (k, FrameControlBytes.FILE_TYPE_TEXT, FrameControlBytes.FILE_LOCKED, v.to_bytes(4, 'big'), FrameControlBytes.TEXT_FILE_START_TIME_ALWAYS) for
             k, v in self.map.items()])

    @staticmethod
    def _memory_map_from_configuration(config: MemoryConfigurationType):
        if config == MemoryConfigurationType.FIRST_FILE_MAX:
            return {k: FrameControlBytes.TOTAL_MEMORY if k == FrameControlBytes.FILE_NORMAL_RANGE[0] else 0 for k in FrameControlBytes.FILE_NORMAL_RANGE}
        elif config == MemoryConfigurationType.ALL_FILES_EQUAL:
            return {k: FrameControlBytes.TOTAL_MEMORY / len(FrameControlBytes.FILE_NORMAL_RANGE) for k in FrameControlBytes.FILE_NORMAL_RANGE}
        else:
            raise Exception({
                ValueError("Inappropriate argument: 'config'"),
                MemoryConfigurationError("Inappropriate MemoryConfigurationType specified")
            })


# Modify MemoryMap as described below and specify MemoryConfigurationType.CUSTOM in relevant functions for custom mapping


class MemoryConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)
