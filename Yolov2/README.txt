The contents of this file come from following
https://lemariva.com/blog/2020/01/maixpy-object-detector-mobilenet-and-yolov2-sipeed-maix-dock

kfpkg files are creating by zipping together the kmodel, json, and bin files
and then we must rename the zip to be kfpkg

____________________________________________________________
  kfpkg FILES
____________________________________________________________

model_v0.3.2.kfpkg
  Using desk.kmodel and firmware v0.3.2 (the latest full release of MaixPy)
  Problem:

model_v0.4.0.kfpkg
  Using desk.kmodel and firmware v0.5.1
  Problem: Firmware seems to have an issue with sensor.reset() (on-board camera)
            Possible we have a different camera than this version is expecting

model_v0.5.1_minimum.kfpkg
  Using desk.kmodel and firmware v0.5.1 minimum
  Problem: Program gets hung up when attempting to load the mode
          Attempted this because this version takes up less space than v0.5.1
          However, lose IDE and python editor with minimum version, doesn't fix v0.5.1 issue

model_v0.5.1.kfpkg
  Using desk.kmodel and firmware v0.5.1
  Problem: Program gets hung up when attempting to load the model


____________________________________________________________
  kmodel FILES
____________________________________________________________
deskv2beta4.kmodel
  Model for detecting desks using nncase v0.2.0 beta4
  This version of nncase is believed to give us kmodel v4

desk.kmodel
  Model for detecting desks using nncase v0.1.0-rc5

weights.kmodel
  A previous model for detecting desks


____________________________________________________________
  JSON FILES
____________________________________________________________

flash-list_v0.3.2.json
  json file for minimum version of maixpy v0.3.2

flash-list_v0.5.1.json
  json file for full version of maixpy v0.5.1

flash-list_v0.5.1_minimum.json
  json file for minimum version of maixpy v0.5.1

flash-list_v0.4.0.json
  json file for minimum version of maixpy v0.4.0


____________________________________________________________
  BIN FILES - firmware versions
____________________________________________________________
maixpy_v0.5.1_103_gf9bb0bb.bin
  maixpy full version 0.5.1

maixpy_v0.5.1_103_gf9bb0bb_minimum.bin
  maixpy minimum version 0.5.1

maixpy_v0.4.0_52_g3b8c18b.bin
  maixpy previous version 0.4.0

maixpy_v0.3.2_full.bin
  maixpy previous version (latest release) 0.3.2
