from flask import Flask, render_template, Response
from video import Video
from file import LoadFile
from matplotlib import pyplot as plt
import numpy as np
import cv2
import ssl
import datetime
import os

app = Flask(__name__)

global_temp = 1

@app.route('/')
def index():
    global global_temp
    dateTimeNow = datetime.datetime.now()
    return render_template('index.html',    
    timeNow = "{}-{}-{} {}:{}".format(dateTimeNow.year, dateTimeNow.month, dateTimeNow.day, dateTimeNow.hour, dateTimeNow.minute, dateTimeNow.second),
    temp=global_temp)

def render(video):  
    print('file: ')
    t = 0
    file = LoadFile()
    loadFileName = ''
    while True:        
        t+=1
        loadFile = file.get_files() #get new video (the first)
        #print('loadFile: ',loadFile)        
        if(loadFile['success']):
            try: 
                cap = cv2.VideoCapture(loadFile['file'])
                length = int(cv2.VideoCapture.get(cap, int(cv2.CAP_PROP_FRAME_COUNT)))
                width = int(cv2.VideoCapture.get(cap, int(cv2.CAP_PROP_FRAME_WIDTH))) 
                #print('width: ',width)
                j = 0
                if(loadFileName != loadFile['file']):                 
                    loadFileName = loadFile['file']       
                    while True and (length > 0 and j < length):
                        
                        j+=1
                        try:
                            global global_temp
                            global_temp = {'totalFrame' : length, 'countFrame' : j, 'widthVideo':width, 'nameVideo' : loadFileName}
                            frame = video.get_frame(cap)
                            yield(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                            #print('Success frame',j,length)
                        except Exception as e:   
                            print('Error frame: ', str(e))
                            break 
            except Exception as e:    
                print('Main: ',str(e))

        else:            
            print(loadFile['message'])
        if(t==3): 
            print('break: ',t)
            #break
 

@app.route('/video')
def video():
    return Response(render(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/read_sensor')
def read_sensor():
    global global_temp
    # return the actual sensor data here:
    return {'infoVideo': global_temp}

app.run(debug=True)