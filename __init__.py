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

__author__ = 'TREE_Ind'

class DesktopControlSkill(MycroftSkill):
    def __init__(self):
        super(DesktopControlSkill, self).__init__(name="DesktopControlSkill")

    def initialize(self):
        
        self.sm_amount = 2
        self.med_amount = 6
        self.lg_amount = 12

        self.register_entity_file("smallscroll.entity")
        self.register_entity_file("medscroll.entity")
        self.register_entity_file("largescroll.entity")
        self.register_entity_file("down.entity")
        self.register_entity_file("up.entity")
        
        self.register_entity_file("x.entity")
        self.register_entity_file("y.entity")
        
        self.register_entity_file("key.entity")

        select_combination_intent = IntentBuilder("SelectCombinationIntent"). \
            require("SelectAllKeyword").optionally("CopyKeyword"). \
                                        optionally("CutKeyword"). \
                                        optionally("PasteKeyword").\
                                        optionally("DeleteKeyword").build()
        self.register_intent(select_combination_intent, self.handle_select_combination_intent)

    @intent_file_handler("scroll.intent")
    def handle_scroll(self, message):
        if message.data.get("smallscroll"):
            if message.data.get("down"):
                scroll_down = self.sm_amount
                pyautogui.scroll(scroll_down)
            if message.data.get("up"):
                scroll_up = self.sm_amount * -1
                pyautogui.scroll(scroll_up)
        elif message.data.get("medscroll"):
            if message.data.get("down"):
                scroll_down = self.med_amount
                pyautogui.scroll(scroll_down)
            if message.data.get("up"):
                scroll_up = self.med_amount * -1
                pyautogui.scroll(scroll_up)
        elif message.data.get("largescroll"):
            if message.data.get("down"):
                scroll_down = self.lg_amount
                pyautogui.scroll(scroll_down)
            if message.data.get("up"):
                scroll_up = self.lg_amount * -1
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
        self.speak_dialog("keypress", {"key": key})
        key = str(key)
        pyautogui.press(key)

    @intent_file_handler("holdkey.intent")
    def handle_hold_key_intent(self, message):
        key = message.data.get("key")
        self.speak_dialog("keyhold", {"key": key})
        pyautogui.keyDown(key)

    @intent_file_handler("releasekey.intent")
    def handle_release_key_intent(self, message):
        key = message.data.get('key')
        self.speak_dialog("keyrelease", {"key": key})
        pyautogui.keyUp(key)

    @intent_handler(IntentBuilder("CopyIntent").require("CopyKeyword"))
    def handle_copy_intent(self, message):
        pyautogui.hotkey("ctrl", "c")
        self.speak("Okay Copied!")

    @intent_handler(IntentBuilder("CutIntent").require("CutKeyword"))
    def handle_cut_intent(self, message):
        self.speak("Cutting to clipboard")
        pyautogui.hotkey("ctrl", "x")

    @intent_handler(IntentBuilder("PasteIntent").require("PasteKeyword"))
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
    return DesktopControlSkill()
