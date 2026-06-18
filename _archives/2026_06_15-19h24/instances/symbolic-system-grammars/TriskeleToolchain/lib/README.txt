SDL2 Native Libraries — Required for TriskeleToolchain
======================================================

SDL2.dll and SDL2.lib must be placed in this folder.

Source: SDL2 2.0.20 (Visual C++ build)
URL   : https://github.com/libsdl-org/SDL/releases/tag/release-2.0.20
File  : SDL2-devel-2.0.20-VC.zip

Steps:
  1. Download SDL2-devel-2.0.20-VC.zip
  2. Extract SDL2-devel-2.0.20-VC.zip
  3. Copy lib\x64\SDL2.dll  → TriskeleToolchain\lib\SDL2.dll
  4. Copy lib\x64\SDL2.lib  → TriskeleToolchain\lib\SDL2.lib

These files are required to build and run triskele-vm and wolf3d-demo.
