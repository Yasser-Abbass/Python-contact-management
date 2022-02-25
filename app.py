import shutil
import PySimpleGUI as sg
from manage import *
from utils import convert_to_bytes


def create_user_gui():
    layout = [[sg.T('User Name', size=(10, 1)), sg.I(key='-USER-')],
              [sg.T('Password', size=(10, 1)), sg.I(key='-PASS-', password_char='*')],
              [sg.T('Email', size=(10, 1)), sg.I(key='-EMAIL-')],
              [sg.Ok(), sg.Cancel()]]
    window = sg.Window('Create User', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif event == 'Ok':
            username = values['-USER-']
            password = values['-PASS-']
            email = values['-EMAIL-']
            create_user(username, password, email)
            window.close()


def list_users_gui():
    layout = []
    users = list_users()
    idx = 0
    for user in users:
        row = [[sg.CB('', key=f'-ID-{idx}', enable_events=True),
                sg.I(user.username, key=f'-USER-{idx}', disabled=True, size=(20, 1), text_color='black'),
                sg.I(user.email, disabled=True, size=(20, 1), text_color='black')]]
        layout.append(row)
        idx += 1
    layout += [[sg.B('Delete'), sg.Cancel()]]
    selected = []
    window = sg.Window('User Management', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif '-ID-' in event:
            if values[event]:
                selected.append(event)
            else:
                selected.remove(event)
        elif event == 'Delete':
            for item in selected:
                delete_user(values[f'-USER-{item.split("-")[-1]}'])
            window.close()


def delete_user_gui():
    username = sg.popup_get_text("Please enter user name")
    user = query_user(username)
    if user:
        response = sg.popup_ok_cancel("Are you sure?")
        if response:
            delete_user(username)
    else:
        sg.popup_error("User does not exist")


def create_contact_gui(contact=None):
    sg.set_options(element_padding=(5, 10))
    left_layout = [[sg.T('First Name', size=(10, 1)), sg.I(key='-FIRST-', size=(50, 1))],
              [sg.T('Last Name', size=(10, 1)), sg.I(key='-LAST-', size=(50, 1))],
              [sg.T('Address', size=(10, 1)), sg.I(key='-ADD-', size=(50, 1))],
              [sg.T('Phone', size=(10, 1)), sg.I(key='-PHONE-', size=(18, 1)),
               sg.T('Mobile', size=(9, 1)), sg.I(key='-MOB-', size=(18, 1))],
              [sg.T('Email', size=(10, 1)), sg.I(key='-EMAIL-', size=(50, 1))],
              [sg.T('Occupation', size=(10, 1)), sg.I(key='-OCC-', size=(50, 1))],
              [sg.T('Gender', size=(10, 1)), sg.Combo(values=['Male', 'Female'], key='-GEN-', default_value='Male')],
              [sg.T('Age', size=(10, 1)), sg.Slider(key='-AGE-', orientation='h', range=(16, 60),size=(38, 20),
                                                    default_value=20)],
              ]
    right_layout = [[sg.T('Select Image'),
                     sg.I(key='-IMG-', enable_events=True),
                     sg.FileBrowse(file_types=(('All Files', ['*.jpg', '*.jpeg', '*.png']),
                                               ("JPEG Files", "*.jpeg"),
                                               ("JPG Files", "*.jpg"),
                                               ("PNG Files", "*.png")))],
                    [sg.Image(key='-PHOTO-', data=convert_to_bytes('res/placeholder-image.png', resize=(300, 300)))]]
    layout = [[sg.Frame("Contact Data", left_layout, vertical_alignment='center', pad=((10, 10), (10, 10))),
               sg.VerticalSeparator(), sg.Col(right_layout, element_justification='center')],
              [sg.B('Save' if contact else 'Add', enable_events=True), sg.Cancel()]]
    window = sg.Window('Create Contact', layout, finalize=True)

    if contact:
        window['-FIRST-'].update(contact.firstname)
        window['-LAST-'].update(contact.lastname)
        window['-ADD-'].update(contact.address)
        window['-PHONE-'].update(contact.phone)
        window['-MOB-'].update(contact.mobile)
        window['-EMAIL-'].update(contact.email)
        window['-OCC-'].update(contact.occupation)
        window['-GEN-'].update(contact.gender)
        window['-AGE-'].update(contact.age)
        if contact.photo:
            photo = contact.photo
        else:
            photo = 'res/placeholder-image.png'
        window['-PHOTO-'].update(data=convert_to_bytes(photo, resize=(300, 300)))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            window.close()
            break
        elif event == '-IMG-':
            window['-PHOTO-'].update(data=convert_to_bytes(values['-IMG-'], resize=(300, 300)))
        elif event == 'Add' or event == 'Save':
            firstname = values['-FIRST-']
            lastname = values['-LAST-']
            address = values['-ADD-']
            phone = values['-PHONE-']
            mobile = values['-MOB-']
            email = values['-EMAIL-']
            occupation = values['-OCC-']
            gender = values['-GEN-']
            age = values['-AGE-']
            _photo = values['-IMG-']
            if _photo:
                fname = _photo.split("/")[-1]
                photo = 'imageDB/'+fname
                shutil.copy(_photo, photo)
            else:
                photo = ""
            if contact:
                if _photo != "":
                    photo = _photo
                else:
                    photo = contact.photo
                edit_contact(contact, firstname, lastname, address, phone, mobile, email, gender, occupation, age, photo)
                window.close()
                break
            else:
                create_contact(firstname, lastname, address, phone, mobile, email, gender, occupation, age, photo)
            for key in values:
                if key not in ['-GEN-', 'Browse']:
                    window[key].update("")
            window['-AGE-'].update(20)
            window['-PHOTO-'].update(data=convert_to_bytes('res/placeholder-image.png', resize=(300, 300)))
        print(event, values)


def list_contacts_page(page):
    contacts = Contact.objects().paginate(page, 5)
    return contacts


def update_contacts_elements(contacts, window):
    for idx in range(5):
        if idx <= len(contacts.items)-1:
            cont = contacts.items[idx]
            if not cont.photo:
                photo = 'res/placeholder-image.png'
            else:
                photo = cont.photo
            window[f'-CON-{idx}'].update(cont.firstname + " " + cont.lastname)
            window[f'-EMAIL-{idx}'].update(cont.email)
            window[f'-IMG-{idx}'].update(data=convert_to_bytes(photo, resize=(75, 75)))
        else:
            window[f'-CON-{idx}'].update("")
            window[f'-EMAIL-{idx}'].update("")
            window[f'-IMG-{idx}'].update(data=convert_to_bytes('res/placeholder-image.png', resize=(75, 75)))
    window['-PAGE-'].update(page)
    window['<'].update(disabled=not contacts.has_prev)
    window['<<'].update(disabled=not contacts.has_prev)
    window['>'].update(disabled=not contacts.has_next)
    window['>>'].update(disabled=not contacts.has_next)


def list_contacts_gui(contacts):
    global page
    sg.set_options(element_padding=(10, 10))
    layout = []
    idx = 0
    for contact in contacts.items:
        if contact.photo:
            photo = contact.photo
        else:
            photo = 'res/placeholder-image.png'
        row = [[sg.CB("", key=f'-ID-{idx}', enable_events=True),
                sg.I(contact.firstname + " " + contact.lastname, key=f'-CON-{idx}', size=(30, 1)),
                sg.I(contact.email, size=(30, 1), key=f'-EMAIL-{idx}'),
                sg.Image(key=f'-IMG-{idx}', data=convert_to_bytes(photo, resize=(75, 75)))]]
        layout.append(row)
        idx += 1
    pagination = [[sg.B('<<', disabled=not contacts.has_prev),
                   sg.B("<", disabled=not contacts.has_prev),
                   sg.T(text=page, key='-PAGE-', size=(2, 1)),
                   sg.B(">", disabled=not contacts.has_next),
                   sg.B(">>", disabled=not contacts.has_next)
                   ]]
    buttons = [[sg.B('Edit'), sg.B('Delete', button_color='red'), sg.Cancel()]]
    layout += [[sg.Col(pagination, justification='right')]]
    layout += buttons
    selected = []
    window = sg.Window('Contacts List', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            page = 1
            window.close()
            break
        elif '-ID-' in event:
            if values[event]:
                selected.append(event)
            else:
                selected.remove(event)
        elif event == 'Edit':
            if len(selected) > 1:
                sg.popup_error("Edit is not allowed for multiple contacts")
            elif len(selected) == 1:
                contact_email = values[f'-EMAIL-{selected[0].split("-")[-1]}']
                contact = query_contact(contact_email)
                create_contact_gui(contact)
                window[selected[0]].update(not selected[0])
                selected = []
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
            else:
                sg.popup('Please select a contact')
        elif event == 'Delete':
            if len(selected) > 0:
                for item in selected:
                    contact_email = values[f'-EMAIL-{item.split("-")[-1]}']
                    delete_contact(contact_email)
                    window[item].update(not item)
                selected = []
                if Contact.objects.count() % 5 ==0:
                    page -= 1
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
        elif event == ">":
            if contacts.has_next:
                page += 1
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
        elif event == ">>":
            if contacts.has_next:
                page = contacts.pages
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
        elif event == "<":
            if contacts.has_prev:
                page -= 1
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
        elif event == "<<":
            if contacts.has_prev:
                page = 1
                contacts = list_contacts_page(page)
                update_contacts_elements(contacts, window)
        print(event, values)


def main():
    menu = [['Contacts', ['Create Contact', 'List Contacts', 'Find Contact', 'Delete Contact']],
            ['Users', ['Create User', 'List Users', 'Delete User']],
            ['Exit', ['Quit']]]
    layout = [[sg.Menu(menu)],
              [sg.Image(data=convert_to_bytes('res/contact-image.png', resize=(490, 220)), background_color="#6c69df")]]
    window = sg.Window('Contact Manager', layout, background_color='#6c69df', icon='res/contact-icon.ico')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        elif event == 'Create User':
            create_user_gui()
        elif event == 'List Users':
            list_users_gui()
        elif event == 'Delete User':
            delete_user_gui()
        elif event == 'Create Contact':
            create_contact_gui()
        elif event == 'List Contacts':
            contacts = list_contacts_page(1)
            list_contacts_gui(contacts)
        elif event == 'Find Contact':
            contact_email = sg.popup_get_text('Please enter contact email')
            contact = query_contact(contact_email)
            if contact:
                create_contact_gui(contact)
        elif event == 'Delete Contact':
            contact_email = sg.popup_get_text('Please enter contact email')
            result = sg.popup_ok_cancel('Are you sure?')
            if result == 'OK':
                delete_contact(contact_email)
        elif event == 'Exit':
            window.close()
            break


def login_user_gui():
    layout = [[sg.T('User Name', size=(10, 1)), sg.I(key='-USER-')],
              [sg.T('Password', size=(10, 1)), sg.I(key='-PASS-', password_char='*')],
              [sg.Ok(), sg.Cancel()]]
    window = sg.Window('Login', layout)
    count = 0
    while count < 3:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        elif event == 'Ok':
            username = values['-USER-']
            password = values['-PASS-']
            if login_user(username, password):
                window.close()
                main()
                break
            else:
                sg.popup_error('Invalid Username or Password')
                count += 1


if __name__ == '__main__':
    sg.theme('DarkGrey')
    page = 1
    login_user_gui()
