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

from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG

import pyautogui
import platform
from num2words import num2words

__author__ = 'eClarity'


class AutoguiSkill(MycroftSkill):
    def __init__(self):
        super(AutoguiSkill, self).__init__(name="AutoguiSkill")

    def initialize(self):
        
        self.sm_amount = 2
        self.med_amount = 6
        self.lg_amount = 12

        #self.register_intent_file('scroll.intent', self.handle_scroll)
        self.register_entity_file("direction.entity")
        self.register_entity_file("smallscroll.entity")
        self.register_entity_file("medscroll.entity")
        self.register_entity_file("largescroll.entity")
        
        self.register_entity_file("x.entity")
        self.register_entity_file("y.entity")
        
        self.register_entity_file("key.entity")

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

    @intent_file_handler("scroll.intent")
    def handle_scroll(self, message):
        direction = message.data.get("direction")
        if message.data.get("smallscroll"):
            if direction == "down":
                scroll_down = self.sm_amount * -1
                pyautogui.scroll(scroll_down)
            elif direction == "up":
                scroll_up = self.sm_amount
                pyautogui.scroll(scroll_up)
        elif message.data.get("medscroll"):
            if direction == "down":
                scroll_down = self.med_amount * -1
                pyautogui.scroll(scroll_down)
            elif direction == "up":
                scroll_up = self.med_amount
                pyautogui.scroll(scroll_up)
        elif message.data.get("largescroll"):
            if direction == "down":
                scroll_down = self.lg_amount * -1
                pyautogui.scroll(scroll_down)
            elif direction == "up":
                scroll_up = self.lg_amount
                pyautogui.scroll(scroll_up)


    @intent_handler(IntentBuilder("TypeIntent").require("TypeKeyword").require("Text"))
    def handle_type_intent(self, message):
        self.speak_dialog("typing")
        text = message.data.get('Text')
        pyautogui.typewrite(text, interval=0.05)

    @intent_file_handler("absolutemousemove.intent")
    def handle_absolute_mouse_move_intent(self, message):
        x = message.data.get("x")
        y = message.data.get("y")
        pyautogui.moveTo(int(x), int(y))
        self.speak_dialog("absolutemousemove", {"x": x, "y": y})

    def handle_mouse_scroll_right_intent(self, message):
        if platform.system().lower().startswith('lin'):
            self.speak('scrolling right now')
            scroll = message.data.get('Scroll')
            scroll_right = int(scroll)
            pyautogui.hscroll(scroll_right)
        else:
            self.speak('Sorry, I cannot scroll right on your current operating system')
    
    @intent_handler(IntentBuilder("ScreenResIntent").require("ScreenResKeyword"))
    def handle_screen_res_intent(self, message):
        screen = pyautogui.size()
        resx = screen[0]
        resy = screen[1]
        responsex = num2words(resx)
        responsey = num2words(resy)
        self.speak_dialog("screenresolution", {"x": responsex, "y": responsey})

    @intent_file_handler("presskey.intent")
    def handle_press_key_intent(self, message):
        key = message.data.get("key")
        self.speak("Pressing %s" % key)
        key = str(key)
        print(key)
        pyautogui.press(key)

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
        else:
            pass
            

    def stop(self):
        pass


def create_skill():
    return AutoguiSkill()
