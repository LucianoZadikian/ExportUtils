import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel

import os 
import shutil

def export():
    export_type = cmds.optionVar(q='lzd_export_type')
    path=cmds.optionVar(q='lzd_root_dir')
    if cmds.optionVar(q='lzd_content_dir') == 0:
        om.MGlobal.displayError('Unable to find Unreal Content Directory. Please set the Unreal Content Directory using the options menu.')
        return
    else:
        if export_type == 'Single File': export_asset_single_file(path); return
        if export_type == 'Multiple Files': export_asset_multiple_files(path); return
        else: export_asset_multiple_folders(path)
        # try:
        #     if export_type == 'Single File': export_asset_single_file(path)
        #     if export_type == 'Multiple Files': export_asset_multiple_files(path)
        #     else: export_asset_multiple_folders(path)
        # except:
        #     om.MGlobal.displayError(f'Directory: {path} does not exist. Please set your Root Directory using the options menu.')
    
def export_asset_base(asset, path):
    pos = cmds.xform(asset, q=True, t=True)
    if len(cmds.ls(sl=True)) > 1:
        cmds.xform(cmds.ls(sl=True), a=True, t=[0, 0, 0], r=True, ws=True)

    if not os.path.exists(path):
        os.mkdir(path)

    mel.eval(f'FBXExport -f "{path}/{asset}.fbx" -s')
    om.MGlobal.displayInfo(f'Exported {asset} to directory {path}.') # Success message
    if asset.rfind('_hp') > -1:
        om.MGlobal.displayInfo(f'Excluding {asset} from being copied to Unreal Content Directory because it ends in "_hp"!')
    else:
        shutil.copy(f'{path}/{asset}.fbx', f'{cmds.optionVar(q="lzd_content_dir")}/{asset}.fbx')
    cmds.xform(cmds.ls(sl=True), a=True, t=pos)


# Exports objects in our selection in different fbx files under the directory of the first selected
def export_asset_multiple_files(path):
    selection = cmds.ls(sl=True)
    path = f'{path}/{selection[0]}'
    for asset in selection:
        cmds.select(asset)
        export_asset_base(asset, path)
    cmds.select(selection) # Reselect original selection 

# Exports objects in our selection in different folders. 
def export_asset_multiple_folders(path):
    selection = cmds.ls(sl=True)
    for asset in selection:
        path = f'{path}/{asset}'
        cmds.select(asset)
        export_asset_base(asset, path)
    cmds.select(selection) # Reselect original selection

def export_asset_single_file(path):
    selection = cmds.ls(sl=True)[0]
    path = f'{path}/{selection}'
    export_asset_base(selection, path)

# Removes the maya folder from our path.
def get_parent_dir(path):
    split_path = path.split('/')
    split_path.pop()
    s = "/"
    return s.join(split_path)

# Gets the path to the assets folder, if we don't have one it creates it. 
def ensure_root_dir(asset_dir):
    root = get_parent_dir(cmds.workspace(q=True, act=True))
    project_path = f'{root}/{asset_dir}'

    if os.path.exists(project_path):
        return project_path
    else:
        om.MGlobal.displayWarning(f'No asset directory was found at "{root}", so created directory: "{asset_dir}" at path: "{project_path}"')
        os.mkdir(project_path)
        return project_path

if __name__ == '__main__':
    asset_dir_name = 'assets'
    export_asset_single_file(asset_dir_name)
