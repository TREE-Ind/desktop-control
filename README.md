# skill-autogui
A Mycroft AI skill to enable keyboard and mouse manipulation via voice command using Autogui

## Usage:
* `type Mycroft is awesome`
* `press enter`
* `scroll up 10 clicks`
* `scroll down 10 clicks`
* `scroll right 10 clicks - Linux only`
* `hold down key`
* `release down key`
* `screen resolution`


## Known Issues:

Fuzzy matching will probably be needed for some of the keyboard commands such as "f1" to trigger correctly

## Todo:

Mouse manipulation code is currently incomplete and not functional - WIP
Implement more keyboard command and hotkey intents.

Use ScreenLocation to move mouse to Google search bar or other common UI elements directly.  Such as "Move mouse to google search bar"
