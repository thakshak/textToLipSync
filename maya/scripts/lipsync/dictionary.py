"""
This module handles loading the CMU pronouncing dictionary.
"""
import os
import maya.cmds as cmds

def load_phenome_dict():
    """Loads the CMU pronouncing dictionary."""
    # This script is in maya/scripts/lipsync, so we need to go up two levels
    # to get to the maya/scripts directory where cmudict is located.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # base_dir is lipsync, parent is scripts.
    scripts_dir = os.path.dirname(base_dir)
    dict_path = os.path.join(scripts_dir, 'cmudict', 'cmudict-0.7b.txt')

    lines = {}
    try:
        with open(dict_path, "r") as f:
            for line in f:
                if not line.startswith(";;;"):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        lines[parts[0]] = parts[1:]
    except IOError as e:
        cmds.warning("Could not load CMU dictionary: {}".format(e))
        return None
    return lines
