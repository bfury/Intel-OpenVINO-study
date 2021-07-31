#!/usr/bin/env python

from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import time
import logging as log

from openvino.inference_engine import IENetwork, IECore


def main():

    model_xml = "model.xml"
    model_bin = "model.bin"

    ie = IECore()
    net=ie.read_network(model=model_xml, weights=model_bin)

    
    input_blob = next(iter(net.inputs))
  

    feed_dict = {}
   
    out_blob = next(iter(net.outputs))

    exec_net = ie.load_network(network=net, num_requests=2, device_name="CPU")

    n, c, h, w = net.inputs[input_blob].shape
   
    cap = cv2.VideoCapture("road.mp4")
    

    cur_request_id = 0
    next_request_id = 1

    with open('labels.txt', 'r') as f:
        labels_map = [x.strip() for x in f]
    

    ret, frame = cap.read()
    frame_h, frame_w = frame.shape[:2]

    #Open file for writing video .avi format
    out_video = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_w,frame_h))


    #Define numbers to each frame
    frame_num = 0

    while cap.isOpened():
        
        ret, next_frame = cap.read()

        #Print Frame number
        sys.stdout.write("\nFrame  " + str(frame_num)+'       ')
        frame_num = frame_num + 1
        
        #Slow down a little..
        time.sleep(0.2) 


        if ret:
            frame_h, frame_w = frame.shape[:2]
        if not ret:
            break  

        in_frame = cv2.resize(next_frame, (w, h))
        in_frame = in_frame.transpose((2, 0, 1))  
        in_frame = in_frame.reshape((n, c, h, w))
        feed_dict[input_blob] = in_frame

        #Start timer
        time_start = time.time()

        exec_net.start_async(request_id=next_request_id, inputs=feed_dict)
            
        #stop timer
        time_end = time.time()
        inference_time = time_end - time_start

        sys.stdout.write('%.5s' %  inference_time)



        if exec_net.requests[cur_request_id].wait(-1) == 0:
            res = exec_net.requests[cur_request_id].outputs[out_blob]

            for obj in res[0][0]:
                if obj[2] > 0.5:
                    xmin = int(obj[3] * frame_w)
                    ymin = int(obj[4] * frame_h)
                    xmax = int(obj[5] * frame_w)
                    ymax = int(obj[6] * frame_h)
                    class_id = int(obj[1])

                    #Print Detected classes
                    sys.stdout.write(str(class_id)+'  ')

                    color = (min(class_id * 25, 255), min(class_id * 60, 255), min(class_id * 5, 255))
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                    det_label = labels_map[class_id] if labels_map else str(class_id)
                    cv2.putText(frame, det_label + ' ' + str(round(obj[2] * 100, 1)) + ' %', (xmin, ymin - 7),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)
                    
                    
        #write next frame to video file.
        out_video.write(frame)
        
        cur_request_id, next_request_id = next_request_id, cur_request_id
        frame = next_frame
        frame_h, frame_w = frame.shape[:2]

        key = cv2.waitKey(1)
        if key == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main() or 0)
