# BossToneStudio
Scripts for Boss Tone Studio

boss_tsl.py

Prints the settings of a liveset that has been exported to a TSL file. 

Currently only livesets for the BOSS ME-80 are supported.

usage: boss_tsl.py [-h] [-L] filename [patch]

Print BOSS Tone Studio livesets. Requires Python 3.6+

positional arguments:
  filename          File name (*.tsl)
  patch             [Optional] Display only 1 patch which may have spaces in
                    the name

optional arguments:
  -h, --help        show this help message and exit
  -L, --patch_list  Display list of patches only
