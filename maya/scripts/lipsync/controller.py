import maya.cmds as cmds
import os
from .phonemes import PHONEME_MAP
from .dictionary import load_phenome_dict

class LipSyncController:
    """
    Controls a facial rig in Maya to animate lip sync from text.
    """
    FRAME_DURATION = 8

    def __init__(self):
        self.controls = {
            'leftEyeLid': 'Mery_ac_lf_supfLid_move_sg',
            'rightEyeLid': 'Mery_ac_rg_supfLid_move_sg',
            'mouthInOut': 'Mery_ac_cn_inout_mouth',
            'jaw': 'Mery_ac_cn_jaw_control',
            'lipLeftCorner1': 'Mery_ac_lf_tinyCorner_control',
            'lipRightCorner1': 'Mery_ac_rg_tinyCorner_control',
            'lipLeftCorner2': 'Mery_ac_lf_corner_control',
            'lipRightCorner2': 'Mery_ac_rg_corner_control',
            'upperLip1': 'Mery_ac_upLip_01_control',
            'upperLip2': 'Mery_ac_upLip_02_control',
            'upperLip3': 'Mery_ac_upLip_03_control',
            'upperLip4': 'Mery_ac_upLip_04_control',
            'upperLip5': 'Mery_ac_upLip_05_control',
            'lowerLip1': 'Mery_ac_loLip_01_control',
            'lowerLip2': 'Mery_ac_loLip_02_control',
            'lowerLip3': 'Mery_ac_loLip_03_control',
            'lowerLip4': 'Mery_ac_loLip_04_control',
            'lowerLip5': 'Mery_ac_loLip_05_control',
            'stickLipsLeft': 'Mery_ac_lf_stickyLips_control',
            'stickLipsRight': 'Mery_ac_rg_stickyLips_control',
            'upperLipInOutLeft': 'Mery_ac_up_lf_lip_inout',
            'upperLipInOutRight': 'Mery_ac_up_rg_lip_inout',
            'lowerLipInOutLeft': 'Mery_ac_dw_lf_lip_inout',
            'lowerLipInOutRight': 'Mery_ac_dw_rg_lip_inout',
            'mouthMove': 'Mery_ac_cn_mouth_move',
            'tongue': ['Mery_ac_cn_tongue1', 'Mery_ac_cn_tongue2', 'Mery_ac_cn_tongue3', 'Mery_ac_cn_tongue4']
        }
        self.phoneme_map = PHONEME_MAP
        self.phenome_dict = load_phenome_dict()

    def _set_keyframe(self, control, attr, value, frame):
        """Sets a keyframe on a control attribute if it exists."""
        full_attr = "{}.{}".format(control, attr)
        if cmds.objExists(control) and cmds.attributeQuery(attr, node=control, exists=True):
            cmds.setKeyframe(full_attr, value=value, time=frame)
        else:
            cmds.warning("Attribute not found, skipping keyframe: {}".format(full_attr))

    def _set_tongue_rotation_keyframe(self, values, frame):
        """Sets keyframes for the tongue control rotations."""
        tongue_controls = self.controls['tongue']
        for i, value in enumerate(values):
            if i < len(tongue_controls):
                self._set_keyframe(tongue_controls[i], 'rotateZ', value, frame)

    def _set_tongue_translation_keyframe(self, attr, value, frame):
        """Sets a keyframe for the base of the tongue's translation."""
        tongue_base = self.controls['tongue'][0]
        self._set_keyframe(tongue_base, attr, value, frame)

    def reset_pose(self):
        """Resets all animated parts to their default positions."""
        for name, control in self.controls.items():
            if name == 'tongue':
                if cmds.objExists(control[0]):
                    cmds.setAttr(control[0] + '.translateX', 0.231)
                    cmds.setAttr(control[0] + '.translateY', 0.563)
                    cmds.setAttr(control[0] + '.translateZ', 0.014)
                for i in range(4):
                    if cmds.objExists(control[i]) and cmds.attributeQuery('rotateZ', node=control[i], exists=True):
                        cmds.setAttr(control[i] + '.rotateZ', 0)
            else:
                if cmds.objExists(control):
                    if cmds.attributeQuery('translateX', node=control, exists=True):
                        cmds.setAttr(control + '.translateX', 0)
                    if cmds.attributeQuery('translateY', node=control, exists=True):
                        cmds.setAttr(control + '.translateY', 0)

    def set_idle_keyframe(self, frame):
        """Sets a keyframe for the idle (neutral) pose."""
        for name, control in self.controls.items():
            if name == 'tongue':
                self._set_keyframe(control[0], 'translateX', 0.231, frame)
                self._set_keyframe(control[0], 'translateY', 0.563, frame)
                self._set_keyframe(control[0], 'translateZ', 0.014, frame)
                self._set_tongue_rotation_keyframe((0, 0, 0, 0), frame)
            else:
                self._set_keyframe(control, 'translateX', 0.0, frame)
                self._set_keyframe(control, 'translateY', 0.0, frame)
        return frame + self.FRAME_DURATION

    def set_ready_keyframe(self, frame):
        """Sets a keyframe for the current pose to transition from."""
        for name, control_name in self.controls.items():
            if name == 'tongue':
                t_controls = self.controls['tongue']
                if cmds.objExists(t_controls[0]):
                    for attr in ['translateX', 'translateY', 'translateZ']:
                        val = cmds.getAttr("{}.{}".format(t_controls[0], attr))
                        self._set_keyframe(t_controls[0], attr, val, frame)
                    rotations = [cmds.getAttr("{}.rotateZ".format(c)) for c in t_controls if cmds.objExists(c)]
                    self._set_tongue_rotation_keyframe(rotations, frame)
            else:
                if cmds.objExists(control_name):
                    translate = cmds.getAttr("{}.translate".format(control_name))[0]
                    self._set_keyframe(control_name, 'translateX', translate[0], frame)
                    self._set_keyframe(control_name, 'translateY', translate[1], frame)
        return frame

    def express_phoneme(self, phoneme, frame, stress):
        """Applies the facial expression for a given phoneme."""
        self.set_ready_keyframe(frame)

        phoneme_code = phoneme.strip('0123456789')
        expression_data = self.phoneme_map.get(phoneme_code)

        if not expression_data:
            cmds.warning("Phoneme '{}' not found in map.".format(phoneme_code))
            return frame + self.FRAME_DURATION - stress

        if isinstance(expression_data, str):
            expression_data = self.phoneme_map.get(expression_data, [])
        elif isinstance(expression_data, list) and expression_data and isinstance(expression_data[0], str):
            next_frame = frame
            for ph_alias in expression_data:
                next_frame = self.express_phoneme(ph_alias, next_frame, stress)
            return next_frame

        for data in expression_data:
            control_name, *rest = data

            if control_name == 'tongue_rotate':
                self._set_tongue_rotation_keyframe(rest[0], frame)
            elif control_name == 'tongue_translate':
                attr, value = rest[0]
                self._set_tongue_translation_keyframe(attr, value, frame)
            else:
                attr, value = rest
                control = self.controls.get(control_name)
                if control:
                    self._set_keyframe(control, attr, value, frame)

        return frame + self.FRAME_DURATION - stress

    def animate_text(self, text):
        """Animates the rig based on the input text."""
        if not self.phenome_dict:
            cmds.error("CMU dictionary not loaded. Cannot animate.")
            return

        words = text.upper().split()
        phonemes = []
        for word in words:
            if word in self.phenome_dict:
                phonemes.extend(self.phenome_dict[word])
            else:
                cmds.warning("Word '{}' not found in dictionary.".format(word))

        if not phonemes:
            cmds.warning("No phonemes found for the given text.")
            return

        self.reset_pose()
        frame = 0
        frame = self.set_idle_keyframe(frame)

        for ph in phonemes:
            print("Expressing: {}".format(ph))
            tmp = ph[-1:]
            stress_val = int(tmp) if tmp in ['0', '1', '2'] else 0
            stress_factor = 2 * (3 - stress_val)
            frame = self.express_phoneme(ph, frame, stress_factor)

        frame = self.set_idle_keyframe(frame)

        cmds.playbackOptions(animationStartTime=0, animationEndTime=frame, playbackSpeed=12)
        cmds.playblast(startTime=0, endTime=frame, format="image", compression="gif")
        if cmds.ls(type='animCurve'):
            cmds.cutKey(cmds.ls(type='animCurve'), time=(0, frame))
        print("Animation complete.")

    def run_interactive_session(self):
        """Starts an interactive session to animate text from user input."""
        cmds.setAttr(self.controls['leftEyeLid'] + '.translateY', 0.8)
        cmds.setAttr(self.controls['rightEyeLid'] + '.translateY', 0.8)

        while True:
            try:
                text_input = raw_input("Enter text to animate (or 'quit' to exit): ")
                if text_input.lower() == 'quit':
                    break
                if text_input:
                    self.animate_text(text_input)
            except EOFError:
                break
            except Exception as e:
                print("An error occurred: {}".format(e))
                break
