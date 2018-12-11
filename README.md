# GraphicsProject
Work in progress ...

A project that trains a CNN to predict joint locations.

Training data can be generated by running mayaGenDat.py in Maya (tested in Maya 2017). This script extracts joint pixel locations from your camera settings. In principle, it works with any vertex, not just joints.

## Instructions
Install Maya (ver. >= 2017)

Import an animated sequence with a 3D model into Maya. If you are interested in MikuMikuDance models, try MMD4Maya.

Position/animate your camera so that your 3D character shows up in your rendered image the way you like.

Copy and paste mayaGenDat.py into Maya command window, under python tab. Before executing, check the last line in file. In "extractJointsPx" call, you need to give the image vertical solution as well as the name of your camera.
