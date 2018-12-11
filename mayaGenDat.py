import maya.cmds as cmds
import math

## ================= Utility functions ========================== ##
# ----------------- rotate vecter in order xyz ------------------ #
def rotxyz(vec,thetas):
    v = rotx(vec,thetas[0])
    v = roty(v,thetas[1])
    v = rotz(v,thetas[2])
    return v

def rotx(vec,theta):
    rad = math.radians(theta)
    y = vec[1]
    z = vec[2]
    y1 = [y*math.cos(rad),y*math.sin(rad)]
    z1 = [-z*math.sin(rad), z*math.cos(rad)]
    return [vec[0],y1[0]+z1[0],y1[1]+z1[1]]

def roty(vec,theta):
    rad = math.radians(theta)
    z = vec[2]
    x = vec[0]
    z1 = [z*math.cos(rad),z*math.sin(rad)]
    x1 = [-x*math.sin(rad), x*math.cos(rad)]
    return [z1[1]+x1[1],vec[1],z1[0]+x1[0]]

def rotz(vec,theta):
    rad = math.radians(theta)
    x = vec[0]
    y = vec[1]
    x1 = [x*math.cos(rad),x*math.sin(rad)]
    y1 = [-y*math.sin(rad), y*math.cos(rad)]
    return [x1[0]+y1[0],x1[1]+y1[1],vec[2]]

# tests
testv = rotxyz([1,0,0],[27.9,90,40])
assert(math.fabs(testv[0]-0)<1e-10)
assert(math.fabs(testv[1]-0)<1e-10)
assert(math.fabs(testv[2]+1)<1e-10)
testv = rotxyz([0,math.sqrt(2),0],[45,-90,-90])
assert(math.fabs(testv[0]-1)<1e-10)
assert(math.fabs(testv[1]-1)<1e-10)
assert(math.fabs(testv[2]-0)<1e-10)
testv = rotxyz([0,0,math.sqrt(2)],[45,90,45])
assert(math.fabs(testv[0]-math.sqrt(2))<1e-10)
assert(math.fabs(testv[1]-0)<1e-10)
assert(math.fabs(testv[2]-0)<1e-10)
testv = rotxyz([1,0,0],[45,90,45])
assert(math.fabs(testv[0]-0)<1e-10)
assert(math.fabs(testv[1]-0)<1e-10)
assert(math.fabs(testv[2]+1)<1e-10)
testv = rotxyz([0,math.sqrt(2),0],[45,90,45])
assert(math.fabs(testv[0]-0)<1e-10)
assert(math.fabs(testv[1]-math.sqrt(2))<1e-10)
assert(math.fabs(testv[2]-0)<1e-10)
testv = rotxyz([1,math.sqrt(2),math.sqrt(2)],[45,90,45])
assert(math.fabs(testv[0]-math.sqrt(2))<1e-10)
assert(math.fabs(testv[1]-math.sqrt(2))<1e-10)
assert(math.fabs(testv[2]+1)<1e-10)

# ----------------- extract canvas corners ---------------------- #
# Inputs:
#   ncp     : distance to nearest clipping plane (nearClipPlane/what i call canvas)
#   ha      : horizontal view angle (degrees)
#   va      : vertiical view angle (degrees)
#   camdir  : direction of sight, unit vector
#   camup   : up direction in camera frame, unit vector
#   camcoord: world coordinates of camera
# Outputs:
#   corners = {'ul': [x,y,z], 'ur':...}
#           : object with four corners (upper left, upper right, lower left, lower right)
def ncpCorners(ncp, ha, va, camdir, camup, camcoord):
    # validate Inputs
    camdirLen = math.sqrt(camdir[0]**2+camdir[1]**2+camdir[2]**2)
    camdir = [camdir[0]/camdirLen,camdir[1]/camdirLen,camdir[2]/camdirLen]
    camupLen  = math.sqrt(camup[0]**2+camup[1]**2+camup[2]**2)
    camup  = [camup[0]/camupLen,camup[1]/camupLen,camup[2]/camupLen]
    ncpHalfWidth = ncp * math.tan(math.radians(ha/2))
    ncpWidth  = 2 * ncpHalfWidth
    ncpHalfHeight = ncp * math.tan(math.radians(va/2))
    ncpHeight = 2 * ncpHalfHeight
    # x direction in camera frame is cross product: camdir x camup
    ncpXvec = [camdir[1]*camup[2]-camdir[2]*camup[1],camdir[2]*camup[0]-camdir[0]*camup[2],camdir[0]*camup[1]-camdir[1]*camup[0]]
    ncpYvec = camup
    # corners of nearClipPlane
    corners = {}
    corners['ul'] = [camcoord[0]+ncp*camdir[0]-ncpHalfWidth*ncpXvec[0]+ncpHalfHeight*ncpYvec[0],camcoord[1]+ncp*camdir[1]-ncpHalfWidth*ncpXvec[1]+ncpHalfHeight*ncpYvec[1],camcoord[2]+ncp*camdir[2]-ncpHalfWidth*ncpXvec[2]+ncpHalfHeight*ncpYvec[2]]
    corners['ur'] = [camcoord[0]+ncp*camdir[0]+ncpHalfWidth*ncpXvec[0]+ncpHalfHeight*ncpYvec[0],camcoord[1]+ncp*camdir[1]+ncpHalfWidth*ncpXvec[1]+ncpHalfHeight*ncpYvec[1],camcoord[2]+ncp*camdir[2]+ncpHalfWidth*ncpXvec[2]+ncpHalfHeight*ncpYvec[2]]
    corners['ll'] = [camcoord[0]+ncp*camdir[0]-ncpHalfWidth*ncpXvec[0]-ncpHalfHeight*ncpYvec[0],camcoord[1]+ncp*camdir[1]-ncpHalfWidth*ncpXvec[1]-ncpHalfHeight*ncpYvec[1],camcoord[2]+ncp*camdir[2]-ncpHalfWidth*ncpXvec[2]-ncpHalfHeight*ncpYvec[2]]
    corners['lr'] = [camcoord[0]+ncp*camdir[0]+ncpHalfWidth*ncpXvec[0]-ncpHalfHeight*ncpYvec[0],camcoord[1]+ncp*camdir[1]+ncpHalfWidth*ncpXvec[1]-ncpHalfHeight*ncpYvec[1],camcoord[2]+ncp*camdir[2]+ncpHalfWidth*ncpXvec[2]-ncpHalfHeight*ncpYvec[2]]
    return corners

# tests
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 90   # horizontal view angle (degrees)
va = 90      # vertiical view angle (degrees)
camdir = [0,0,-1]     # unit vector
camup  = [0,1,0]      # unit vector
camcoord = [0,0,0]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]+0.1) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-0.1) < 1e-10)
assert(math.fabs(testcorners['ul'][2]+0.1) < 1e-10)
ncp = 1    # distance to nearest clipping plane (nearClipPlane) *
ha = 90   # horizontal view angle (degrees)
va = 90      # vertiical view angle (degrees)
camdir = [0,0,-1]     # unit vector
camup  = [0,1,0]      # unit vector
camcoord = [0,0,0]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]+1) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-1) < 1e-10)
assert(math.fabs(testcorners['ul'][2]+1) < 1e-10)
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 90   # horizontal view angle (degrees)
va = 90      # vertiical view angle (degrees)
camdir = [0,0,-1]     # unit vector
camup  = [0,1,0]      # unit vector
camcoord = [5,10,-130]# *
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]+0.1-5) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-0.1-10) < 1e-10)
assert(math.fabs(testcorners['ul'][2]+0.1+130) < 1e-10)
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 90   # horizontal view angle (degrees) *
va = 60      # vertiical view angle (degrees)
camdir = [0,0,-1]     # unit vector
camup  = [0,1,0]      # unit vector
camcoord = [0,0,0]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]+0.1) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-0.1/math.sqrt(3)) < 1e-10)
assert(math.fabs(testcorners['ul'][2]+0.1) < 1e-10)
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 2*math.degrees(math.atan(2/math.sqrt(3)))   # horizontal view angle (degrees) *
va = 60      # vertiical view angle (degrees)  * (aspect ratio 1:2)
camdir = [0,0,-1]     # unit vector
camup  = [0,1,0]      # unit vector
camcoord = [0,0,0]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]+2*0.1/math.sqrt(3)) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-0.1/math.sqrt(3)) < 1e-10)
assert(math.fabs(testcorners['ul'][2]+0.1) < 1e-10)
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 90   # horizontal view angle (degrees)
va = 90      # vertiical view angle (degrees)
camdir = [1/math.sqrt(2),1/math.sqrt(2),0]     # unit vector *
camup  = [0,0,1]      # unit vector *
camcoord = [0,0,0]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
assert(math.fabs(testcorners['ul'][0]) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-0.1*math.sqrt(2)) < 1e-10)
assert(math.fabs(testcorners['ul'][2]-0.1) < 1e-10)
ncp = 0.1    # distance to nearest clipping plane (nearClipPlane)
ha = 90   # horizontal view angle (degrees) *
va = 60      # vertiical view angle (degrees)
thetas = [30,60,90]
camdir = rotxyz([0,0,-1],thetas)     # unit vector
camup  = rotxyz([0,1,0],thetas)      # unit vector
camcoord = [10,-20,30]
testcorners = ncpCorners(ncp, ha, va, camdir, camup, camcoord)
ul = rotxyz([-0.1,0.1/math.sqrt(3),-0.1],thetas)
assert(math.fabs(testcorners['ul'][0]-ul[0]-10) < 1e-10)
assert(math.fabs(testcorners['ul'][1]-ul[1]+20) < 1e-10)
assert(math.fabs(testcorners['ul'][2]-ul[2]-30) < 1e-10)

# ----------------- extract joint pixel locations ---------------------- #
def extractJointsPx(camname, joint_names, getJointCoord, resln_h=512, startFrame=1, endFrame=7800, everyXFrames=2000):
    camcoord = cmds.camera(camname, position=True, query=True)
    camrots = cmds.camera(camname, query=True, rotation=True)
    hangle = cmds.camera(camname, horizontalFieldOfView=True, query=True)
    vangle = cmds.camera(camname, verticalFieldOfView=True, query=True)
    # aspect ratio
    ar = math.tan(math.radians(hangle/2)) / math.tan(math.radians(vangle/2))
    # resln_h = 512    # in pixels
    resln_w = ar*resln_h
    ncp = cmds.camera(camname, nearClipPlane=True, query=True)

    camdir = rotxyz([0,0,-1],camrots)    # camera started out pointing in negative z direction
    camup  = rotxyz([0,1,0],camrots)    # camera started out standing up
    # find 4 corners of canvas
    corners = ncpCorners(ncp, hangle, vangle, camdir, camup, camcoord)
    ul = corners['ul']
    ur = corners['ur']
    ll = corners['ll']
    lr = corners['lr']
    # startFrame = 1
    # endFrame = 7800
    # everyXFrames = 2000

    for i in range(startFrame,endFrame+1,everyXFrames):
        # sets frame number
        cmds.currentTime(i)
        print("Frame: %d"%(i))

        joints_framei = {}
        for jn in joint_names:
            # read world coordinates
            joints_framei[jn] = getJointCoord[jn]()
            ptcoord = joints_framei[jn]
            # 'project' onto nearClipPlane (ncp)
            ray = [ptcoord[0]-camcoord[0], ptcoord[1]-camcoord[1], ptcoord[2]-camcoord[2]]
            s = ncp/(camdir[0]*ray[0]+camdir[1]*ray[1]+camdir[2]*ray[2])
            ray = [s*ray[0], s*ray[1], s*ray[2]]
            ncpWidth = ((ur[0]-ul[0])**2+(ur[1]-ul[1])**2+(ur[2]-ul[2])**2)**0.5
            ncpHeight = ((ur[0]-lr[0])**2+(ur[1]-lr[1])**2+(ur[2]-lr[2])**2)**0.5
            ncpXvec = [(ur[0]-ul[0])/ncpWidth,(ur[1]-ul[1])/ncpWidth,(ur[2]-ul[2])/ncpWidth]
            ncpYvec = [(lr[0]-ur[0])/ncpHeight,(lr[1]-ur[1])/ncpHeight,(lr[2]-ur[2])/ncpHeight]
            ncpRayvec = [camcoord[0]+ray[0]-ul[0],camcoord[1]+ray[1]-ul[1],camcoord[2]+ray[2]-ul[2]]
            px = resln_w*(ncpRayvec[0]*ncpXvec[0]+ncpRayvec[1]*ncpXvec[1]+ncpRayvec[2]*ncpXvec[2])/ncpWidth
            py = resln_h*(ncpRayvec[0]*ncpYvec[0]+ncpRayvec[1]*ncpYvec[1]+ncpRayvec[2]*ncpYvec[2])/ncpHeight
            print('Joint %s has pixel location x=%d and y=%d'%(jn,int(round(px)),int(round(py))))

## ================= END Utility functions ======================= ##




## ================= Model Information ======================= ##
# see credits.md for model credits

# tda_out_of_the_gravity_miku_v1 by chocofudge98
joint_names_anime = ['body_upper','neck','head','nose_tip','nose_root','arm_left','elbow_left','wrist_left','thumb_left','arm_right','elbow_right','wrist_right','thumb_right','leg_left','knee_left','ankle_left','tiptoe_left','leg_right','knee_right','ankle_right','tiptoe_right']
getJointCoord_anime = {}
getJointCoord_anime['body_upper'] = (lambda: cmds.joint('No_12_joint_Torso2',position=True,query=True))
getJointCoord_anime['neck'] = (lambda: cmds.joint('No_18_joint_Neck',position=True,query=True))
getJointCoord_anime['head'] = (lambda: cmds.joint('No_19_joint_Head',position=True,query=True))
getJointCoord_anime['nose_tip'] = (lambda: cmds.pointPosition('U_Char_1.vtx[298]'))
getJointCoord_anime['nose_root'] = (lambda: cmds.pointPosition('U_Char_1.vtx[274]'))
getJointCoord_anime['arm_left'] = (lambda: cmds.joint('No_61_joint_LeftArm',position=True,query=True))
getJointCoord_anime['elbow_left'] = (lambda: cmds.joint('No_68_joint_LeftElbow',position=True,query=True))
getJointCoord_anime['wrist_left'] = (lambda: cmds.joint('No_73_joint_LeftWrist',position=True,query=True))
getJointCoord_anime['thumb_left'] = (lambda: cmds.joint('No_306_i_joint_LeftThumb0M',position=True,query=True))
getJointCoord_anime['arm_right'] = (lambda: cmds.joint('No_23_joint_RightArm',position=True,query=True))
getJointCoord_anime['elbow_right'] = (lambda: cmds.joint('No_30_joint_RightElbow',position=True,query=True))
getJointCoord_anime['wrist_right'] = (lambda: cmds.joint('No_35_joint_RightWrist',position=True,query=True))
getJointCoord_anime['thumb_right'] = (lambda: cmds.joint('No_307_i_joint_RightThumb0M',position=True,query=True))
getJointCoord_anime['leg_left'] = (lambda: cmds.joint('No_106_joint_LeftHip',position=True,query=True))
getJointCoord_anime['knee_left'] = (lambda: cmds.joint('No_107_joint_LeftKnee',position=True,query=True))
getJointCoord_anime['ankle_left'] = (lambda: cmds.joint('No_108_joint_LeftFoot',position=True,query=True))
getJointCoord_anime['tiptoe_left'] = (lambda : cmds.pointPosition('U_Char_0.vtx[29091]'))
getJointCoord_anime['leg_right'] = (lambda: cmds.joint('No_102_joint_RightHip',position=True,query=True))
getJointCoord_anime['knee_right'] = (lambda: cmds.joint('No_103_joint_RightKnee',position=True,query=True))
getJointCoord_anime['ankle_right'] = (lambda: cmds.joint('No_104_joint_RightFoot',position=True,query=True))
getJointCoord_anime['tiptoe_right'] = (lambda: cmds.pointPosition('U_Char_0.vtx[28428]'))

# joint_names = ['tiptoe_left','tiptoe_right','knee_left','knee_right','elbow_right']
# getJointCoord = {}
# getJointCoord['tiptoe_left'] = (lambda : cmds.pointPosition('U_Char_0.vtx[29091]'))
# getJointCoord['tiptoe_right'] = (lambda: cmds.pointPosition('U_Char_0.vtx[28428]'))
# getJointCoord['knee_left'] = (lambda: [0.5*(cmds.pointPosition('U_Char_0.vtx[1207]')[0]+cmds.pointPosition('U_Char_0.vtx[1093]')[0]),0.5*(cmds.pointPosition('U_Char_0.vtx[1207]')[1]+cmds.pointPosition('U_Char_0.vtx[1093]')[1]),0.5*(cmds.pointPosition('U_Char_0.vtx[1207]')[2]+cmds.pointPosition('U_Char_0.vtx[1093]')[2])])
# getJointCoord['knee_right'] = (lambda: [0.5*(cmds.pointPosition('U_Char_0.vtx[2432]')[0]+cmds.pointPosition('U_Char_0.vtx[2474]')[0]),0.5*(cmds.pointPosition('U_Char_0.vtx[2432]')[1]+cmds.pointPosition('U_Char_0.vtx[2474]')[1]),0.5*(cmds.pointPosition('U_Char_0.vtx[2432]')[2]+cmds.pointPosition('U_Char_0.vtx[2474]')[2])])
# getJointCoord['elbow_right'] = (lambda: [0.5*(cmds.pointPosition('U_Char_0.vtx[3072]')[0]+cmds.pointPosition('U_Char_0.vtx[3118]')[0]),0.5*(cmds.pointPosition('U_Char_0.vtx[3072]')[1]+cmds.pointPosition('U_Char_0.vtx[3118]')[1]),0.5*(cmds.pointPosition('U_Char_0.vtx[3072]')[2]+cmds.pointPosition('U_Char_0.vtx[3118]')[2])])


camname = 'camera2'
# prints joint pixel locations to console
# position your camera properly before calling
# make sure to give the right resln_h (picture height in pixels)
extractJointsPx(camname, joint_names_anime, getJointCoord_anime, resln_h=512, startFrame=1, endFrame=7800, everyXFrames=2000)
