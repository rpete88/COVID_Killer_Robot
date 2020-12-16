COVID_Killer_Robot Team
Senior Design - Fall 2020

Software Files
  autonomousDriving.py
      Controls servos and ultrasonic sensors to move robot
      Adjust pin numbers based on robot configuration

  deskDetection.py
      Uses camera to locate desks, puts rectangle around them
      Adjust location of kmodel based on where it is flashed/ or SD card path

  microservo_scan_code.py
      Moves on of the microservos on mini pan tilt kit about 180 degrees

  m.kmodel
      Model that is used to do perform image recognition

  maixpy_v0.5.1_103_gf9bb0bb.bin
      Firmware used during this semester
      version 0.6.0 has been released-- we will look into this version

  Training Folder - dataset for object detection 
    anns - annotations of our dataset
    imgs - images of our dataset
