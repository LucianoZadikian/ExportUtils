import maya.cmds as cmds
from functools import partial

import export_script as ex

export_type = str
asset_dir_name = str
file_name = str
project_dir = ex.get_parent_dir()
folder_name = str

cmds.optionVar(stringValue=('lzd_project_dir', ex.get_parent_dir()))

# Option vars
# need not only file paths/names, but also bools for each of the checkboxes. 
# probably need to refactor checkbox code. we need to query our option vars to see if they're enabled or not. 
# implement reverting to default?
# apply button, like default maya. Probably need another layout, row I think?
def create_ui(window_name):
    if cmds.window(window_name, ex=True):
        cmds.deleteUI(window_name)
    
    module_window = cmds.window(window_name, title='Export Utils', w=260)
    module_layout = cmds.columnLayout(adjustableColumn=True, p=module_window)
    

    # Widget Decleration
    title = cmds.text(label="Exporter",p= module_layout,)

    override_root_dir_checkbox = cmds.checkBoxGrp(l='Override Root Directory:', p=module_layout)
    
    
    
    override_root_dir_textfield = cmds.textFieldGrp(l='Root Directory:', 
                                                    tx=ex.get_parent_dir(),
                                                    en=False, 
                                                    p=module_layout )

    cmds.checkBoxGrp(override_root_dir_checkbox, e=True, onc=partial(toggle_text_field_from_checkbox, 
                                                                     override_root_dir_checkbox, 
                                                                     override_root_dir_textfield),
                                                         ofc= partial(toggle_text_field_from_checkbox, 
                                                                     override_root_dir_checkbox, 
                                                                     override_root_dir_textfield))
    
    export_type_menu = cmds.optionMenuGrp(l='Export Type:', p=module_layout)
    export_type_menu_single_file = cmds.menuItem(l='Single File')
    export_type_menu_multi_file = cmds.menuItem(l='Multiple Files')
    export_type_menu_multi_folder = cmds.menuItem(l='Multiple Folders')
    
    # Create widgets for overriding file names
    override_file_name_checkbox = cmds.checkBoxGrp(l='Override File Name:', p=module_layout)
    override_file_name_text_field = cmds.textFieldGrp(l='File Name:',
                                                      tx=cmds.ls(sl=True)[0],
                                                      en=False,
                                                      p=module_layout)
    
    # Create Widgets for overriding folder names
    override_folder_name_checkbox = cmds.checkBoxGrp(l='Override Folder Name:', p=module_layout)

    
    override_folder_name_text_field = cmds.textFieldGrp(l='Folder Name:',
                                                      tx=cmds.ls(sl=True)[0],
                                                      en=False,
                                                      p=module_layout)
    #cmds.fileDialog2() - Implement later 
    # Assign commands to our override widgets
    
    cmds.checkBoxGrp(override_file_name_checkbox, e=True, onc=partial(toggle_text_field_from_checkbox, 
                                                                     override_file_name_checkbox, 
                                                                     override_file_name_text_field),
                                                          ofc=partial(toggle_text_field_from_checkbox, 
                                                          override_file_name_checkbox, 
                                                          override_file_name_text_field))
    cmds.checkBoxGrp(override_folder_name_checkbox, e=True, onc=partial(toggle_text_field_from_checkbox, 
                                                                     override_folder_name_checkbox, 
                                                                     override_folder_name_text_field),
                                                          ofc=partial(toggle_text_field_from_checkbox, 
                                                          override_folder_name_checkbox, 
                                                          override_folder_name_text_field))
    
    # Assign command our export menu
    cmds.optionMenuGrp(export_type_menu, e=True, cc=partial(toggle_override_name,
                                                            override_file_name_checkbox,
                                                            override_folder_name_checkbox))
    
    
    # TODO: Implement OptionVars for persistent window state
    """
        Title: Text
        Override Root Directory: Checkbox - would activate Root Dir
        Root Dir: Text field - implement default/ file dialog button
        Export Type: Options Menu - implement different export funcs.  
        Override file naming: Checkbox - only visible on base export.
         
    """ 

    cmds.showWindow(module_window)

def update_export_type_menu(checkbox_grp1, checkbox_grp2, *args):
    toggle_override_name(checkbox_grp1, checkbox_grp2, *args)
    change_export_type()

def change_export_type():
    pass

def toggle_text_field_from_checkbox(checkbox_grp, text_field_grp,*args):
    new_text_field_grp = cmds.textFieldGrp(text_field_grp, e=True, en=args[0]) 

def toggle_override_name(checkbox_grp1,checkbox_grp2, *args):
    b = True
    if args[0] == 'Multiple Folders':
        b = False
    new_checkbox_grp1 = cmds.checkBoxGrp(checkbox_grp1, e=True, en=b)
    new_checkbox_grp2 = cmds.checkBoxGrp(checkbox_grp2, e=True, en=b)

def write_string_option_var(option_var_name, *args):
       cmds.optionVar(stringValue=(option_var_name, args[0]))
if __name__ == '__main__':
    
    cmds.window()
    create_ui('LZDExporter')