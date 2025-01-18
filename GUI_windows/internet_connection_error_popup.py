def internet_connection_error_popup():

    import PySimpleGUI as sg
    import sys
    sg.popup('No internet connection found. Please restart the application after connecting to a stable internet network.', title='unknown error', no_titlebar= True)
    sys.exit()
    return False
    

internet_connection_error_popup()