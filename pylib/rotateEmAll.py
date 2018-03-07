# Rotates all FBX models in a directory to Z +
# Assumes FBX contains only one mesh hierarchy

import os
import subprocess
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
        process(fbx)
        fbxName = os.path.basename(fbx)
        target = os.path.join(destination, fbxName)
        export(target)
        pmc.newFile(force=True)


def process(sourceFileName):
    pmc.mel.FBXImport(f=sourceFileName)
    # Get meshes in scene
    meshes = pmc.ls(type='mesh')
    # Get Transforms (mesh Parents)
    transforms = [m.getParent() for m in meshes]
    # Find Root
    root = [t for t in transforms if t.getParent()==None][0]
    root.setRotation([0.0,180.0,0.0], space='world')
    root.select()
    ## Freeze Transformations
    pmc.makeIdentity(apply=True)

def export(targetFileName):
    """Export FBX in centimeters"""
    pmc.mel.eval('FBXResetExport')
    pmc.mel.eval('FBXExportConvertUnitString -cm')
    pmc.mel.FBXExport(f=targetFileName)



