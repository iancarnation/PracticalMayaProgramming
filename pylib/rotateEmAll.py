"""
Rotates all FBX models in current directory to Z +
Assumes each FBX contains only one mesh hierarchy
"""

import os
import pymel.core as pmc

def run():
    # get current working directory and create export folder
    cwd = os.getcwd()
    destination = os.path.join(cwd,"export")
    if not os.path.exists(destination):
        os.makedirs(destination)

    files = []
    for filename in os.listdir(cwd):
        if filename.endswith('.fbx'):
            files.append(filename)

    for fbx in files:
        _process(fbx)
        fbxName = os.path.basename(fbx)
        target = os.path.join(destination, fbxName)
        _export(target)
        pmc.newFile(force=True)


def _process(sourceFileName):
    pmc.mel.FBXImport(f=sourceFileName)

    meshes = pmc.ls(type='mesh')
    
    transforms = [m.getParent() for m in meshes]
    
    root = [t for t in transforms if t.getParent()==None][0]
    
    root.setRotation([0.0,180.0,0.0], space='world')
    
    root.select()
    pmc.makeIdentity(apply=True) # Freeze Transformations

def _export(targetFileName):
    """Export FBX in centimeters"""
    pmc.mel.eval('FBXResetExport')
    pmc.mel.eval('FBXExportConvertUnitString -cm')
    pmc.mel.FBXExport(f=targetFileName)



