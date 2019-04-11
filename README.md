# README

This is a FUN project that allows you to enter the world of HARRY POTTER.
Here u will be able to create a SCENE from the MOVIE and then assume the role
of Harry Potter. 

You will then be able to wear a RED CAPE that is magical... and if you hide under it
you will become invisible to anyone.... in the video feed.

The MAGIC of Invisibility that happens between when the CAMERA sees you and when it presents the same
video stream to the Display ..... is done using OPEN CV 2 Visual Coginition Libraries and the Python language.

There are 2 steps involved, the first is in Crafting the SCENE and the CAPE using this command
### python CreateMagicCape.py -f HSV --webcam
You have to make sure you have a bright location that is static with the scene you want. 
You have to choose a constrast color for your MAGIC CAPE that doesnt clash with the scene.
The best chance of Coginition is using the HUE, SATURATION and VALUE method of pixel identification
rather than the Red Blue Green values of the RGB. This is because the real world has shades and tones.


Then once you have done that you can run the magic of HARRY POTTER AND HIS INVISIBLE CAPE.using this command
### python HarryPotterMagic.py
Please make sure that for the MAGIC to work, the REAL world camera has to see the same scene that the SCENE and CAPE program SAW.


