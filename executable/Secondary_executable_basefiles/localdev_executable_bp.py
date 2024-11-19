import argparse
import base64
import sys
import PySimpleGUI as sg
import os
import sys
import cv2
import time
import urllib3
import regex
from os.path import expanduser
import subprocess

__version__=0.01
url='https://raw.githubusercontent.com/Mainakdey1/Image-Encryption-using-Cellular-Automata-Draft/refs/heads/main/executable/Secondary_executable_basefiles/localdev_executable_bp.py'
dir_pathV= expanduser("~")+"\\" 
file=sys.argv[0]




def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


image_path = resource_path('newimg.png')

class logger:


    def __init__(self,_log_file,_global_severity=0 ,_dir_path=str,_logobj= str):
        self._logobj=_logobj
        self._global_severity=_global_severity
        self._log_file=_log_file
        self._dir_path=_dir_path
        
    

    def info(self,_function_name,_message):

    
        log_file=open(self._dir_path+self._log_file,"a+")
        log_file.write("\n"+time.ctime()+" at "+str(time.perf_counter_ns())+"    "+_function_name+"   called (local_severity=INFO)with message:  "+_message)
        log_file.close()


    def warning(self,_function_name,_message):

        log_file=open(self._dir_path+self._log_file,"a+")
        log_file.write("\n"+time.ctime()+" at "+str(time.perf_counter_ns())+"    "+_function_name+"   called (local_severity=WARNING)with message:  "+_message)
        log_file.close()

    def critical(self,_function_name,_message):

        log_file=open(self._dir_path+self._log_file,"a+")
        log_file.write("\n"+time.ctime()+" at "+str(time.perf_counter_ns())+"    "+_function_name+"   called (local_severity=CRITICAL)with message:  "+_message)
        log_file.close()
 
#call this method to produce the log file
    def producelog(self):
        log_file=open(self._dir_path+self._log_file,"r")
        msg=log_file.readlines()
        log_file.close()
        return msg
    
#call this method to find the privilege level of the current logging instance.
    def privilege(self):
        if self._global_severity==0:
            print("This logger is at the highest privilege level")
        else:
            return self._global_severity
        
#call this method to identify the logging instance, if there are several instances initiated.
    def identify(self):
        print(self._logobj)

logins=logger("logfile.txt",0,dir_pathV,"globallogger")


def custom_popup_yes_no(message, title='', keep_on_top=True):
    # Define the layout for the custom popup window
    layout = [
        [sg.Text(message)],
        [sg.Button('Yes'),
         sg.Button('No')]
    ]

    # Create the window without a title bar
    window = sg.Window(title, layout, keep_on_top=keep_on_top, no_titlebar=True, element_justification='center')

    # Read the window's events
    event, _ = window.read()

    # Close the window
    window.close()

    return event



#initiate connection object.
try:

    connection_pool=urllib3.PoolManager()
    resp=connection_pool.request("GET",url)
    match_regex=regex.search(r'__version__*= *(\S+)', resp.data.decode("utf-8"))
    logins.info("CONNECTION OBJECT","CONNECTION OBJECT INITIALIZED")
except:
    logins.critical("CONNECTION OBJECT","CONNECTION OBJECT NOT INITIALIZED")


match_regexno=float(match_regex.group(1))

#version matching is done here
if match_regexno>__version__:

    try:

    
        response = custom_popup_yes_no('A new version has been found. Do you wish to update?')

        if response== 'Yes':
            #new version available. update immediately
            logins.info("REGEX VERSION MATCH","NEW VERSION FOUND")
            origin_file=open(file,"wb")
            origin_file.write(resp.data)
            origin_file.close()
            logins.info("REGEX VERSION MATCH","SUCCESFUL")
            subprocess.call(file,shell=True)

    except:
        logins.critical("REGEX VERSION MATCH","UNSUCCESFUL")
elif match_regexno<__version__:
    try:

        #version rollback initiated. updating to old version
        logins.info("REGEX VERSION MATCH","NEW VERSION FOUND")
        origin_file=open(file,"wb")
        origin_file.write(resp.data)
        origin_file.close()
        logins.info("REGEX VERSION MATCH","VERSION ROLLBACK INITIATED")
        subprocess.call(file,shell=True)
    except:
        logins.critical("REGEX VERSION MATCH","UNSUCCESFUL")
else:
    #no new version found. 
    #update not called.
    logins.info("REGEX VERSION MATCH","NO NEW VERSION FOUND")

    
   









class file_read:
    def __init__(self, _coded_b64) -> None:
        self._coded_b64=_coded_b64
        decoded_byte= base64.b64decode(self._coded_b64)
        _file_data=decoded_byte.decode('utf-8')


        primary_len=len(_file_data)

        self._data=[]

        count=0


        for i in range(primary_len):
            if _file_data[i] == '|':
                if count==0:
                    
                    self._data+=[_file_data[count:i],]
                    count=i
                else:
                    self._data+=[_file_data[count+1:i],]
                    count=i


            elif _file_data[i] == '~':
                self._data+=[_file_data[count+1:i],]
                self._key=_file_data[i+1:]

    
        pass

    def data(self):
        return self._data
    
    def key(self):
        return self._key

def signo_repr(primary_key, secondary_key, encryptped_data):
    import numpy as np
    height, width= 360, 480
    unenc_signature_arr=[]
    prim_len=len(primary_key)
    for i in range(prim_len):
        unenc_signature_arr+=[int(primary_key[i])^(int(encryptped_data[i]))]


    


   


    
    unenc_np_arr=np.array(unenc_signature_arr)
    unenc_image=unenc_np_arr.reshape((height,width))    
    unenc_image=unenc_image.astype(np.uint8)
  
    cv2.imshow('the final image',unenc_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




def main():


    

    try:
        parser = argparse.ArgumentParser(description=".")
        parser.add_argument("file", help="Path to the file you want to read")
        args = parser.parse_args()
        if args.file.endswith('.pxe'):
                
            with open(args.file, 'r') as f:
                content = f.read()
                


                flr_pre=file_read(content)
                data=flr_pre.data()
                key=flr_pre.key()
 
                modified_primary_len=len(data)
                new_data=''
                signo_data=[]

                for i in range(modified_primary_len):
                    signo_data+=[int(data[i])^int(key[i]),]
                sg.theme('LightPurple')

                

                layout = [
                [sg.Text('Please select the type of data you want to decrypt :')],
                [sg.Radio('Text Decryption', 'RADIO1', key='te', size=(40)), sg.Radio('Image Decryption', 'RADIO1', key='ie', size=40), sg.Radio('Signature Decryption', 'RADIO1', key='sige' , size=40) , ],
                
                [sg.Button('Submit'), sg.Button('Cancel') ]
                ]

                
                window = sg.Window( "new window", layout, no_titlebar=True)
                event , vals= window.read()
                window.close()
                stat_inp=0
                for k in vals:
                    if  k=='te' and vals[k]==True :
                        stat_inp=1
            
                    elif k=='ie' and vals[k]==True :
                        stat_inp=2
                    elif k=='sige' and vals[k]==True :
                        stat_inp=3


                if stat_inp == 1:
                    try:
                    

                        sg.theme('LightPurple') 
                        title_bar = [
                                    [sg.Text('PXEopen', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                                    ]
                                ]
                        layout = [[sg.Column(title_bar, background_color='#2e756a')], [sg.Image(filename=image_path )], [sg.Input(key='-IN-'), sg.FileBrowse()],
                        [sg.Button('Go'), sg.Button('Exit')]]

                        #choose your input file here
                        window = sg.Window('select your primary encryption key please', layout, no_titlebar=True)
                        event,values = window.read()
                        window.close()
                        file_path = values['-IN-']
                        file_extension = os.path.splitext(file_path)
                        if file_extension[1] == '.pxe' :
                            try:
                                with open(file_path, 'r') as file:
                                    ac_key_b64 = file.read()
                                    window.close()
                                    flr_post=file_read(ac_key_b64)
                                    ac_key_key=flr_post.key()
                                    ac_key_data=flr_post.data()
                                    ac_key=''
                                    for i in range(len(ac_key_data)):
                                        ac_key+=str(int(ac_key_data[i])^int(ac_key_key[i]))

                                    
                                    for i in range(modified_primary_len):
                                        new_data+=chr(int(data[i])^int(key[i])^int(ac_key[i]))
                                                    
                                    print(new_data)

                                    sys.exit()

                            except:
                                print()


                    except:
                        print('module error')

                if stat_inp == 3:
                    signo_primary_ac_key=''
                    signo_sec_ac_key=''
                    try:
                    

                        sg.theme('LightPurple') 
                        title_bar = [
                                    [sg.Text('PXEopen', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                                    ]
                                ]
                        layout = [[sg.Column(title_bar, background_color='#2e756a')], [sg.Image(filename=image_path )], [sg.Input(key='-IN-'), sg.FileBrowse()],
                        [sg.Button('Go'), sg.Button('Exit')]]

                        #choose your input file here
                        window = sg.Window('select your secondary encryption key please', layout, no_titlebar=True)
                        event,values = window.read()
                        window.close()
                        prim_file_path = values['-IN-']
                        window.close()
                        file_extension = os.path.splitext(prim_file_path)





                        if file_extension[1] == '.pxe' :



                                
                                with open(prim_file_path, 'r') as file:
                                    signo_primary_ac_key_b64 = file.read()
                                    window.close()
                                    flr_post=file_read(signo_primary_ac_key_b64)

                                    signo_primary_ac_key_key=flr_post.key()
                                    signo_primary_ac_key_data=flr_post.data()

                                    signo_primary_ac_key=[]
                                    
                                    for i in range(len(signo_primary_ac_key_data)):
                                     
                                        signo_primary_ac_key+=str(int(signo_primary_ac_key_data[i])^int(signo_primary_ac_key_key[i]))

                                    

                                     
                                    














                        sg.theme('LightPurple') 
                        title_bar = [
                                    [sg.Text('PXEopen', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                                    ]
                                ]
                        layout = [[sg.Column(title_bar, background_color='#2e756a')], [sg.Image(filename=image_path )], [sg.Input(key='-IN-'), sg.FileBrowse()],
                        [sg.Button('Go'), sg.Button('Exit')]]

                        #choose your input file here
                        window = sg.Window('select your secondary encryption key', layout, no_titlebar=True)
                        event,values = window.read()
                        sec_file_path = values['-IN-']

                        window.close()
                        file_extension = os.path.splitext(sec_file_path)



                        if file_extension[1] == '.pxe' :
                            try:
                                with open(sec_file_path, 'r') as file:
                                    signo_sec_ac_key_b64 = file.read()
                                    
                                    flr_post=file_read(signo_sec_ac_key_b64)
                                    signo_sec_ac_key_key=flr_post.key()
                                    signo_sec_ac_key_data=flr_post.data()
                                    signo_sec_ac_key=[]
                                    for i in range(len(signo_sec_ac_key_data)):
                                        signo_sec_ac_key+=str(int(signo_sec_ac_key_data[i])^int(signo_sec_ac_key_key[i]))

                                    


                                window.close()


                            except:
                                print('Provided file is not of the appropriate format')

                                          
                        signo_repr(signo_primary_ac_key,signo_sec_ac_key,signo_data)

                    except:
                        print()
  

                        
        else:
            print("Invalid file type for this application")
            raise Exception("Invalid file type. Please connect both of your brain cells together.")



                




                



    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



    except:
        print()
        

if __name__ == "__main__":
    main()
