import PySimpleGUI as sg

# Define a custom theme for the window
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
sg.theme('CustomTheme')

# Define the layout for the login page
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

# Create the window
window = sg.Window("Login Page", layout, size=(450, 300), element_justification='center', finalize=True, no_titlebar=True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break
    elif event == 'Login':
        username = values['-USERNAME-']
        password = values['-PASSWORD-']

        # Login validation logic
        if username == "admin" and password == "1234":
            window['-MESSAGE-'].update("Login successful! 🎉", text_color='green')
        else:
            window['-MESSAGE-'].update("Invalid username or password.", text_color='red')
    elif event == '-FORGOT-':
        window.close()
        sg.popup("Forgot Password", "Please contact support to reset your password.", font=("Helvetica", 12))

    elif event == '-NEW-':
        window.close()
        print('new person sheesh')

# Close the window
window.close()
