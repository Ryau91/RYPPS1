# RYPPS1

## Introduction

My first game. This was created in python in about two weeks. I used the pygame module to make this game.

## Starting the game

You must have the pygame module installed for the game run. Once pygame is installed, download (and extract) all of the files and execute main.py to begin the game.

## Controls

Use number keys and ESC to navigate through the menus. controls.txt lists the controls for the actual game. To change the controls, read through controls.txt to find the desired keys for input and change accordingly.

Additional controls:\
M key: toggles the music on and off during the game\
F11: toggles fullscreen

## Modes

Classic: Endless. Aim for the highest score possible\
40 Lines: Aim to see how fast you can clear 40 lines\
Invisible: Classic but the pieces and locked positions are invisible. The ghost pieces remain visible.

## Piece sets

Regular: Tetrominoes\
Pentris: Pentominoes\
OLL: OLL inspired pieces that spawn with real OLL probabilities!\
Wacky: A set of 1000 wacky 1x2 - 3x4 pieces is generated with random colours every time using a basic algorithm that I designed. A new set with new colours is generated every time you play. You will probably never play with the same set twice!\

01/05/21 One third of the pieces of the wacky piece set are nice pieces to prolong games.

## Gameplay

Use your configured direction keys to move the pieces around. Rotate pieces when necessary and hard drop the piece if/when you want the current piece to drop down and immediately lock into place.
At the moment you cannot slide pieces horizontally, you must tap. The level advances by 1 after every 10 lines.
There is no lock delay nor new piece entry delay for 40 Lines mode.\

01/05/21 DAS (Delayed Auto Shift) has been implemented. Pieces move left and right smoothly.
