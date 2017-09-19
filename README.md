# ImageReplacer
Compares images in directories to see if they are similar

Usage:

Add the directories to compare in the config.cfg file.
Run python ImageReplacer.py

The script will hash all files in the source and target directories, one at a time. These hashes will be compared, and if similar (within a configurable tolerance), then they will be presented within a GUI. The accept button moves the source file over the target file, after backing up the target file. The quit button skips the pair of images.

Files that are exactly the same (as in the md5 hash matches for the image files) are skipped.
