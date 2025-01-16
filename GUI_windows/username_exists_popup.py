def username_exists():

    import PySimpleGUI as sg
    import sys
    sg.popup('Username already exists. Please sign in or reset password.', title='username exists error', no_titlebar= True)
    sys.exit()
    return False
    
username_exists()