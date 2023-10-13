import maya.cmds as cmds
import maya.OpenMaya as om

from functools import partial
import importlib

import lzdExport_utils as lzd_utils
importlib.reload(lzd_utils)

def create_ui(window_name):
    margin = 2
    ensure_root_dir_option_var()
    
    if cmds.window(window_name, ex=True):
        cmds.deleteUI(window_name)
    # Module Decleration
    module_window = cmds.window(window_name, title='Export Utils')
    base_layout = cmds.formLayout(p=module_window)  
    main_column_layout = cmds.columnLayout(adjustableColumn=True, p=base_layout, rowSpacing= margin)  
    cmds.formLayout(base_layout, e=True, attachForm=[(main_column_layout, 'left', margin), (main_column_layout, 'right', margin)])    

    title = cmds.text(label="Export Utils",p= main_column_layout)
    cmds.separator(p=main_column_layout)
    
    # File Dialogs / Reset Button
    unreal_content_dir_grp = build_file_dialog_grp(main_column_layout, label='Unreal Content Directory:', optionVar='lzd_content_dir', annotation='Set this field to your Unreal content directory.')
    root_dir_grp = build_file_dialog_grp(main_column_layout, label='Root Directory:', optionVar='lzd_root_dir', annotation='Directory in which your exported assets will be stored.')    
    
    reset_button_row_layout = cmds.rowLayout(p=main_column_layout, numberOfColumns=1,
                                        adjustableColumn=1)
    reset_button = cmds.button(label='Reset to Default', p=reset_button_row_layout, ann='Resets (or creates) the Root Directory to the assets folder in the parent directory of your maya project.',
                               c=partial(update_text_field_from_function, root_dir_grp[2], reset_root_dir_option_var))

    # Export Type Menu
    export_type_menu = cmds.optionMenuGrp(l='Export Type:', p=main_column_layout, adj=True)
    export_type_menu_single_file = cmds.menuItem(l='Single File', ann='Exports your whole selection as one file, with the name of your first selected object.')
    export_type_menu_multi_file = cmds.menuItem(l='Multiple Files', ann='Exports your selection into multiple files for every object, do not use this with groups.')
    export_type_menu_multi_folder = cmds.menuItem(l='Multiple Folders', ann='Exports your selection into multiple folders for every object, do not use this with groups.')
    
    # Export Buttons Form
    export_button_parent_layout = cmds.formLayout(p=base_layout, nd=3)
    cmds.formLayout(base_layout, e=True, attachForm=[(export_button_parent_layout, 'left', margin), (export_button_parent_layout, 'right', margin), (export_button_parent_layout, 'bottom', margin)])    
    cmds.formLayout(export_button_parent_layout, e=True)
    
    cur_export_type = cmds.optionMenuGrp(export_type_menu, q=True, value=True)
    b1 = cmds.button('Export', command=partial(export, cur_export_type))
    b2 = cmds.button('Export and Close', command=partial(export_and_close, cur_export_type, window_name))
    b3 = cmds.button(l='Close', command=partial(close_window, window_name))

    
    cmds.formLayout(export_button_parent_layout, e=True, attachForm=[(b1, 'left', margin), 
                                                                     (b3, 'right', margin)], 
                                                         attachPosition=[
                                                             (b1, 'right', margin, 1), 
                                                             (b2, 'left', margin, 1), 
                                                             (b2, 'right', margin, 2), 
                                                             (b3, 'left', margin, 2)])
    cmds.showWindow(module_window)

def export_and_close(export_type, window, *args):
    export(export_type)
    close_window(window)

def export(export_type, *args):
    lzd_utils.export(export_type)

def close_window(window, *args):
    cmds.deleteUI(window)

def build_file_dialog_grp(parent, label=str, optionVar=str, annotation=str):
    layout = cmds.rowLayout(p=parent, numberOfColumns=3, adjustableColumn=2, annotation=annotation,w=300)
    text = cmds.text(p=layout, label=label)
    text_field = cmds.textField(p=layout, 
                                tx=cmds.optionVar(q=optionVar), 
                                cc=partial(write_path_to_option_var, optionVar=optionVar))
    button = cmds.symbolButton(p=layout, 
                               image='fileOpen.png', 
                               command=partial(populate_text_field_from_file_dialog, 
                                               text_field, 
                                               partial(write_path_to_option_var, optionVar=optionVar)))
    return [layout, text, text_field, button]

def write_path_to_option_var(path, *args, optionVar=str):
    if args:
        path = args[0]
    cmds.optionVar(stringValue=(optionVar, path))
    
def populate_text_field_from_file_dialog(text_field, text_changed_function,*args):
    try:
        path = execute_file_dialog()
        cmds.textField(text_field,e=True, tx=path)
        text_changed_function(path)
    except:
        om.MGlobal.displayWarning('User cancelled file selection, reverting back to previously saved path.')

def execute_file_dialog():
     return cmds.fileDialog2(fileMode=2, dir=cmds.optionVar(q='lzd_root_dir'))[0]

def write_string_option_var(option_var_name, *args):
       cmds.optionVar(stringValue=(option_var_name, args[0]))

# Reset or create optionVar for "root dir" if project changes or optionVar doesn't exist.
def ensure_root_dir_option_var():
    root_dir = cmds.optionVar(q='lzd_root_dir') or lzd_utils.ensure_root_dir('assets')
    cmds.optionVar(stringValue=('lzd_root_dir', root_dir))

def update_text_field_from_function(text_field, update_function, *args):
    text = update_function()
    cmds.textField(text_field, e=True, tx=text)

def reset_root_dir_option_var():
    cmds.optionVar(stringValue=('lzd_root_dir', lzd_utils.ensure_root_dir('assets')))
    return cmds.optionVar(q='lzd_root_dir')

if __name__ == '__main__':
    cmds.window()
    create_ui('LZDExporter')