# LZD Maya to Unreal Exporter
A small python script that removes annoyances when exporting from maya to unreal
## Installation
Drag the 2 files: `lzdExport_ui` and `lzdExport_utils` into your Maya scripts directory. 

To run the script use the following commands:

`import lzdExport_ui; lzdExport_ui.create_ui('lzd_Exporter')` - This opens the option menu where you can adjust your export settings.

`import lzdExport_utils; lzdExport_utils.export()` - This exports your current selection using your latest export settings. 

You can bind these commands to hotkeys by doing the following:


1. Open the hotkey editor, and press the Runtime Command Editor Tab on the right
2. Hit the "New" button, and give it a name.
3. Change the language to python
4. Paste above command.
5. Hit "Save Runtime Command". Then assign like anormal Hotkey

![HotKeyGuide](hotkey_guide.png)

