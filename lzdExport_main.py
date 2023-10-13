import maya.cmds as cmds

import importlib

import lzdExport_utils as lzd_utils
import lzdExport_ui as lzd_ui

importlib.reload(lzd_ui, lzd_utils)

cmds.runTimeCommand()