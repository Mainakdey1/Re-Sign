import subprocess
import os





import urllib3
import regex
import imageio.v3
import time
import sys
import numpy as np
import cv2
import random
import PySimpleGUI as sg
import base64
from os.path import expanduser
import pyotp
import qrcode
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
import bcrypt
import pyrebase #important note: Please use pip install pyrebase4 or whatever the lates version of pyrebase is. There is module and package naming discrepancy for pyrebase.
import firebase_admin
from firebase_admin import credentials, db
import requests
from datetime import datetime




#gets the filepath of the current file the program is in
file=sys.argv[0]
 
str_to_int_limits=100000  #sets the string to integer conversion limit to a specified number
nca_limit=10000  
size=101
tbit=size//2
stat_inp=0


dir_pathV= expanduser("~")+"\\"    #saves log file directly to the current working directory
sg.theme('DarkTeal10')             #sets the global gui color for the program
url='https://raw.githubusercontent.com/Mainakdey1/Image-Encryption-using-Cellular-Automata-Draft/refs/heads/main/AI-differentiator/AI_branch_server.py'


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


image_path = resource_path('dark.png')




start_time=time.time()
sys.set_int_max_str_digits(str_to_int_limits)


#new_vers=107
__version__=0.108



def get_online_time():
    try:
        response = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Kolkata")
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data

    except requests.RequestException as e:
        print(f"Error fetching online time: {e}")
        return None

def compare_times():
    dt= datetime.now()
    hour= dt.hour
    minute = dt.minute
    day = dt.day
    month = dt.month
    try:
        dted = get_online_time()
        if dted['hour'] == hour and dted['minute'] == minute and dted['day'] == day and dted['month'] == month:
            return True
        else:
            return False
    except:
        print('Errorrrrr')


try:
    if compare_times() == True:
        print('Time zones are synchronized')

    else:
        print('Time zone not synchronized, please synchronize data and time on local device.')


except Exception as e:
    print(f"An error occured: {e}"
          )


#Logger class for logging events. Events have 3 severity:info, warning and critical
#info: call with this to record events that are part of the normal functioning of the program
#warning: call with this severity to record events that are crucial but will not break the funtioning of the program.
#critical: call with this severity to record events that are critical to the functioning of the program.

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



def storage_enc():

    def sbox(hieght,width):

        res_arr=[]
        for i in range(hieght*width):
            res_arr+=[random.randint(0,255),]

        return res_arr

    def rule30(left, center, right):


        RULE_30 = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    }
        return RULE_30[(left, center, right)]

    def rule90(left, center, right):

        RULE_90 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    }
        return RULE_90[(left, center, right)]

    def rule115(left, center, right):
        RULE_115 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 1,
        (0, 0, 0): 1
    }
        return RULE_115[(left, center, right)]



    def rule110(left, center, right):

        RULE_110 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 1,
        (0, 0, 0): 0
    }
        return RULE_110[(left, center, right)]

    def rule197(left, center, right):

        RULE_197 = {
        (1, 1, 1): 1,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 0,
        (0, 1, 1): 0,
        (0, 1, 0): 1,
        (0, 0, 1): 0,
        (0, 0, 0): 1
    }
        return RULE_197[(left, center, right)]
    
    def rule80(left, center, right) :
        RULE_80 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 1,
        (0, 1, 1): 0,
        (0, 1, 0): 0,
        (0, 0, 1): 0,
        (0, 0, 0): 0
    }
        
        return RULE_80[(left, center, right)]
    
    def rule45(left, center, right) :
        RULE_45 = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 1,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 1,
        (0, 0, 1): 0,
        (0, 0, 0): 1
        }
        
        return RULE_45[(left, center, right)]
    
    def rule129(left, center, right) :
        RULE_129 = {
        (1, 1, 1): 1,
        (1, 1, 0): 0,
        (1, 0, 1): 0,
        (1, 0, 0): 0,
        (0, 1, 1): 0,
        (0, 1, 0): 0,
        (0, 0, 1): 0,
        (0, 0, 0): 1
        }
        
        return RULE_129[(left, center, right)]
    
    def rule73(left, center, right) :
        RULE_73 = {
        (1, 1, 1): 0,
        (1, 1, 0): 1,
        (1, 0, 1): 0,
        (1, 0, 0): 0,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 0,
        (0, 0, 0): 1
        }
        
        return RULE_73[(left, center, right)]

    def rule54(left, center, right) :
        RULE_54 = {
        (1, 1, 1): 0,
        (1, 1, 0): 0,
        (1, 0, 1): 1,
        (1, 0, 0): 1,
        (0, 1, 1): 1,
        (0, 1, 0): 0,
        (0, 0, 1): 1,
        (0, 0, 0): 1
        }
        
        return RULE_54[(left, center, right)]








    


    def initialize_ca(size,tbit):
        cells=np.zeros(size, dtype=int)
        cells[tbit]=1
        return cells

    def update_cells(cells):
        rule_randomizer_int=0



        new_cells = np.zeros_like(cells)
        for i in range(1, len(cells) - 1):
            rule_randomizer_int=random.randint(0,9)
            if rule_randomizer_int==0:

                new_cells[i] = rule30(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==1:
                new_cells[i] = rule90(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==2:
                new_cells[i] = rule115(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==3:
                new_cells[i] = rule110(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==4:
                new_cells[i] = rule197(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==5:
                new_cells[i] = rule80(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==6:
                new_cells[i] = rule129(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==7:
                new_cells[i] = rule45(cells[i - 1], cells[i], cells[i + 1])
            
            elif rule_randomizer_int==8:
                new_cells[i] = rule73(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==9:
                new_cells[i] = rule54(cells[i - 1], cells[i], cells[i + 1])

        return new_cells

    def generate_psn(size,nbit, target_bit):
        cells=initialize_ca(size,target_bit)
        bit_stream=[]
        for _ in range(nbit):
            temp_cell=update_cells(cells)
            bit_stream+=[temp_cell[target_bit],]


        return bit_stream

    size=101
    nbit=10000
    target_bit=size//2
    binary_gen=generate_psn(size,nbit, target_bit)
    

    storage_pseudo_random_number = int("".join(map(str, binary_gen)), 2)
    

    return storage_pseudo_random_number








class encoded_file_storage():
    #storage
    def __init__(self,file_path = None, _pseudo_random_number = None) -> None:
        self._file_path=file_path
        self._pseudo_random_number=_pseudo_random_number
        
    def encode(self,pretext):

        prim_len=len(pretext)
        if prim_len>=len(str(self._pseudo_random_number)):
            temp=prim_len//len(str(self._pseudo_random_number))
            rem=prim_len-temp*(len(str(self._pseudo_random_number)))
            spseudo_random_number=temp*(str(self._pseudo_random_number))+rem*"0"

        else:
            
            spseudo_random_number=int(str(self._pseudo_random_number)[:(len(pretext))])

        
        _enc_string=[]
        for i in range(prim_len):
            _enc_string+=[str(int(str(spseudo_random_number)[i])^int(pretext[i])),]


        _new_enc_string=''
        for i in range(prim_len):
            if i!=prim_len-1:
                _new_enc_string+=_enc_string[i]+'|'
            else:
                _new_enc_string+=_enc_string[i]

        scrambled_enc_string=_new_enc_string+'~'+str(spseudo_random_number)
        


        encoded_data = base64.b64encode(scrambled_enc_string.encode('utf-8'))

            
        


        

        
        # Writing the Base64 encoded data to a new file
        
        with open(self._file_path, 'wb+') as encoded_file:
            encoded_file.write(encoded_data)
        
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


    




logins=logger("logfile.txt",0,dir_pathV,"globallogger")
logins.info("APPLICATION VERSION NUMBER : ",str(__version__))





# Firebase configuration
firebase_config = {
    'apiKey': "AIzaSyC7EXl7sMRE1rrwRted_kYKybecl0IQajk",
  'authDomain': "ssenc-96031.firebaseapp.com",
  'databaseURL': "https://ssenc-96031-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "ssenc-96031",
  'storageBucket': "ssenc-96031.firebasestorage.app",
  'messagingSenderId': "371333696694",
  'appId': "1:371333696694:web:37043b8b1212e36796ea17",
  'measurementId': "G-NGPL08S15H"

}



# Initialize Firebase app
cred = credentials.Certificate(r"C:\Users\chestor\Desktop\Project_tempfiles\Units\ssenc_json.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ssenc-96031-default-rtdb.asia-southeast1.firebasedatabase.app"
})



def change_password_in_database(username, new_password):
    ref = db.reference('users')  # Reference the "users" node in the database
    user_ref = ref.child(username)  # Locate the specific user
    hashed_new_pw= hash_password(new_password)

    if user_ref.get():
        user_ref.update({"password": hashed_new_pw.decode('utf-8')})
        sg.popup("Password reset successfully", "Welcome back!", title="Success", no_titlebar=True)  # Show success message
        print("Password updated successfully in the database!")
    else:
        print("User not found.")

    return


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())











firebase = pyrebase.initialize_app(firebase_config)
dab = firebase.database()

def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

def sign_up(username, password):
    users = dab.child("users").get().val()
    if users and username in users:
        print("Username already exists.")
        return
    
    hashed_password = hash_password(password)
    dab.child("users").child(username).set({"password": hashed_password.decode('utf-8')})
    print("User registered successfully!")

def login(username, password):
    user = dab.child("users").child(username).get().val()
    if not user:
        print("User not found.")
        sys.exit()
        return False

    
    stored_password = user["password"].encode('utf-8')
    if verify_password(stored_password, password):
        print("Login successful!")

    else:
        print("Invalid username or password.")
        return False
        sys.exit()
    
    return True


def sign_up_gui():




    sg.LOOK_AND_FEEL_TABLE['CustomSignupTheme'] = {
        'BACKGROUND': '#2C3E50',
        'TEXT': '#ECF0F1',
        'INPUT': '#34495E',
        'TEXT_INPUT': '#ECF0F1',
        'SCROLL': '#2C3E50',
        'BUTTON': ('#FFFFFF', '#1ABC9C'),
        'PROGRESS': ('#2E86C1', '#D0D3D4'),
        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    }



    layout = [
        [sg.Text("✨ Sign Up ✨", size=(30, 1), justification='center', font=("Helvetica", 20), text_color='#1ABC9C')],
        [sg.Text("Create a new account", size=(25, 1), justification='center', font=("Helvetica", 12), text_color='lightgray')],
        [sg.HorizontalSeparator(color='#1ABC9C')],
        [sg.Text("Username:", size=(10, 1), font=("Helvetica", 12)), 
        sg.InputText("", size=(30, 1), key='-USERNAME-', tooltip="Enter your username")],
        [sg.Text("Password:", size=(10, 1), font=("Helvetica", 12)), 
        sg.InputText("", size=(30, 1), key='-PASSWORD-', password_char='*', tooltip="Enter your password")],
        [sg.Button("Sign Up", size=(15, 1), font=("Helvetica", 12), tooltip="Click to create your account"),
        sg.Button("Cancel", size=(15, 1), font=("Helvetica", 12))],
        [sg.Text('', size=(40, 1), justification='center', key='-MESSAGE-', text_color='red')],
    ]


    window = sg.Window("Signup Page", layout, size=(450, 350), element_justification='center', finalize=True, no_titlebar=True)


    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            sys.exit()
            break
        elif event == 'Sign Up':
            username = values['-USERNAME-']
            password = values['-PASSWORD-']
            sign_up(username =  username, password = password)


            if username  and password:

                sg.popup("Registered as new user!", "Welcome to the app!", title="Success", no_titlebar=True)  # Show success message
                window.close()
 
            else:
                window['-MESSAGE-'].update("All fields are required.", text_color='red')

            window.close()


    window.close()
    return 


def password_reset_gui():



    sg.LOOK_AND_FEEL_TABLE['CustomSignupTheme'] = {
        'BACKGROUND': '#2C3E50',
        'TEXT': '#ECF0F1',
        'INPUT': '#34495E',
        'TEXT_INPUT': '#ECF0F1',
        'SCROLL': '#2C3E50',
        'BUTTON': ('#FFFFFF', '#1ABC9C'),
        'PROGRESS': ('#2E86C1', '#D0D3D4'),
        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
    }



    layout = [
        [sg.Text(" Reset password ", size=(30, 1), justification='center', font=("Helvetica", 20), text_color='#1ABC9C')],
        [sg.Text("Reset your password", size=(27, 1), justification='center', font=("Helvetica", 12), text_color='lightgray')],
        [sg.HorizontalSeparator(color='#1ABC9C')],
        [sg.Text("Username:", size=(13, 1), font=("Helvetica", 12)), 
        sg.InputText("", size=(30, 1), key='-USERNAME-', tooltip="Enter your username")],
        [sg.Text("New password:", size=(13, 1), font=("Helvetica", 12)), 
        sg.InputText("", size=(30, 1), key='-PASSWORD-', password_char='*', tooltip="Enter your password")],
        [sg.Button("Reset", size=(15, 1), font=("Helvetica", 12), tooltip="Click to create your account"),
        sg.Button("Cancel", size=(15, 1), font=("Helvetica", 12))],
        [sg.Text('', size=(40, 1), justification='center', key='-MESSAGE-', text_color='red')],
    ]


    window = sg.Window("Signup Page", layout, size=(450, 350), element_justification='center', finalize=True, no_titlebar=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Reset':
            username = values['-USERNAME-']
            npassword = values['-PASSWORD-']
            change_password_in_database(username = username, new_password = npassword)
            

            if username  and npassword:

                window['-MESSAGE-'].update("Password reset successfully 🎉", text_color='green')
            else:
                window['-MESSAGE-'].update("All fields are required.", text_color='red')
                


    window.close()

sg.LOOK_AND_FEEL_TABLE['CustomTheme'] = {
    'BACKGROUND': '#2C3E50',
    'TEXT': '#ECF0F1',
    'INPUT': '#34495E',
    'TEXT_INPUT': '#ECF0F1',
    'SCROLL': '#2C3E50',
    'BUTTON': ('#FFFFFF', '#1ABC9C'),
    'PROGRESS': ('#2E86C1', '#D0D3D4'),
    'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
}



layout = [
    [sg.Text("✨ Welcome to MyApp ✨", size=(30, 1), justification='center', font=("Helvetica", 20), text_color='#1ABC9C')],
    [sg.Text("Login to Continue", size=(25, 1), justification='center', font=("Helvetica", 12), text_color='lightgray')],
    [sg.HorizontalSeparator(color='#1ABC9C')],
    [sg.Text("Username:", size=(10, 1), font=("Helvetica", 12)), 
     sg.InputText(key='-USERNAME-', size=(30, 1), tooltip="Enter your username")],
    [sg.Text("Password:", size=(10, 1), font=("Helvetica", 12)), 
     sg.InputText(key='-PASSWORD-', size=(30, 1), password_char='*', tooltip="Enter your password")],
    [sg.Text("", size=(40, 1), key='-MESSAGE-', text_color='red', justification='center')],
    [sg.Button("Login", size=(10, 1), font=("Helvetica", 12), tooltip="Click to log in"),
     sg.Button("Cancel", size=(10, 1), font=("Helvetica", 12))],
    [sg.Text("Forgot Password?", size=(20, 1), justification='center', font=("Helvetica", 10), text_color='#1ABC9C', enable_events=True, key='-FORGOT-')],
    [sg.Text("New to the Authenticator?", size=(20, 1), justification='center', font=("Helvetica", 10), text_color='#1ABC9C', enable_events=True, key='-NEW-')]
]


window = sg.Window("Login Page", layout, size=(450, 300), element_justification='center', finalize=True, no_titlebar=True)


while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        sys.exit()
        break

    elif event == 'Login':
        username = values['-USERNAME-']
        password = values['-PASSWORD-']



        if login(username, password):

            window['-MESSAGE-'].update("Login successful! 🎉", text_color='green')
            

        else:
            window['-MESSAGE-'].update("Invalid username or password.", text_color='red')
            
        break
    elif event == '-FORGOT-':
        password_reset_gui()
        window.close()
        break
   

    elif event == '-NEW-':
        window.close()
        sign_up_gui()

        print('new person sheesh')
        break


window.close()













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

    
   





#this function converts the image into a array set
def img_inp_method(path):
    try:
        imgcolor=imageio.v3.imread(path) # please add "r" in front of the path in case of input errors.
        rows, cols, rgb=imgcolor.shape

        R=[]
        G=[]
        B=[]
        for i in range(rows):
            for j in range(cols):
                B.append(imgcolor[i,j,0])
                G.append(imgcolor[i,j,1])
                R.append(imgcolor[i,j,2])


        logins.info("IMAGE INPUT METHOD CALLED","CALLED")
        return R+G+B
        
    
    except:
        logins.critical('IMAGE INPUT METHOD ',"FUNCTION INITIATION FAILED")


#this function converts the raw text into a workable array set
def text_inp_method(raw_text):
    try:
        res=[]
        lt=len(raw_text)
        for i in range(lt):
            res+=[ord(raw_text[i]),]

        logins.info('TEXT INPUT METHOD ','CALLED')

        return res
    except:
        logins.critical('TEXT INPUT METHOD ','FUNCTION INITIATION FAILED')

#this function converts the raw signature image into a workable array set
def signo_inp_method(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        height,width=image.shape
        pixel_values = image.flatten()
        logins.info('SIGNO_INP_METHOD','CALLED')    
        
        return height, width, pixel_values

    except:
        logins.critical('SIGNO_INP_METHOD','ERROR IN CALLING')


#this converts any text to binary. Used later in the program to pack text.
def text_to_binary(text):
    try:
        logins.info('TEXT_TO_BINARY','CALLED')
        return ' '.join(format(ord(char), '08b') for char in text)
    except:
        logins.warning('TEXT_TO_BINARY','ERROR IN CALLING')


def AI_differen_func(raw_image_path):



    data_dir = r"C:\Users\chestor"
    genuine_dir = os.path.join(data_dir, "genuine")
    forged_dir = os.path.join(data_dir, "forged")



    def load_data(data_dir, label , img_size = (128, 128)):


        

        images = []
        labels = []
        

        def load_images_from_folder(folder, label):
            for filename in os.listdir(folder):
                if filename.endswith(".png") or filename.endswith(".jpg"):
                    filepath = os.path.join(folder, filename)
                img = load_img(filepath, target_size=img_size, color_mode="grayscale")
                img_array = img_to_array(img)  
                images.append(img_array)
                labels.append(label)  
            return np.array(images), np.array(labels)
        
        return load_images_from_folder(data_dir, label)

    gen_signatures, gen_labels = load_data(genuine_dir,1)
    forged_signatures, forged_labels = load_data(forged_dir,0)


    all_images = np.concatenate((gen_signatures, forged_signatures), axis=0)
    all_labels = np.concatenate((gen_labels, forged_labels), axis=0)

    from sklearn.utils import shuffle
    all_images, all_labels = shuffle(all_images, all_labels, random_state=42)

    all_images = all_images / 255.0

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(all_images, all_labels, test_size=0.2, random_state=42)


    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
        MaxPooling2D((2, 2)),
        Dropout(0.2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')  
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


    history = model.fit(X_train, y_train, epochs=10, validation_split=0.2, batch_size=32)


    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Accuracy: {accuracy:.2f}")


    def predict_signature(image):
        processed_image = image / 255.0
        processed_image = np.expand_dims(processed_image, axis=0)  # Add batch dimension
        return "Genuine" if model.predict(processed_image) > 0.5 else "Forged"
    img_size=(128, 128)

    post_processed_img = load_img(raw_image_path, target_size=img_size, color_mode="grayscale")
    post_processed_img_array = img_to_array(post_processed_img)
    result = predict_signature(post_processed_img_array)
    print(f"Prediction: {result}")

    return None





#substitution method function
def sbox(hieght,width):

    res_arr=[]
    for i in range(hieght*width):
        res_arr+=[random.randint(0,255),]

    return res_arr



#rule sets. All rules are in dictionary format. This is because the lookup time for dictionaries in O(1) which is faster than calculating the individual bits.

def rule30(left, center, right):


    RULE_30 = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0
}
    return RULE_30[(left, center, right)]

def rule90(left, center, right):

    RULE_90 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 0,
    (0, 0, 1): 1,
    (0, 0, 0): 0
}
    return RULE_90[(left, center, right)]

def rule115(left, center, right):
    RULE_115 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 0,
    (0, 0, 1): 1,
    (0, 0, 0): 1
}
    return RULE_115[(left, center, right)]



def rule110(left, center, right):

    RULE_110 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0
}
    return RULE_110[(left, center, right)]

def rule197(left, center, right):

    RULE_197 = {
    (1, 1, 1): 1,
    (1, 1, 0): 1,
    (1, 0, 1): 0,
    (1, 0, 0): 0,
    (0, 1, 1): 0,
    (0, 1, 0): 1,
    (0, 0, 1): 0,
    (0, 0, 0): 1
}
    return RULE_197[(left, center, right)]

def rule80(left, center, right) :
    RULE_80 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 0,
    (0, 1, 0): 0,
    (0, 0, 1): 0,
    (0, 0, 0): 0
}
    
    return RULE_80[(left, center, right)]

def rule45(left, center, right) :
    RULE_45 = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 0,
    (0, 0, 0): 1
    }
    
    return RULE_45[(left, center, right)]

def rule129(left, center, right) :
    RULE_129 = {
    (1, 1, 1): 1,
    (1, 1, 0): 0,
    (1, 0, 1): 0,
    (1, 0, 0): 0,
    (0, 1, 1): 0,
    (0, 1, 0): 0,
    (0, 0, 1): 0,
    (0, 0, 0): 1
    }
    
    return RULE_129[(left, center, right)]

def rule73(left, center, right) :
    RULE_73 = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 0,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 0,
    (0, 0, 1): 0,
    (0, 0, 0): 1
    }
    
    return RULE_73[(left, center, right)]

def rule54(left, center, right) :
    RULE_54 = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 1,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 0,
    (0, 0, 1): 1,
    (0, 0, 0): 1
    }
    
    return RULE_54[(left, center, right)]








#Initializes an empty array set with a specified number of bits that the user wants to work with.
def initialize_ca(size,tbit):
    try:
        cells=np.zeros(size, dtype=int)
        cells[tbit]=1
        logins.info('INITIALIZE_CA','CALLED')
        return cells
    
    except:
        logins.critical('INITIALIZE_CA','ERROR IN CALLING')



#updates the selected cell based on the array's previous states
def update_cells(cells):

    try:
        rule_randomizer_int=0
        new_cells = np.zeros_like(cells)

    
        for i in range(1, len(cells) - 1):

            #this selects a random number and based on that number, a rule is selected for state updation
            rule_randomizer_int=random.randint(0,9)
            if rule_randomizer_int==0:

                new_cells[i] = rule30(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==1:
                new_cells[i] = rule90(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==2:
                new_cells[i] = rule115(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==3:
                new_cells[i] = rule110(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==4:
                new_cells[i] = rule197(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==5:
                new_cells[i] = rule80(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==6:
                new_cells[i] = rule129(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==7:
                new_cells[i] = rule45(cells[i - 1], cells[i], cells[i + 1])
            
            elif rule_randomizer_int==8:
                new_cells[i] = rule73(cells[i - 1], cells[i], cells[i + 1])

            elif rule_randomizer_int==9:
                new_cells[i] = rule54(cells[i - 1], cells[i], cells[i + 1])

        return new_cells
        
    except:
        logins.critical('UPDATE_CELL','ERROR IN CALLING')


 #generates a pseudo random number based on the binary number that is extracted from the final array from the update_cell module.           
def generate_psn(size,nbit, target_bit):
    try:
        cells=initialize_ca(size,target_bit)
        bit_stream=[]
        probar_count=0
        for _ in range(nbit):
            temp_cell=update_cells(cells)
            bit_stream+=[temp_cell[target_bit],]
            probar_count+=(100/nca_limit)   #this updates the progress bar based on the current number of iterations completed.
            window['-PROGRESS-'].update(probar_count)

        window.close()
        logins.info('GENERATE_PSN','CALLED')
        return bit_stream

    except:
        logins.critical('GENERATE_PSN','ERROR IN CALLING')



        

    


#GUI specifications for the opening window. Window closes when a psn is generated.
title_bar = [
    [sg.Text('Encrypter', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
     ]
]


layout = [[sg.Column(title_bar, background_color='#2e756a')], [sg.Image(filename=image_path )], 
    [sg.Text('Cellular Automata Maker')], 
    [sg.ProgressBar(max_value=100, orientation='h', size=(20, 20), key='-PROGRESS-')],
    [sg.Button('Start'), sg.Button('Exit')] , [sg.Text('Enter the number of iterations(minimum 50): '), sg.InputText(key='-ITER-')] ]


window = sg.Window('Encrypter', layout, no_titlebar=True)


while True:
    event, values = window.read()


    if event == sg.WIN_CLOSED:

        break
    elif event == 'Exit':
        sys.exit()



    elif event == 'Start':
        try:
            nca_limit=int(values['-ITER-'])
        except: 
            nca_limit=10000
        
        

       
        size=101
        tbit=size//2
 
        ngen=generate_psn(size,nca_limit,tbit)
        pseudo_random_number = int("".join(map(str, ngen)), 2)




storage_pseudo_random_number=storage_enc()







#key packer for the program
def enc_key_packer(key_arr):
    try:
        if type(key_arr) == list:
            key_arr=key_arr
        elif type(key_arr) == int:
            key_arr=list(str(key_arr))
        packed_key=''
        for i in range(len(key_arr)):
            packed_key+=str(key_arr[i])+"|"

        logins.info('ENC_KEY_PACKER','CALLED')
        return packed_key[:len(packed_key)-1]

    except:
        logins.warning('ENC_KEY_PACKER','ERROR IN CALLING')


def accuracy_checker(in_arr, out_arr, prim_len):
    
    vote=0
    for i in range(prim_len):
        if in_arr[i]!=out_arr[i]:
            vote+=1

    print("Inaccuracy percentage : ",(vote/prim_len)*100 ,'%')
    return None




#Encryption function for Images with non zero r,g,b values.
def image_encrpt_decrypt(pseudo_random_number,unenc_key_arr):
    try:

    #Important information: The pseudo random number must be in integer format and the unenc_key_arr argument must recieve only list objects.

        #this takes a new psn and either pads it if it is too small for the working array set or trims it if it is too large.
        if len(unenc_key_arr)>=len(str(pseudo_random_number)):
            temp=len(unenc_key_arr)//len(str(pseudo_random_number))
            rem=pseudo_random_number-int(temp*(str(pseudo_random_number)))
            pseudo_random_number=temp*(str(pseudo_random_number))+rem

        else:
            pseudo_random_number=int(str(pseudo_random_number)[:len(unenc_key_arr)])

            
        def encrypter(enc_len,enc_text, psn):
            enc_out=[]
            for i in range(enc_len):
                enc_out+=[int(enc_text[i]) ^ int(psn[i])]


            return enc_out
        
        print("The raw rgb pixel values are: ",unenc_key_arr)

        print("The encrypted rgb pixel values are : ",encrypter(len(unenc_key_arr),unenc_key_arr,pseudo_random_number))

        logins.info('IMAGE_ENC_DENC_INTERNAL', 'CALLED')

    except:
        logins.warning('IMAGE_ENC_DENC_INTERNAL','ERROR IN CALLING')



#Text encryption function that takes a psn and the working array set and encrypts it.
def text_encrypt_decrypt(pseudo_random_number,unenc_key_arr):


    #Important information: The pseudo random number must be in integer format and the unenc_key_arr argument must recieve only list objects.


    try:
        #read the description in image encryption module
        prim_len=len(unenc_key_arr)
        


        
        if len(unenc_key_arr)>=len(str(pseudo_random_number)):

            temp=len(unenc_key_arr)//len(str(pseudo_random_number))
            rem=pseudo_random_number-int(temp*(str(pseudo_random_number)))
            pseudo_random_number=temp*(str(pseudo_random_number))+rem
            print(pseudo_random_number)
        else:

            pseudo_random_number=int(str(pseudo_random_number)[:len(unenc_key_arr)]
                                    )

        print(pseudo_random_number)
        enc_list=[]
        for i in range(len(unenc_key_arr)):
            enc_list+=[unenc_key_arr[i]^int(str(pseudo_random_number)[i]),]



        fin=""
        for i in enc_list:
            fin+=chr(i)

        print("\nThe encrypted data is thus: ",fin)

        un_encrypted_ls=[]
        for i in range(len(unenc_key_arr)):
            un_encrypted_ls+=[enc_list[i]^int(str(pseudo_random_number)[i])]

        res=""

        for i in un_encrypted_ls:
            res+=chr(i)

        accuracy_checker(unenc_key_arr,un_encrypted_ls, prim_len)
        print(len(res))
        print("\nThe un-encrypted data is thus: ",res)
        logins.info('TEXT ENC_DENC_INTERNAL','CALLED')
        enc=encoded_file_storage(r'C:\Users\chestor\Desktop\enc_text.pxe',storage_pseudo_random_number)
        enc.encode(enc_list)
 
    except:
        logins.warning('TEXT ENC_DENC_INTERNAL','ERROR IN CALLING')




#Signature encryption and decryption module that takes a psn(key) and a working data set in array form and encrypts as well as decrypts it.
def signature_encrypt_decrypt(pseudo_random_number, unenc_key_arr, height, width, raw_image_path):



    try:






    

        prim_len=len(unenc_key_arr)
        sbox_arr=sbox(height,width)
        packed_secondary_key=enc_key_packer(sbox_arr)

        layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
                [sg.Button('Go'), sg.Button('Exit')]]
            
        window = sg.Window('Select your secondary encryption key file', layout)
        event,values = window.read()
        file_path = values['-IN-']
        window.close()
        

        primary_key_enc_storage=encoded_file_storage(file_path,storage_pseudo_random_number)
        primary_key_enc_storage.encode(sbox_arr)
            


        if prim_len>=len(str(pseudo_random_number)):
            temp=prim_len//len(str(pseudo_random_number))
            rem=prim_len-temp*(len(str(pseudo_random_number)))
            pseudo_random_number=temp*(str(pseudo_random_number))+rem*"0"

        else:
            pseudo_random_number=int(str(pseudo_random_number)[:len(unenc_key_arr)])
            
        packed_primary_key=enc_key_packer(pseudo_random_number)

        layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
                        [sg.Button('Go'), sg.Button('Exit')]]
                
        window = sg.Window('Select your primary encryption key file', layout)
        event,values = window.read()
        file_path = values['-IN-']
        window.close()
        temp_key=str(pseudo_random_number)
        print(len(list(temp_key)))

        primary_key_enc_storage=encoded_file_storage(file_path,storage_pseudo_random_number)
        primary_key_enc_storage.encode(temp_key)
        

        
        enc_key_arr=[]
        for i in range(prim_len):
            enc_key_arr+=[unenc_key_arr[i]^int(str(pseudo_random_number)[i]),]


        enc_dict_pck={}
        for i in range(prim_len):
            enc_dict_pck[sbox_arr[i]]=enc_key_arr[i]

        

        

        enc_np_arr=np.array(sbox_arr)

        enc_image=enc_np_arr.reshape((height,width))
        enc_image=enc_image.astype(np.uint8)
        





        unenc_arr=[]
        for i in range(prim_len):
            unenc_arr+=[enc_dict_pck[sbox_arr[i]],]
        
        for i in range(len(unenc_key_arr)):
            unenc_arr[i]=[enc_key_arr[i]^int(str(pseudo_random_number)[i]),]
        

        accuracy_checker(unenc_key_arr,unenc_arr, prim_len)
        unenc_np_arr=np.array(unenc_arr)
        print(len(unenc_np_arr))
        unenc_image=unenc_np_arr.reshape((height,width))
        unenc_image=unenc_image.astype(np.uint8)
        cv2.imshow("Encrypted signature",enc_image)
        cv2.imshow("Un- Encrypted signature", unenc_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        postext=enc_key_packer(sbox_arr)
        logins.info('SIGNATURE ENC DENC INTERAL', 'CALLED')
        print('hello')
        enc=encoded_file_storage(r'C:\Users\chestor\Desktop\enc_signature.pxe',storage_pseudo_random_number)
        enc.encode(enc_key_arr)
        window.close()
        AI_response= custom_popup_yes_no("Do you wish to run AI(CNN) on the signature to check if it is forged?")
        if AI_response == 'Yes':
            secret = pyotp.random_base32()
            print(f"Secret Key: {secret}")


            totp = pyotp.TOTP(secret)


            qr_url = totp.provisioning_uri(name="Sirsimonjerkalot", issuer_name="ssenc")
            qr = qrcode.make(qr_url)
            qr.save("qrcode.png")
            qr_path = resource_path('qrcode.png')
            title_bar = [
                [sg.Text('QR code', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                ]
                        ]
            layout= [[sg.Column(title_bar, background_color='#2e756a')],
                    [sg.Image(qr_path)]
                     , [sg.Text('Enter the OTP generated by your authenticator app please:  '), sg.InputText(key='-ITER-')] ,
                       [sg.Button('Start'), sg.Button('Exit')] ]
            window= sg.Window('Your qr code',layout, no_titlebar=True)
            event, values= window.read()
            if event == 'Start':

                window.close()
                
                print("QR code saved as 'qrcode.png'. Scan this with your 2FA app.")


                user_otp = values[ '-ITER-']
                if totp.verify(user_otp):
                    print("OTP is valid!")
                    
                    
                    class RedirectOutput:
                        def __init__(self, output_element):
                            self.output_element = output_element

                        def write(self, message):
                            
                            self.output_element.update(message, append=True)

                        def flush(self):
                            pass 



                    layout = [
                        [sg.Text("Terminal Output")],
                        [sg.Multiline(size=(80, 20), key="output", disabled=True, autoscroll=True)],
                        [sg.Button("Start"), sg.Button("Exit")],
                    ]

                
                    window = sg.Window("AI prediction terminal", layout, finalize=True)

                
                    output_element = window["output"]
                    sys.stdout = RedirectOutput(output_element)

                
                    while True:
                        event, values = window.read(timeout=10) 

                        if event == sg.WINDOW_CLOSED or event == "Exit":
                            break
                        elif event == "Start":
                            print("hello")
                            AI_differen_func(raw_image_path= raw_image_path)
                        


                 
                    sys.stdout = sys.__stdout__
                    window.close()

                else:
                    print("Invalid OTP. Please try again.")
            elif event == 'Exit':
                sys.exit()


        else:
            print('Fatal error!!')
        sys.exit()

    

    except:
        logins.warning('SIGNATURE ENC DENC INTERNAL','ERROR IN CALLING')




def signature_bonafide_checker(comp_path_1,comp_path_2):
    try:
        agg_difference_pcnt=0
        prim_sig_arr_len=len(comp_path_1)
    

        for i in range(prim_sig_arr_len):
            if comp_path_2[i]-comp_path_1[i]!=0:
                agg_difference_pcnt+=1


        print((agg_difference_pcnt/prim_sig_arr_len)*100, 'percent mismatch')
        logins.warning('SIGNO_BONAFIDE_CHK','CALLED')
    
    except:
        logins.warning('SIGNO_BONAFIDE_CHK','ERROR IN CALLING')













#Main function
def main():
    sg.theme("DarkTeal10")


    layout = [
    [sg.Text('Please select the type of data you want to encrypt :')],
    [sg.Radio('Text Encryption', 'RADIO1', key='te', size=(40)), sg.Radio('Image encryption', 'RADIO1', key='ie', size=40), sg.Radio('Signature encryption', 'RADIO1', key='sige' , size=40) , sg.Radio('Signature bonafide checker', 'RADIO1', key='sbe', size=40) ],
    
    [sg.Button('Submit'), sg.Button('Cancel') ]
    ]

    
    window = sg.Window( "new window", layout, no_titlebar=True)
    event , vals= window.read()




    for k in vals:
        if  k=='te' and vals[k]==True :
            stat_inp=1
   
        elif k=='ie' and vals[k]==True :
            stat_inp=2
        elif k=='sige' and vals[k]==True :
            stat_inp=3
        elif k == 'sbe' and vals[k] == True:
            stat_inp=4



    if stat_inp==2:
        try:
            path=img_inp_method(str(input("Please enter the path of your image: \n")))
            unenc_key_arr=img_inp_method(path)
            image_encrpt_decrypt(pseudo_random_number,unenc_key_arr)
            logins.info('STAT INP IMG', 'CALLED')
        
        except:
            logins.critical('STAT INP IMG','ERROR IN CALLING STAT INP')


    elif stat_inp==1:
        
        try:
            layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
            [sg.Button('Go'), sg.Button('Exit')]]

            #choose your input file here
            window = sg.Window('Select your input file', layout)
            event,values = window.read()
            file_path = values['-IN-']
            with open(file_path, 'r') as file:
                content = file.read()
            window.close()
           
           #preview the file
            title_bar = [
                [sg.Text('Text Preview', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                ]
                        ]

            layout = [
                [sg.Text('Do you wish to use this text?', font=('Helvetica', 16))],
                [sg.Multiline(content, size=(80, 20), font=('Courier New', 12), disabled=True)],
                [sg.Yes(), sg.No()]
    ]

            window = sg.Window('Text File Preview', layout, resizable=True, finalize=True)
            event, values= window.read()
    


            if event=='Yes':

                unenc_key_arr=text_inp_method(str(content))
                
                temp_key=str(pseudo_random_number)[:len(unenc_key_arr)]


                layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
                          [sg.Button('Go'), sg.Button('Exit')]]
                
                window = sg.Window('Select your encryption key file', layout)
                event,values = window.read()
                file_path = values['-IN-']
                key_enc_storage=encoded_file_storage(file_path,storage_pseudo_random_number)
                key_enc_storage.encode(temp_key)


    
                



               
                text_encrypt_decrypt(pseudo_random_number,unenc_key_arr)
                logins.info('STAT INP TXT', 'CALLED')
          
            else:
                sys.exit()

        except:
            logins.critical('STAT INP TXT','ERROR IN CALLING STAT INP')

    elif stat_inp==3:


        try:
            layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
            [sg.Button('Go'), sg.Button('Exit')]]


            window = sg.Window('File Browser', layout)
            event,values = window.read()
            file_path = values['-IN-']
            window.close()
            
            title_bar = [
                [sg.Text('Signature Preview', background_color='#2e756a', text_color='white', pad=(10, 0), size=(30, 1)),
                ]
                        ]

            layout= [[sg.Column(title_bar, background_color='#2e756a')],
                    [sg.Image(file_path)],
                    [sg.Text('Do you wish to use this signature?')],
                    [sg.Yes() , sg.No()]]
            
            window= sg.Window('Preview Signature',layout, no_titlebar=True)
            event, values= window.read()
    
        

            if event== 'Yes':

                height,width, unenc_key_arr=signo_inp_method(file_path)

                signature_encrypt_decrypt(pseudo_random_number,unenc_key_arr, height, width, raw_image_path=file_path)
            else:
                sys.exit()
            
            logins.info('STAT INP SIGNATURE', 'CALLED')

        except:
            logins.critical('STAT INP SIGNATURE','ERROR IN CALLING STAT INP')



    elif stat_inp==4:
        layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
        [sg.Button('Go'), sg.Button('Exit')]]


        window = sg.Window('First Signature', layout)
        event,values = window.read()
        _comp_path_1 = values['-IN-']
        window.close()

        layout = [[sg.Input(key='-IN-'), sg.FileBrowse()],
        [sg.Button('Go'), sg.Button('Exit')]]


        window = sg.Window('Second Signature', layout)
        event,values = window.read()
        _comp_path_2 = values['-IN-']
        window.close()
        sig_comp_arr_1=signo_inp_method(_comp_path_1)[2]
        sig_comp_arr_2=signo_inp_method(_comp_path_2)[2]
        signature_bonafide_checker(sig_comp_arr_1,sig_comp_arr_2)
        

    sys.exit()
try:
    if __name__=="__main__":
        main()
        logins.info('MAIN', 'CALLED')

except:
    logins.critical('MAIN', 'CRITICAL ERROR IN CALLING MAIN')
    sys.exit()







