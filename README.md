# 3D-renderer-using-pygame
Learning the basics of 3D graphics and lighting using pygame.

This is not optimized for highpoly models and is purely made for learning about 3d rendering also triangulation is implemented in this project which is a rework of my last repo but by using pygame whis is a module specialized in 2d graphics.

To install pygame run the following command in the terminal/ cmd:
  
	pip install pygame

Also i tried implementing lighting in this project but it's not per pixel like most 3d renderers but it's per triangle, also texturing is not implemented in this version and the model is coloured in monochrome.

Every math operations in the project are taken care using the pyglm module including the matrix operations.

to install pyglm, run the following the command in the terminal/ cmd:

	pip install pyglm

Instructions:

  -use w, a, s, d keys for moving around the scene and spcebar, lshift for moving up or down
  
  -mouse controls supported for camera movement
  
  -About the models I used to test this:
  
	-cube = very low poly

	-astronaut = low poly

	-mountains = large model

	-teapot = hello world to 3d graphics testing

	-cat = high poly

  -To load your own models:

	-download them as a .obj file and place them in the models folder.

 	-change the model name in the main.py file and run it.

  References:

  https://youtu.be/ih20l3pJoeU?si=o02OevIxmKlqbKtd

  https://youtu.be/M_Hx0g5vFko?si=RQakbSVQ28MzHUu2
  
  https://www.youtube.com/watch?v=XgMWc6LumG4

  
