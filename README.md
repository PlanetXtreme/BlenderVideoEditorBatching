Run files via the "Text Editor" in Blender. The scripts are run determined by what you have selected in the video editor.
The duplicate script allows you a variable to duplicate from.

This script is intended for testing frame blending capabilites in Blender: 
You should set the alpha of the image sequence (which is required to be placed in channel 1 in the video editor) to 1 divided by the number of duplications. This works similarly to After Effects Echo effect, but is not effective past 300 frames due to limitations with Blender, or some bug.
If past 127 duplications, nested sequences are automatically created in blender.
