# Text-to-Lip-Sync for Maya

This project provides a Python script for Autodesk Maya that animates a facial rig to simulate speech from text input. It uses the CMU Pronouncing Dictionary to convert words into phonemes and then maps those phonemes to facial poses, creating a basic but effective lip-sync animation.

## Features

*   **Text-Based Animation:** Simply type in words or sentences, and the script will generate a lip-sync animation on the Mery character rig.
*   **Phoneme-Based Posing:** Utilizes the CMU Pronouncing Dictionary for accurate phoneme-to-expression mapping.
*   **Interactive Workflow:** Run the script in Maya's script editor and interactively enter text to see the animation.
*   **Customizable:** The script is written in Python and can be easily modified to work with other rigs or to add more complex facial expressions.

## How it Works

The script works by taking a string of text as input and breaking it down into individual words. Each word is then looked up in the CMU Pronouncing Dictionary to find its corresponding sequence of phonemes.

For each phoneme, the script applies a pre-defined facial pose to the character rig by setting keyframes on various facial controls (e.g., jaw, lips, tongue). The result is a sequence of facial animations that approximates the look of real speech.

## Dependencies

Before using the script, you will need the following:

1.  **Autodesk Maya:** The script is designed to be run within Maya's Python environment.
2.  **Mery Character Rig:** This script is specifically tailored to the "Mery" character rig. You can download it for free from the official website:
    *   [www.meryproject.com](https://www.meryproject.com/)
3.  **CMU Pronouncing Dictionary:** The dictionary files are included in this repository under `maya/scripts/cmudict/`. No separate download is necessary.

## Installation and Usage

Follow these steps to get the lip-sync script running in Maya:

1.  **Download the Mery Rig:** If you haven't already, download the Mery rig from [www.meryproject.com](https://www.meryproject.com/) and import it into your Maya scene.

2.  **Copy the Scripts:**
    *   Locate your Maya scripts directory. This is typically found in:
        *   **Windows:** `C:\\Users\\<YourUsername>\\Documents\\maya\\scripts`
        *   **macOS:** `/Users/<YourUsername>/Library/Preferences/Autodesk/maya/scripts`
        *   **Linux:** `~/maya/scripts`
    *   Copy the `mery_talks.py` file, the `cmudict` directory, and the `lipsync` package directory from this repository's `maya/scripts/` folder into your Maya scripts directory. Your scripts folder should look like this:
        ```
        <maya_scripts_folder>/
        ├── mery_talks.py
        ├── cmudict/
        │   └── ...
        └── lipsync/
            └── ...
        ```

3.  **Run in Maya:**
    *   Open Maya and load the scene with the Mery rig.
    *   Open the Python Script Editor (`Windows -> General Editors -> Script Editor`).
    *   In the Python tab, enter the following commands:

    ```python
    import mery_talks
    reload(mery_talks) # Use reload to pick up any changes if you edit the script
    mery_talks.runFacialExpressions()
    ```

4.  **Animate!**
    *   After running the commands, the script editor's input field will prompt you to "Enter text to animate".
    *   Type a word or sentence and press Enter.
    *   The script will generate the lip-sync animation on the timeline and create a playblast preview.

## Credits

*   **Mery Character Rig:** Created by the Mery Project. All rights and credits go to them.
*   **CMU Pronouncing Dictionary:** A public domain resource created by Carnegie Mellon University. [http://www.speech.cs.cmu.edu/cgi-bin/cmudict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict)
