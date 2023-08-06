"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Imports
# Files
import disspy.activity
import disspy.app_commands
import disspy.application
import disspy.client
import disspy.channel
import disspy.embed
import disspy.errors
import disspy.guild
import disspy.reaction
import disspy.typ
import disspy.ui
import disspy.user

# Classes
from disspy.activity import Activity, ActivityType
from disspy.app_commands import (
    ApplicationCommandType,
    Context,
    Option,
    OptionType,
    StrOption,
    IntOption,
    NumOption,
    BoolOption,
    UserOption,
    ChannelOption,
    Localization,
)
from disspy.channel import (
    Channel,
    ChannelType,
    Message,
    RawMessage,
)
from disspy.client import Client
from disspy.http import Flags
from disspy.embed import Embed, Field, Color
from disspy.guild import Guild
from disspy.user import User
from disspy.reaction import Emoji, Reaction
from disspy.ui import (
    Component,
    ActionRow,
    Button,
    ButtonStyle,
    TextInput,
    SelectMenu,
    SelectMenuOption,
)
from disspy.state import ConnectionState
from disspy.webhook import DispyWebhook, TypingInfo
from disspy.application import Application

# Methods for other variables
def _all_generator(alls: list) -> tuple:
    result = []

    for file_all in alls:
        if isinstance(file_all, str):
            result.append(file_all)
        else:
            for element in file_all:
                result.append(element)

    return tuple(result)


# Info about package
__version__ = "0.7"
__pkgname__ = "disspy"
__description__ = "Dispy - package for creating bots in discord written in Python"
__github__ = "https://github.com/itttgg/dispy"

# __all__
__alls__: list = [
    disspy.activity.__all__,
    disspy.app_commands.__all__,
    disspy.application.__all__,
    disspy.client.__all__,
    disspy.channel.__all__,
    disspy.embed.__all__,
    disspy.errors.__all__,
    disspy.guild.__all__,
    disspy.reaction.__all__,
    disspy.ui.__all__,
    disspy.user.__all__,
]

__all__: tuple = _all_generator(__alls__)
