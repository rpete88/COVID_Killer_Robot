The contents of this file come from following
https://lemariva.com/blog/2020/01/maixpy-object-detector-mobilenet-and-yolov2-sipeed-maix-dock

kfpkg files are creating by zipping together the kmodel, json, and bin files
and then we must rename the zip to be kfpkg

____________________________________________________________
  kfpkg FILES - what we actually flash to board
____________________________________________________________

model_v0.5.1_nncasev2b2.kfpkg
  Converts from flite to kmodel using nncase v0.2.0 Beta2
  Problem: Unsuccessful load, same issue we have been getting
  ValueError: [MAIXPY]kpu: load error:2002, ERR_KMODEL_VERSION: only support kmodel V3/V4 now

model_v0.5.1_nncasev2b4.kfpkg
  Converts from flite to kmodel using nncase v0.2.0 Beta4
  Problem: Unsuccessful load, https://github.com/sipeed/MaixPy/issues/256, trying beta2 instead

model_v0.3.2.kfpkg
  Using desk.kmodel and firmware v0.3.2 (the latest full release of MaixPy)
  Problem: Firmware also doesn't support our camera

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
  Model for detecting desks using nncase v0.2.0 beta2
  This version of nncase is believed to give us kmodel v4, and is supported by MaixPy

deskv2beta4.kmodel
  Model for detecting desks using nncase v0.2.0 beta4
  This version of nncase is believed to give us kmodel v4

desk.kmodel
  Model for detecting desks using nncase v0.1.0-rc5

weights.kmodel
  A previous model for detecting desks


____________________________________________________________
  JSON FILES - used to flash the board with kflash
____________________________________________________________
flash-list_v5bin_v2beta4.json
  v0.5.1 of firmware with kmodel of nncasev0.2.0 beta 4

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
  MAY BE TOO LARGE IF THE KMODEL IS TOO LARGE

maixpy_v0.5.1_103_gf9bb0bb_minimum.bin
  maixpy minimum version 0.5.1
  MINIMUM VERSION DOES NOT INCLUDE IDE and PYE from terminal

maixpy_v0.4.0_52_g3b8c18b.bin
  maixpy previous version 0.4.0
  DOES NOT SUPPORT CAMERA

maixpy_v0.3.2_full.bin
  maixpy previous version (latest release) 0.3.2
  DOES NOT SUPPORT CAMERA
