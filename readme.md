# LZD Maya to Unreal Exporter
A small python script that removes annoyances when exporting from maya to unreal
## Installation
Drag the 2 files: `lzdExport_ui` and `lzdExport_utils` into your Maya scripts directory. 

To run the script use the following commands:

`import lzdExport_ui; lzdExport_ui.create_ui('lzd_Exporter')` - This opens the option menu where you can adjust your export settings.

`import lzdExport_utils; lzdExport_utils.export()` - This exports your current selection using your latest export settings. 


