def timezone_not_synced():
    import PySimpleGUI as sg
    import sys
    sg.popup('Time zones not synced. Please set system time to run the application', title='timezone desync error', no_titlebar= True)
    sys.exit()
    return False
    

timezone_not_synced()