# Author:bfury
# since:31/7/2021
import cv2 as cv

# Load the model
net = cv.dnn.readNet('../IRmodel/face-detection-adas-0001.xml', '../IRmodel/face-detection-adas-0001.bin')

# Specify target device (CPU)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# Read an image
frame = cv.imread('../sources/faces.jpeg')

# Prepare input blob 
blob = cv.dnn.blobFromImage(frame, size=(672, 384), ddepth=cv.CV_8U)

#perform inference (face detection)
net.setInput(blob)
out = net.forward()

# Draw detected faces on the frame
for detection in out.reshape(-1, 7):

    confidence = float(detection[2])

    xmin = int(detection[3] * frame.shape[1])
    ymin = int(detection[4] * frame.shape[0])
    xmax = int(detection[5] * frame.shape[1])
    ymax = int(detection[6] * frame.shape[0])

    if confidence > 0.5:
        cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

# Save the frame to an image file
cv.imwrite('./result/out1.png', frame)

for detection in out.reshape(-1, 7):

    confidence = float(detection[2])

    xmin = int(detection[3] * frame.shape[1])
    ymin = int(detection[4] * frame.shape[0])
    xmax = int(detection[5] * frame.shape[1])
    ymax = int(detection[6] * frame.shape[0])

    if confidence > 0.2:
        cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

# Save the frame to an image file
cv.imwrite('./result/out2.png', frame)