import PySimpleGUI as sg
from utils import convert_to_bytes

#sg.popup('Hello World')
#sg.popup_error('This is an error')
# result = sg.popup_get_text("Please enter your name")
# print(result)

# fs = sg.popup_get_file('please choose a file')
# print(fs)

# layout = [[sg.Text('Please enter your name')],
#           [sg.Input(key='-IN-')],
#           [sg.Ok(), sg.Cancel()]]
# window = sg.Window('pop up get text', layout)
# events, values = window.read()
# print(events, values)

# layout = [[sg.T('User Name', size=(10, 1)), sg.I(key='-USER-')]]
# layout += [[sg.T('Password', size=(10, 1)), sg.I(key='-PASS-', password_char='*')]]
# layout += [[sg.Ok(), sg.Cancel()]]
# window = sg.Window('Login', layout)
# while True:
#     event, values = window.read()
#     if event == 'Cancel' or event == sg.WIN_CLOSED:
#         break
#     if event == 'Ok':
#         if not values['-USER-'] or not values['-PASS-']:
#             sg.popup_error('Invalid username or password')
#         else:
#             print('Valid identity')
#     print(event, values)

# sg.theme('DarkBlue')
# layout = [[sg.T('Please select a file')],
#           [sg.I(key='-IMG-', enable_events=True), sg.FileBrowse(file_types=(('All Files', ['*.jpeg', '*.jpg', '*.png']),
#                                                         ('JPEG', '*.jpeg'), ('jpg', '*.jpg'), ('PNG', '*.png')))],
#           [sg.Image(key='-PHOTO-', size=(300, 300))],
#           [sg.Combo(['US', 'England', 'France'], default_value='US'),
#            sg.Checkbox('check', key='-CHK-', enable_events=True),
#            sg.Ok(), sg.Cancel(), sg.Button('Clear')]]
#
# window = sg.Window('Image Browser', layout)
#
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':
#         break
#     elif event == '-IMG-':
#        window['-PHOTO-'].update(data=convert_to_bytes(values['-IMG-'], resize=(300, 300)))
#     elif event == 'Clear':
#         window['-CHK-'].update(not values['-CHK-'])
#     print(event, values)
menu = [['File', ['Open', 'Save', 'Exit']],
        ['Edit', ['Cut', 'Copy']]]

left_layout = [[sg.Combo(values=['Left', 'Left1'])],
               [sg.Check('Options')]]
right_layout = [[sg.Combo(values=['Right', 'Right1'])],
               [sg.Check('Options')]]

layout = [[sg.Menu(menu)],
          [sg.Frame("Left", left_layout),sg.VSep(), sg.Col(right_layout)]]
window = sg.Window('Cols', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    print(event, values)