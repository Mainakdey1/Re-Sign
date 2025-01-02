
def sign_up_gui():

    import PySimpleGUI as sg

    # Define a custom theme for the application
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
    sg.theme('CustomSignupTheme')

    # Define the layout for the signup page
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

    # Create the window
    window = sg.Window("Signup Page", layout, size=(450, 350), element_justification='center', finalize=True)

    # Event loop
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Sign Up':
            username = values['-USERNAME-']
            password = values['-PASSWORD-']

            # Perform signup logic
            if username  and password:
                window['-MESSAGE-'].update("Account created successfully! 🎉", text_color='green')
            else:
                window['-MESSAGE-'].update("All fields are required.", text_color='red')

    # Close the window
    window.close()

sign_up_gui()