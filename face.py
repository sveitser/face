#!/usr/bin/env python2
import SimpleCV as scv
import numpy as np
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
    img = prepare(cam.getImage())
    img.save(fname)

def save_raw(fname):
    cam.getImage().save(fname)

def find_face(img):
    for n in ["", "2", "3", "4"]:
        face = img.findHaarFeatures("face.xml")
        if len(face) == 1:
            img = face[0].crop()
            break
    return img

def find_eyes(img):
    try:
        re = img.findHaarFeatures("lefteye.xml")[0]
        le = img.findHaarFeatures("right_eye.xml")[0]
    except:
        return img
    lec = le.coordinates()
    rec = re.coordinates()
    print(lec, rec)
    angle = np.arctan(float(lec[1] - rec[1]) / (lec[0] - rec[0])) * 180 / np.pi
    center = (lec + rec) / 2.0
    return img.rotate(angle, point=center)

def prepare(img):
    img = find_face(img)
    img = find_eyes(img)
    img = find_face(img)
    return img.grayscale()

def shoot_user(npics, name):
    mkdir("{0}/{1}".format(picsdir,name))
    n = 0
    n_taken = 0
    while n_taken < npics:
        fname = "{0}/{1}/{2}.jpg".format(picsdir, name, str(n).zfill(4))
        if not os.path.exists(fname):
            print('taking pic number {0}'.format(n_taken + 1))
            save_raw(fname)
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
