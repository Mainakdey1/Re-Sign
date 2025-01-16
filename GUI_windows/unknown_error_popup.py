def unknown_error():

    import PySimpleGUI as sg
    import sys
    sg.popup('An unknown error has occured. Please restart the application. If the issue persists, consult the log files.', title='unknown error', no_titlebar= True)
    sys.exit()
    return False
    

unknown_error()