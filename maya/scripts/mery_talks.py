import maya.cmds as cmds
import sys
import os

leftEyeLid = 'Mery_ac_lf_supfLid_move_sg'
rightEyeLid = 'Mery_ac_rg_supfLid_move_sg'

mouthInOut = 'Mery_ac_cn_inout_mouth'

jaw = 'Mery_ac_cn_jaw_control'

lipLeftCorner1 = 'Mery_ac_lf_tinyCorner_control'
lipRightCorner1 = 'Mery_ac_rg_tinyCorner_control'
lipLeftCorner2 = 'Mery_ac_lf_corner_control'
lipRightCorner2 = 'Mery_ac_rg_corner_control'

upperLip1 = 'Mery_ac_upLip_01_control'
upperLip2 = 'Mery_ac_upLip_02_control'
upperLip3 = 'Mery_ac_upLip_03_control'
upperLip4 = 'Mery_ac_upLip_04_control'
upperLip5 = 'Mery_ac_upLip_05_control'

lowerLip1 = 'Mery_ac_loLip_01_control'
lowerLip2 = 'Mery_ac_loLip_02_control'
lowerLip3 = 'Mery_ac_loLip_03_control'
lowerLip4 = 'Mery_ac_loLip_04_control'
lowerLip5 = 'Mery_ac_loLip_05_control'

stickLipsLeft = 'Mery_ac_lf_stickyLips_control'
stickLipsRight = 'Mery_ac_rg_stickyLips_control'

upperLipInOutLeft = 'Mery_ac_up_lf_lip_inout'
upperLipInOutRight = 'Mery_ac_up_rg_lip_inout'

lowerLipInOutLeft = 'Mery_ac_dw_lf_lip_inout'
lowerLipInOutRight = 'Mery_ac_dw_rg_lip_inout'

mouthMove='Mery_ac_cn_mouth_move'

tongue = ['Mery_ac_cn_tongue1','Mery_ac_cn_tongue2','Mery_ac_cn_tongue3','Mery_ac_cn_tongue4']
parts = [mouthInOut,tongue,jaw,lipLeftCorner1,lipRightCorner1,lipLeftCorner2,lipRightCorner2,upperLip1,upperLip2,upperLip3,upperLip4,upperLip5,lowerLip1,lowerLip2,lowerLip3,lowerLip4,lowerLip5,stickLipsLeft,stickLipsRight,upperLipInOutLeft,upperLipInOutRight,lowerLipInOutLeft,lowerLipInOutRight,mouthMove]

df = 8

def resetParts():
    for part in parts:
        if part != tongue:
            try:
                cmds.setAttr(part + '.translateX', 0)
            except:
                pass
            try:
                cmds.setAttr(part + '.translateY', 0)
            except:
                pass
        else:
            cmds.setAttr(part[0]  + '.translateX', 0.231)
            cmds.setAttr(part[0]  + '.translateY', 0.563)
            cmds.setAttr(part[0]  + '.translateZ', 0.014)
            cmds.setAttr(part[0]  + '.rotateZ', 0)
            cmds.setAttr(part[1]  + '.rotateZ', 0)
            cmds.setAttr(part[2]  + '.rotateZ', 0)
            cmds.setAttr(part[3]  + '.rotateZ', 0)

def setPartKeyframe(obj,x,y,frame):
    try:
        cmds.setKeyframe(obj + '.translateX', value=x, time=frame)
    except:
        pass
    try:
        cmds.setKeyframe(obj + '.translateY', value=y, time=frame)
    except:
        pass

def setLiftTongueFrame(t1,t2,t3,t4,frame):
    cmds.setKeyframe(tongue[0] + '.rotateZ', value = t1, time=frame)
    cmds.setKeyframe(tongue[1] + '.rotateZ', value = t2, time=frame)
    cmds.setKeyframe(tongue[2] + '.rotateZ', value = t3, time=frame)
    cmds.setKeyframe(tongue[3] + '.rotateZ', value = t4, time=frame)
    return frame + df

def setPartsToIdle(frame):
    for obj in parts:
        if obj != tongue:
            setPartKeyframe(obj,0.0,0.0,frame)
        else:
            cmds.setKeyframe(obj[0] + '.translateX', value=0.231, time=frame)
            cmds.setKeyframe(obj[0] + '.translateY', value=0.563, time=frame)
            cmds.setKeyframe(obj[0] + '.translateZ', value=0.014, time=frame)
            setLiftTongueFrame(0,0,0,0,frame)
    return frame + df

def setPartsToReady(frame):
    for obj in parts:
        
        if obj != tongue:
            [(x,y,z)]=cmds.getAttr( obj+".translate")
            setPartKeyframe(obj,x,y,frame)
        else:
            [(x,y,z)]=cmds.getAttr( obj[0] + ".translate")
            try:
                cmds.setKeyframe(obj[0] + '.translateX', value=x, time=frame)
            except:
                pass
            try:
                cmds.setKeyframe(obj[0] + '.translateY', value=y, time=frame)
            except:
                pass
            try:
                cmds.setKeyframe(obj[0] + '.translateZ', value=z, time=frame)
            except:
                pass
            t0 = cmds.getAttr(tongue[0] + '.rotateZ')
            t1 = cmds.getAttr(tongue[1] + '.rotateZ')
            t2 = cmds.getAttr(tongue[2] + '.rotateZ')
            t3 = cmds.getAttr(tongue[3] + '.rotateZ')
            setLiftTongueFrame(t0,t1,t2,t3,frame)
    return frame

def AA(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,0.7,0.0,frame)
    setPartKeyframe(lipLeftCorner2,0.7,0.0,frame)
    setPartKeyframe(jaw,0.0,-0.7,frame)
    return frame + df - stress

def AE(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(jaw,0.0,-0.5,frame)
    return frame + df - stress

def AH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(jaw,0.0,-0.4,frame)
    return frame + df - stress

def AO(frame, stress):
    return AA(frame, stress)
def AW(frame, stress):
    #AO+OW
    return UW(AO(frame, stress), stress)
def AY(frame, stress):
    #AH+Y
    return Y(AH(frame, stress), stress)
def B(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,0.1,0.0,frame)
    setPartKeyframe(lipLeftCorner2,0.1,0.0,frame)
    setPartKeyframe(stickLipsLeft,0.0,1.0,frame)
    setPartKeyframe(stickLipsRight,0.0,1.0,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def CH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,0.3,0.0,frame)
    setPartKeyframe(lipLeftCorner2,0.3,0.0,frame)
    setPartKeyframe(upperLip4,0.0,0.2,frame)
    setPartKeyframe(lowerLip4,0.0,0.1,frame)
    setPartKeyframe(upperLip2,0.0,0.2,frame)
    setPartKeyframe(lowerLip2,0.0,0.1,frame)
    setPartKeyframe(upperLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(upperLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(mouthInOut,0.0,1.0,frame)
    return frame + df - stress
def D(frame, stress):
    setPartsToReady(frame)
    setLiftTongueFrame(0,0,0,25,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def DH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(jaw,0.0,-0.2,frame)
    setPartKeyframe(tongue[0],0.250,0.600,frame)
    return frame + df - stress
def EH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(jaw,0.0,-0.3,frame)
    return frame + df - stress
def ER(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,0.2,0.0,frame)
    setPartKeyframe(lipLeftCorner2,0.2,0.0,frame)
    setPartKeyframe(upperLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(upperLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(mouthInOut,0.0,1.0,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def EY(frame, stress):
    return AE(frame, stress)
def F(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,-0.6,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,-0.6,frame)
    setPartKeyframe(jaw,0.0,-0.15,frame)
    return frame + df - stress
def G(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def HH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,0.3,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,0.3,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def IH(frame, stress):
    return HH(frame, stress)
def IY(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(tongue[0],0.0,0.0,frame)
    setLiftTongueFrame(0,0,0,0,frame)
    setPartKeyframe(lipRightCorner2,-0.2,0.0,frame)
    setPartKeyframe(lipLeftCorner2,-0.2,0.0,frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def JH(frame, stress):
    return CH(frame, stress)
def K(frame, stress):
    return G(frame, stress)
def L(frame, stress):
    return D(frame, stress)
def M(frame, stress):
    return B(frame, stress)
def N(frame, stress):
    return D(frame, stress)
def NG(frame, stress):
    return G(N(frame, stress), stress)
def OW(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,0.9,0.0,frame)
    setPartKeyframe(lipLeftCorner2,0.9,0.0,frame)
    setPartKeyframe(jaw,0.0,-0.5,frame)
    setPartKeyframe(mouthInOut,0.0,0.25,frame)
    setPartKeyframe(upperLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutLeft,0.0,1.0,frame)
    setPartKeyframe(upperLipInOutRight,0.0,1.0,frame)
    setPartKeyframe(lowerLipInOutRight,0.0,1.0,frame)
    return frame + df - stress
def OY(frame, stress):
    return Y(AO(frame, stress), stress)
def P(frame, stress):
    return B(frame, stress)
def R(frame, stress):
    return D(frame, stress)
def S(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,-0.3,0.0,frame)
    setPartKeyframe(lipLeftCorner2,-0.3,0.0,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def SH(frame, stress):
    return CH(frame, stress)
def T(frame, stress):
    return D(frame, stress)
def TH(frame, stress):
    return DH(frame, stress)
def UH(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,1,0.0,frame)
    setPartKeyframe(lipLeftCorner2,1,0.0,frame)
    setPartKeyframe(mouthInOut,0.0,0.1,frame)
    setPartKeyframe(jaw,0.0,-0.3,frame)
    return frame + df - stress
def UW(frame, stress):
    return UH(frame, stress)
def V(frame, stress):
    return F(frame, stress)
def W(frame, stress):
    return F(frame, stress)
def Y(frame, stress):
    setPartsToReady(frame)
    setPartKeyframe(lipRightCorner2,-0.1,0.0,frame)
    setPartKeyframe(lipLeftCorner2,-0.1,0.0,frame)
    setPartKeyframe(jaw,0.0,-0.1,frame)
    return frame + df - stress
def Z(frame, stress):
    return S(frame, stress)
def ZH(frame, stress):
    return CH(frame, stress)


def express(ph,frame):
    tmp = ph[-1:]
    stress = int(tmp) if tmp in ['0','1','2'] else 0 
    phenomes = {
        'AA' : AA,
        'AA0' : AA,
        'AA1' : AA,
        'AA2' : AA,
        'AE' : AE,
        'AE0' : AE,
        'AE1' : AE,
        'AE2' : AE,
        'AH' : AH,
        'AH0' : AH,
        'AH1' : AH,
        'AH2' : AH,
        'AO' : AO,
        'AO0' : AO,
        'AO1' : AO,
        'AO2' : AO,
        'AW' : AW,
        'AW0' : AW,
        'AW1' : AW,
        'AW2' : AW,
        'AY' : AY,
        'AY0' : AY,
        'AY1' : AY,
        'AY2' : AY,
        'B' : B,
        'CH' : CH,
        'D' : D,
        'DH' : DH,
        'EH' : EH,
        'EH0' : EH,
        'EH1' : EH,
        'EH2' : EH,
        'ER' : ER,
        'ER0' : ER,
        'ER1' : ER,
        'ER2' : ER,
        'EY' : EY,
        'EY0' : EY,
        'EY1' : EY,
        'EY2' : EY,
        'F' : F,
        'G' : G,
        'HH' : HH,
        'IH' : IH,
        'IH0' : IH,
        'IH1' : IH,
        'IH2' : IH,
        'IY' : IY,
        'IY0' : IY,
        'IY1' : IY,
        'IY2' : IY,
        'JH' : JH,
        'K' : K,
        'L' : L,
        'M' : M,
        'N' : N,
        'NG' : NG,
        'OW' : OW,
        'OW0' : OW,
        'OW1' : OW,
        'OW2' : OW,
        'OY' : OY,
        'OY0' : OY,
        'OY1' : OY,
        'OY2' : OY,
        'P' : P,
        'R' : R,
        'S' : S,
        'SH' : SH,
        'T' : T,
        'TH' : TH,
        'UH' : UH,
        'UH0' : UH,
        'UH1' : UH,
        'UH2' : UH,
        'UW' : UW,
        'UW0' : UW,
        'UW1' : UW,
        'UW2' : UW,
        'V' : V,
        'W' : W,
        'Y' : Y,
        'Z' : Z,
        'ZH' : ZH
    }
    f = phenomes.get(ph)(frame, 2*(3 - stress))
    return f

def load_phenome_dict(filename):
    lines={}
    with open(filename,"r") as f:
        for line in f:
            temp = line.strip().split()
            lines[temp[0]] = temp[1:]
    return lines

def runFacialExpressions():
    #Open Eyes
    cmds.setAttr(leftEyeLid + '.translateX', 0)
    cmds.setAttr(leftEyeLid + '.translateY', 0.8)
    cmds.setAttr(rightEyeLid + '.translateX', 0)
    cmds.setAttr(rightEyeLid + '.translateY', 0.8)
    #audioLoc = 'C:\\Users\\gthak\\OneDrive\\Documents\\maya\\mery\\temp.mp3'
    base = os.path.dirname(os.path.abspath(__file__)) #"C:\\Users\\gthak\\OneDrive\\Documents\\maya\\mery\\"
    print base
    phenome_dict = load_phenome_dict(base+"\\cmudict\\cmudict-0.7b.txt")
    while(True):
        str = raw_input()
        str = str.strip()
        #os.system('gtts-cli '+str+' -l "en" -o '+audioLoc)
        resetParts()
        frame = 0
        frame = setPartsToIdle(frame)
        for x in phenome_dict[str.upper()]:
            print x,
            frame = express(x,frame)
        print ''
        frame = setPartsToIdle(frame)
        cmds.playbackOptions(animationStartTime=0, animationEndTime=frame, playbackSpeed=12)
        #cmds.playblast(  sound = audioLoc, format="movie", compression="" )
        cmds.playblast(startTime=0, endTime=frame, format="image", compression="gif" )
        cmds.cutKey( cmds.ls(), time=(0,frame) )