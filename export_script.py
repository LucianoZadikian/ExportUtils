import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import os 

def export(export_type, asset_dir):
    if export_type == 'Single File': export_asset_single_file(asset_dir)
    if export_type == 'Multiple Files': export_asset_multiple_files(asset_dir)
    else: export_asset_multiple_folders(asset_dir)

def export_asset_base(asset, path):
    if not os.path.exists(path):
        os.mkdir(path)
    
    mel.eval(f'FBXExport -f "{path}/{asset}.fbx" -s')
    om.MGlobal.displayInfo(f'Exported {asset} to directory {path}.') # Success message

# Exports objects in our selection in different fbx files under the directory of the first selected
def export_asset_multiple_files(asset_dir_name):
    selection = cmds.ls(sl=True)
    path = f'{get_project_dir(asset_dir_name)}/{selection[0]}'
    for asset in selection:
        cmds.select(asset)
        export_asset_base(asset, path)
    cmds.select(selection) # Reselect original selection

# Exports objects in our selection in different folders. 
def export_asset_multiple_folders(asset_dir_name):
    selection = cmds.ls(sl=True)
    for asset in selection:
        path = f'{get_project_dir(asset_dir_name)}/{asset}'
        cmds.select(asset)
        export_asset_base(asset, path)
    cmds.select(selection) # Reselect original selection

def export_asset_single_file(asset_dir_name):
    selection = cmds.ls(sl=True)[0]
    path = f'{get_project_dir(asset_dir_name)}/{selection}'
    export_asset_base(selection,path)

# Removes the maya folder from our path.
def get_parent_dir():
    project_dir = cmds.workspace(q=True, act=True)
    split_path = project_dir.split('/')
    split_path.pop()
    s = "/"
    return s.join(split_path)

# Gets the path to the assets folder, if we don't have one it creates it. 
def get_project_dir(asset_dir):
    root = get_parent_dir()
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

# get the name of the selected object, make sure we have a mesh selected.
## pull project path with assets folder
#om.MGlobal.displayWarning('The selection contains objects other than meshes! Unwanted results may occur.')
# Export selected mesh in fbx format to a specified file path. 