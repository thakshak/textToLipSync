# textToLipSync
animates a facial rig to show as if its speaking the entered text in Maya.

Used The CMU Pronouncing Dictionary from the following website for extracting phenomes from the entered text.
http://www.speech.cs.cmu.edu/cgi-bin/cmudict

Used the Mery character Rig from the following website.
https://www.meryproject.com/

#HOW TO USE IT.
-download mery rig from the above website.
-copy contents from script directory in this repo to your maya script directory.
-import rig it in maya.
-open maya's python script editor and enter the following commands

import mery_talks
reload(mery_talks)
mery_talks.runFacialExpressions()

enter words to see the rig talking.
