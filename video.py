
import torch #pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
from matplotlib import pyplot as plt
import numpy as np
import cv2
import ssl
import os
ssl._create_default_https_context = ssl._create_unverified_context

model = torch.hub.load('ultralytics/yolov5','custom', path='models/mask/last.pt',force_reload=True)

class Video(object):
    def __init__(self): 
        self.index = 0
  
    def __del__(self):
        try:
            self.video.release()
        except:
            print('video release error')
 
    def get_frame(self, video):
        self.video = video
        ret, frame = video.read()   
        #return frame
        # Make detections 
        results = model(frame)  
        draw = np.squeeze(results.render())
        ret, jpg = cv2.imencode('.jpg',draw) 
        #cv2.imshow('Detector mask', np.squeeze(results.render())) 
        return jpg.tobytes()
