"""
This script serves as the main entry point for the Text-to-Lip-Sync tool in Maya.

It imports the main controller from the `lipsync` package and starts the
interactive session for the user.
"""
# Add the 'scripts' directory to the Python path to allow for package imports
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

# Import the controller from the lipsync package
from lipsync.controller import LipSyncController

def runFacialExpressions():
    """
    Creates a LipSyncController instance and starts an interactive session.
    This is the main entry point for the script in Maya.
    """
    try:
        # If the package was updated, we need to reload its modules deeply
        import lipsync.controller
        import lipsync.dictionary
        import lipsync.phonemes
        reload(lipsync.phonemes)
        reload(lipsync.dictionary)
        reload(lipsync.controller)
        
        # Re-import the controller after reloading
        from lipsync.controller import LipSyncController

    except (ImportError, NameError, AttributeError):
        # This will run on the first import
        from lipsync.controller import LipSyncController

    controller = LipSyncController()
    controller.run_interactive_session()

# Example of how to run it in Maya:
#
# import mery_talks
# reload(mery_talks)
# mery_talks.runFacialExpressions()
