from email import message
import numpy as np
import os 

class LoadFile(object):
    def __init__(self):
        self.path = os.path.join('data') 
        self.filenames = []
        
    def get_files(self):
        path = self.path
        try:
            filenames = os.listdir(path)
            files = [path +'/' + images for images in filenames] 
            self.filenames = np.sort(files)
            #print('self.filenames: ',self.filenames)
        except:
            return {'success' : False, 'message' : "No such file or directory"}
        #except FileNotFoundError:
            #self.error = ("No such file or directory: 'data'")
        finally:            
            if (len(self.filenames) <= 0):
                return {'success' : False, 'message' : "No file"}
            else:
                file = self.filenames
                return {'success' : True, 'file' : file[len(file) - 1]}
                
        