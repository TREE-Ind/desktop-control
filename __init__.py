# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

import pyautogui
import platform
from num2words import num2words

__author__ = 'eClarity'

LOGGER = getLogger(__name__)


class AutoguiSkill(MycroftSkill):
    def __init__(self):
        super(AutoguiSkill, self).__init__(name="AutoguiSkill")

    def initialize(self):
        type_intent = IntentBuilder("TypeIntent"). \
            require("TypeKeyword").require("Text").build()
        self.register_intent(type_intent, self.handle_type_intent)

        mouse_absolute_intent = IntentBuilder("MouseAbsoluteIntent"). \
            require("MouseAbsoluteKeyword").require("X").require("Y").build()
        self.register_intent(mouse_absolute_intent, self.handle_mouse_absolute_intent)

        mouse_scroll_down_intent = IntentBuilder("MouseScrollDownIntent"). \
            require("MouseScrollDownKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_down_intent, self.handle_mouse_scroll_down_intent)

        mouse_scroll_up_intent = IntentBuilder("MouseScrollUpIntent"). \
            require("MouseScrollUpKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_up_intent, self.handle_mouse_scroll_up_intent)

        mouse_scroll_right_intent = IntentBuilder("MouseScrollRightIntent"). \
            require("MouseScrollRightKeyword").require("Scroll").build()
        self.register_intent(mouse_scroll_right_intent, self.handle_mouse_scroll_right_intent)

        screen_res_intent = IntentBuilder("ScreenResIntent"). \
            require("ScreenResKeyword").build()
        self.register_intent(screen_res_intent, self.handle_screen_res_intent)

        press_key_intent = IntentBuilder("PressKeyIntent"). \
            require("PressKeyKeyword").require("Key").build()
        self.register_intent(press_key_intent, self.handle_press_key_intent)

        hold_key_intent = IntentBuilder("HoldKeyIntent"). \
            require("HoldKeyKeyword").require("Key").build()
        self.register_intent(hold_key_intent, self.handle_hold_key_intent)

        release_key_intent = IntentBuilder("ReleaseKeyIntent"). \
            require("ReleaseKeyKeyword").require("Key").build()
        self.register_intent(release_key_intent, self.handle_release_key_intent)

        select_combination_intent = IntentBuilder("SelectCombinationIntent"). \
            require("SelectAllKeyword").optionally("CopyKeyword"). \
                                        optionally("CutKeyword"). \
                                        optionally("PasteKeyword").\
                                        optionally("DeleteKeyword").build()
        self.register_intent(select_combination_intent, self.handle_select_combination_intent)


        copy_intent = IntentBuilder("CopyIntent"). \
            require("CopyKeyword").build()
        self.register_intent(copy_intent, self.handle_copy_intent)

        cut_intent = IntentBuilder("CutIntent"). \
            require("CutKeyword").build()
        self.register_intent(cut_intent, self.handle_cut_intent)

        paste_intent = IntentBuilder("PasteIntent"). \
            require("PasteKeyword").build()
        self.register_intent(paste_intent, self.handle_paste_intent)

    def handle_type_intent(self, message):
        self.speak_dialog("typing")
        text = message.data.get('Text')
        pyautogui.typewrite(text, interval=0.05)

    def handle_mouse_absolute_intent(self, message):
        self.speak('moving mouse now')
    #X = message.data.get('X')
    #Y = message.data.get('Y')
        #pyautogui.moveTo(X, Y)

    def handle_mouse_scroll_down_intent(self, message):
        self.speak('scrolling down now')
        scroll = message.data.get('Scroll')
        scroll_down = int(scroll) * -1
        pyautogui.scroll(scroll_down)

    def handle_mouse_scroll_up_intent(self, message):
        self.speak('scrolling up now')
        scroll = message.data.get('Scroll')
        scroll_up = int(scroll)
        pyautogui.scroll(scroll_up)

    def handle_mouse_scroll_right_intent(self, message):
        if platform.system().lower().startswith('lin'):
            self.speak('scrolling right now')
            scroll = message.data.get('Scroll')
            scroll_right = int(scroll)
            pyautogui.hscroll(scroll_right)
        else:
            self.speak('Sorry, I cannot scroll right on your current operating system')

    def handle_screen_res_intent(self, message):
        screen = pyautogui.size()
        resx = screen[0]
        resy = screen[1]
        responsex = num2words(resx)
        responsey = num2words(resy)
        self.speak("Your screen resolution is %s by %s" % (responsex, responsey))

    def handle_press_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Pressing %s" % key)
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)

    def handle_hold_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Holding down %s key" % key)
        pyautogui.keyDown(key)

    def handle_release_key_intent(self, message):
        key = message.data.get('Key')
        self.speak("Releasing %s key" % key)
        pyautogui.keyUp(key)

    def handle_copy_intent(self, message):
        pyautogui.hotkey("ctrl", "c")
        self.speak("Okay Copied!")

    def handle_cut_intent(self, message):
        self.speak("Cutting to clipboard")
        pyautogui.hotkey("ctrl", "x")

    def handle_paste_intent(self, message):
        self.speak("Pasting from clipboard")
        pyautogui.hotkey("ctrl", "v")

    def handle_select_combination_intent(self, message):
        self.speak("Selecting all")
        pyautogui.hotkey("ctrl", "a")
        if message.data.get("PasteKeyword"):
            self.handle_paste_intent(message)
        elif message.data.get("CopyKeyword"):
            self.handle_copy_intent(message)
        elif message.data.get("CutKeyword"):
            self.handle_cut_intent(message)
        elif message.data.get("DeleteKeyword"):
            self.speak("deleting")
            pyautogui.keyDown("delete")
            pyautogui.keyUp("delete")
            

    def stop(self):
        pass


def create_skill():
    return AutoguiSkill()
