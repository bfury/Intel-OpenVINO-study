
from __future__ import print_function
import sys
import os
from argparse import ArgumentParser, SUPPRESS
import cv2
import numpy as np
import logging as log

from openvino.inference_engine import IECore

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")
    args.add_argument("-m", "--model", help="Required. Path to an .xml file with a trained model.",
        required=True, type=str)

    args.add_argument("-i", "--input", help="Required. Path to image file.",
        required=True, type=str, nargs="+")

    args.add_argument("--labels", help="Optional. Labels mapping file", default=None, type=str)
    return parser

 

def main():
    log.basicConfig(format="[ %(levelname)s ] %(message)s", level=log.INFO, stream=sys.stdout)
    args = build_argparser().parse_args()
    
    ie = IECore()

    # Read IR 
    model_xml = args.model
    model_bin = os.path.splitext(model_xml)[0] + ".bin"

    net = ie.read_network(model=model_xml, weights=model_bin)

    #  Read and preprocess input
    input_blob = next(iter(net.inputs))
    n, c, h, w = net.inputs[input_blob].shape
    images = np.ndarray(shape=(n, c, h, w))
    images_hw = []

    for i in range(n):
        image = cv2.imread(args.input[i])
        ih, iw = image.shape[:-1]
        images_hw.append((ih, iw))
        log.info("File was added: ")
        log.info("        {}".format(args.input[i]))
        if (ih, iw) != (h, w):
            image = cv2.resize(image, (w, h))
            log.warning("Image {} is resized from {} to {}".format(args.input[i], image.shape[:-1], (h, w)))
        image = image.transpose((2, 0, 1))  # Change data layout from HWC to CHW
        images[i] = image

    #Prepare input blobs 
    log.info("Preparing input blobs")
    assert (len(net.inputs.keys()) == 1 or len(net.inputs.keys()) == 2), "Sample supports topologies only with 1 or 2 inputs"
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))

    input_name, input_info_name = "", ""

 

    for input_key in net.inputs:
        if len(net.inputs[input_key].layout) == 4:
            input_name = input_key
            log.info("Batch size is {}".format(net.batch_size))
            net.inputs[input_key].precision = 'U8'
        elif len(net.inputs[input_key].layout) == 2:
            input_info_name = input_key
            net.inputs[input_key].precision = 'FP32'
            if net.inputs[input_key].shape[1] != 3 and net.inputs[input_key].shape[1] != 6 or net.inputs[input_key].shape[0] != 1:
                log.error('Invalid input info. Should be 3 or 6 values length.')
 

    # Prepare output blobs 
    log.info('Preparing output blobs')

    output_name, output_info = "", net.outputs[next(iter(net.outputs.keys()))]
    
    for output_key in net.outputs:
        if net.layers[output_key].type == "DetectionOutput":
            output_name, output_info = output_key, net.outputs[output_key]

    if output_name == "":
        log.error("Can't find a DetectionOutput layer in the topology")

    output_dims = output_info.shape

    if len(output_dims) != 4:
        log.error("Incorrect output dimensions for SSD model")

    max_proposal_count, object_size = output_dims[2], output_dims[3]

    if object_size != 7:
        log.error("Output item should have 7 as a last dimension")

    output_info.precision = "FP32"

    # Performing inference 
    log.info("Loading model to the device")
    exec_net = ie.load_network(network=net, device_name="CPU")
    log.info("Creating infer request and starting inference")

    res = exec_net.infer(inputs={input_blob: images})

    # Read and postprocess output 
    log.info("Processing output blobs")

    res = res[out_blob]
    boxes, classes = {}, {}
    data = res[0][0]

    ##prepare labels
    with open('../../../../Downloads/BDpanDownloads/51openlab/03/exercise-2/labels.txt') as f:
        labels = dict(x.rstrip().split(None, 1) for x in f)

    for number, proposal in enumerate(data):
        if proposal[2] > 0:
            imid = np.int(proposal[0])
            ih, iw = images_hw[imid]

            label = str(np.int(proposal[1]))

            confidence = proposal[2]

            xmin = np.int(iw * proposal[3])
            ymin = np.int(ih * proposal[4])
            xmax = np.int(iw * proposal[5])
            ymax = np.int(ih * proposal[6])

            print("Detected Object is {}".format(labels[label]))

            if proposal[2] > 0.5:
                if not  imid in boxes.keys():
                    boxes[imid] = []
                boxes[imid].append([xmin, ymin, xmax, ymax, labels[label]])
                if not  imid in classes.keys():
                    classes[imid] = []
                classes[imid].append(label)
            else:
                print()

    

    for imid in classes:
        tmp_image = cv2.imread(args.input[imid])
        for box in boxes[imid]:
            cv2.rectangle(tmp_image, (box[0], box[1]), (box[2], box[3]), (232, 35, 244), 2)
            cv2.putText(tmp_image, str(box[4]),(box[0], box[1]),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

        cv2.imwrite("out.bmp", tmp_image)
        log.info("Image out.bmp created!")

    log.info("Execution successful\n")

if __name__ == '__main__':
    sys.exit(main() or 0)
