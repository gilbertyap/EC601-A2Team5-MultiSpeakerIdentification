# USAGE
# python findMouthThresholdValue.py -v video.mp4
# or 
# python findMouthThresholdValue.py --video video.mp4

# import the necessary packages
from imutils.video import FileVideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import csv
import os, sys

def get_luminosity_of_masked_image(frame):
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # In the frame, there will be black pixels representing the masked portions, do not count those in the average
    luminosity = 0
    nonMaskPixels = 0
    luminosity = grayFrame.sum()
    nonMaskPixels = np.array(np.nonzero(grayFrame)).size
    # print('L: {}, Total: {}, Avg: {}'.format(luminosity, nonMaskPixels, round(luminosity/(nonMaskPixels))))
    # return round(luminosity/(nonMaskPixels))
    return luminosity/(nonMaskPixels)


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default="",
                    help="video path input")
    args = vars(ap.parse_args())

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    # grab the indexes of the facial landmarks for the mouth
    (mStart, mEnd) = (49, 68)

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    try:
        fvs = FileVideoStream(path=args["video"]).start()
    except:
        print('Cannot open file!')
        sys.exit(1)

    frame_width = 640
    frame_height = 360

    framerate = 25
    # Create CSV files for the mouth luminosity values of all frames
    # and a file for the pixel coordinates of the outline
    fileName, fileExt = os.path.splitext(args["video"])
    mouthLumCsvName = fileName+'_mouthLum.csv'
    with open(mouthLumCsvName, 'w') as mouthLumCsv:
        mouthLumCsvWriter = csv.writer(mouthLumCsv)
    mouthCoorCsvName = fileName+'_mouthCoor.csv'
    with open(mouthCoorCsvName, 'w') as mouthCoorCsv:
        mouthCoorCsvWriter = csv.writer(mouthCoorCsv)

    # loop over frames from the video stream
    frameNum = 0
    while True:
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = fvs.read()
        if not (frame is None):
            frame = imutils.resize(frame, width=frame_width)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale frame
            faces = detector(gray, 0)
            
            if(frameNum % 100) == 0:
                print('Frame num : {}'.format(frameNum))
            
            # loop over the face detections
            imgMask = np.zeros(frame.shape, np.uint8)
            imgMask = cv2.cvtColor(imgMask, cv2.COLOR_BGR2GRAY)
            
            mouthLumCsv = open(mouthLumCsvName, 'a')
            mouthLumCsvWriter = csv.writer(mouthLumCsv)
            mouthCoorCsv = open(mouthCoorCsvName, 'a')
            mouthCoorCsvWriter = csv.writer(mouthCoorCsv)
            for face in faces:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, face)
                shape = face_utils.shape_to_np(shape)
                # TODO: Should we be using ML to track faces?
                
                # extract the mouth coordinates
                mouth = shape[mStart:mEnd]
                mouthCoorCsvWriter.writerow(mouth)
                
                # compute the convex hull for the mouth, then
                # visualize the mouth
                mouthHull = cv2.convexHull(mouth)
                
                # Generate a mask for each mouth
                mask = np.zeros(frame.shape, np.uint8)
                mask = cv2.drawContours(mask, [mouthHull], -1, (255,255,255), -1)
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                imgMask = cv2.bitwise_or(imgMask, mask)
                maskedImage = cv2.bitwise_and(frame, frame, mask=mask)
                averageLuminosity = get_luminosity_of_masked_image(maskedImage)
                mouthLumCsvWriter.writerow([frameNum, averageLuminosity])
            
            mouthLumCsv.close()
            frameNum+=1
        else:
            break

    print('Finished!')
    print('Closing everything.')

    # do a bit of cleanup
    cv2.destroyAllWindows()
    fvs.stop()
    sys.exit(0)
