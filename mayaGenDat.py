import maya.cmds as cmds
import math
import json
import os
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
def extractJointsPx(camname, joint_names, getJointCoord, outfile='', image_height=0, image_width=0, startFrame=0, endFrame=0, everyXFrames=1):
    if (image_height==0) or (image_width==0):
        print("Please enter image height and width in pixels")
        return
    image_ar = float(image_width) / float(image_height)
    dictionary = {}
    for i in range(startFrame,endFrame+1,everyXFrames):
        # sets frame number
        cmds.currentTime(i)
        print("Frame: %d"%(i))
        frame_num = i
        if outfile != '':
            # with open(outfile, 'a+') as file:
            #     file.write('%d' % i)
            #     file.write('\n')
            print()
        # camera parameters
        camcoord = cmds.camera(camname, position=True, query=True)
        camrots = cmds.camera(camname, query=True, rotation=True)
        hangle = cmds.camera(camname, horizontalFieldOfView=True, query=True)
        vangle = cmds.camera(camname, verticalFieldOfView=True, query=True)
        # aspect ratio
        ar = math.tan(math.radians(hangle/2)) / math.tan(math.radians(vangle/2))
        ncp = cmds.camera(camname, nearClipPlane=True, query=True)
        scale = cmds.camera(camname, cameraScale=True, query=True)
        if scale != 1:
            ncp = ncp/scale
            hangle = 2*math.degrees(math.atan(scale*math.tan(math.radians(hangle/2))))
            vangle = 2*math.degrees(math.atan(scale*math.tan(math.radians(vangle/2))))

        camdir = rotxyz([0,0,-1],camrots)    # camera started out pointing in negative z direction
        camup  = rotxyz([0,1,0],camrots)    # camera started out standing up
        # find 4 corners of canvas
        corners = ncpCorners(ncp, hangle, vangle, camdir, camup, camcoord)
        ul = corners['ul']
        ur = corners['ur']
        ll = corners['ll']
        lr = corners['lr']

        fitResolutionGate = cmds.camera(camname, query=True, filmFit=True)
        if fitResolutionGate == 'fill':
            if image_ar <= ar:
                fitResolutionGate = 'vertical'
            else:
                fitResolutionGate = 'horizontal'
        joints_framei = {}
        for jn in joint_names:
            # read world coordinates
            fucn = (lambda: cmds.joint(getJointCoord[jn],position=True,query=True))
            joints_framei[jn] = fucn()
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
            px = 0
            py = 0
            if fitResolutionGate == 'vertical':
                x_fraction = (ncpRayvec[0]*ncpXvec[0]+ncpRayvec[1]*ncpXvec[1]+ncpRayvec[2]*ncpXvec[2])/ncpWidth
                px = image_width*(0.5+(x_fraction-0.5)*ar/image_ar)
                py = image_height*(ncpRayvec[0]*ncpYvec[0]+ncpRayvec[1]*ncpYvec[1]+ncpRayvec[2]*ncpYvec[2])/ncpHeight
            elif fitResolutionGate == 'horizontal':
                px = image_width*(ncpRayvec[0]*ncpXvec[0]+ncpRayvec[1]*ncpXvec[1]+ncpRayvec[2]*ncpXvec[2])/ncpWidth
                y_fraction = (ncpRayvec[0]*ncpYvec[0]+ncpRayvec[1]*ncpYvec[1]+ncpRayvec[2]*ncpYvec[2])/ncpHeight
                py = image_height*(0.5+(y_fraction-0.5)*image_ar/ar)
            print('Joint %s has pixel location x=%d and y=%d'%(jn,int(round(px)),int(round(py))))
            joint_name = jn
            dictionary[(frame_num, joint_name)] = [int(round(px)),  int(round(py))]
            if outfile != '':
                # with open(outfile, 'a+') as file:
                #     file.write('%s:%d,%d' % (jn,px,py))
                #     file.write('\n')
                print()
    return dictionary

## ================= Model Information ======================= ##
# see credits.md for model credits

# tda_out_of_the_gravity_miku_v1 by chocofudge98
joint_names_anime = ['body_upper','neck','head','arm_left',
'elbow_left','wrist_left','thumb_left','arm_right','elbow_right','wrist_right',
'thumb_right','leg_left','knee_left','ankle_left', 'leg_right',
'knee_right','ankle_right']
joint_names_model = ['Torso', 'Neck', 'Head', 'LeftArm', 'LeftElbow', 'LeftWrist', 'LeftThumb0M',
'RightArm', 'RightElbow', 'RightWrist', 'RightThumb0M', 'LeftHip', 'LeftKnee', 'LeftFoot', 'RightHip',
'RightKnee', 'RightFoot']
for i in range(len(joint_names_model)):
    joint_names_model[i] = cmds.ls('*'+joint_names_model[i]+'*')[0]

getJointCoord_anime = {}

for j in range(len(joint_names_anime)):
    val = joint_names_model[j]
    getJointCoord_anime[joint_names_anime[j]] = val

camname = 'persp'
# prints joint pixel locations to console
# position your camera properly before calling
# make sure to give the right resln_h (picture height in pixels)
start_frame = 505
end_frame = 508
frame_per_img = 1
img_height = 512
img_width = 512
frame_padding = 4
dictionary = extractJointsPx(camname, joint_names_anime, getJointCoord_anime, '', 
image_height=img_height, 
image_width=img_width, 
startFrame=start_frame, 
endFrame=end_frame, 
everyXFrames=frame_per_img)
json_list = []
project_name = 'Miku_Hatsune+Bad_Romance' # file path to the rendered img folder (i.e. model name + vmd name)
for i in range(start_frame, end_frame+1, frame_per_img):
    json_obj = {}
    json_obj['isValidation'] = 0.0
    json_obj['joint_others'] = {"_ArrayType_": "double", "_ArraySize_": [0, 0], "_ArrayData_": None}
    json_obj['people_index'] = 1.0
    json_obj['scale_provided'] = img_height/200.0
    json_obj['joint_self'] = [0] * 16
    json_obj['joint_self'][0] = dictionary[(i, 'ankle_right')]
    json_obj['joint_self'][1] = dictionary[(i, 'knee_right')]
    json_obj['joint_self'][2] = dictionary[(i, 'leg_right')]
    json_obj['joint_self'][3] = dictionary[(i, 'leg_left')]
    json_obj['joint_self'][4] = dictionary[(i, 'knee_left')]
    json_obj['joint_self'][5] = dictionary[(i, 'ankle_left')]
    json_obj['joint_self'][6] = [(dictionary[(i, 'leg_right')][0] + dictionary[(i, 'leg_left')][0])/2,
    (dictionary[(i, 'leg_right')][1] + dictionary[(i, 'leg_left')][1])/2]
    json_obj['joint_self'][7] = dictionary[(i, 'body_upper')]
    json_obj['joint_self'][8] = dictionary[(i, 'neck')]
    json_obj['joint_self'][9] = dictionary[(i, 'head')]
    json_obj['joint_self'][10] = dictionary[(i, 'wrist_right')]
    json_obj['joint_self'][11] = dictionary[(i, 'elbow_right')]
    json_obj['joint_self'][12] = dictionary[(i, 'arm_right')]
    json_obj['joint_self'][13] = dictionary[(i, 'arm_left')]
    json_obj['joint_self'][14] = dictionary[(i, 'elbow_left')]
    json_obj['objpos_other'] = {"_ArrayType_": "double", "_ArraySize_": [0, 0], "_ArrayData_": None}
    json_obj['img_width'] = img_width
    json_obj['dataset'] = "Synthetic"
    json_obj['img_height'] = img_height
    json_obj['objpos'] = dictionary[(i, 'body_upper')]
    json_obj['scale_provided_other'] = {"_ArrayType_": "double", "_ArraySize_": [0, 0], "_ArrayData_": None}
    json_obj['annolist_index'] = 0.0
    if len(str(i)) < frame_padding:
        json_obj['img_paths'] = project_name + '0' + str(i) +'.jpeg'
    else:
        json_obj['img_paths'] = project_name + str(i) +'.jpeg'
    json_obj['numOtherPeople'] = 0.0
    json_list.append(json_obj)

out_path = os.path.abspath('C:/Users/yhyma/Desktop/535 Synthetic/' + project_name + '.json')

with open( out_path, 'w') as outfile:
    json.dump(json_list, outfile)

