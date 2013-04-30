#!/usr/bin/env python2
import SimpleCV as scv
import os, sys, time

camera_id = 0
cam = scv.Camera(camera_id)
picsdir = "data"
interval_seconds = 1

def mkdir(name):
    try: 
        os.mkdir(name)
    except OSError:
        pass

def setup():
    mkdir(picsdir)

def take_pic(fname):
    img = cam.getImage()
    img.save(fname)

def shoot_user(npics, name):
    mkdir("{0}/{1}".format(picsdir,name))
    n = 0
    n_taken = 0
    while n_taken < npics:
        fname = "{0}/{1}/{2}.jpg".format(picsdir, name, str(n).zfill(4))
        if not os.path.exists(fname):
            print('taking pic number {0}'.format(n_taken + 1))
            take_pic(fname)
            n_taken += 1
            time.sleep(interval_seconds)
        n += 1

def main():
    setup()
    print cam.getAllProperties()
    while True:
        print("Enter name of suspect and press enter.")
        name = raw_input()
        shoot_user(10, name)

if __name__ == "__main__":
    main()
