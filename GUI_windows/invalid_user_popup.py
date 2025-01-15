def invalid_user_gui():

    sg.popup('Username not found', title='Username error', no_titlebar= True)
    sys.exit()
    return False
    


invalid_user_gui()