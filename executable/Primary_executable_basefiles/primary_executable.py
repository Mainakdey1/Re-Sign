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

#gets the filepath of the current file the program is in
file=sys.argv[0]
 
str_to_int_limits=100000  #sets the string to integer conversion limit to a specified number
nca_limit=10000  
size=101
tbit=size//2
stat_inp=0


dir_pathV= expanduser("~")+"\\"    #saves log file directly to the current working directory
sg.theme('DarkTeal10')             #sets the global gui color for the program
url='https://raw.githubusercontent.com/Mainakdey1/Image-Encryption-using-Cellular-Automata-Draft/executable/Primary_executable_basefiles/primary_executable.py'


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


image_path = resource_path('dark.png')




start_time=time.time()
sys.set_int_max_str_digits(str_to_int_limits)


#new_vers=107
__version__=0.107




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
def signature_encrypt_decrypt(pseudo_random_number, unenc_key_arr,height, width):



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

                signature_encrypt_decrypt(pseudo_random_number,unenc_key_arr,height,width)
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







