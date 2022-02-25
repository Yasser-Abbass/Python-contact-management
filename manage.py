import bcrypt
from mongoengine import connect
from models import User, Contact
from faker import Faker
from utils import get_person
import asyncio
import shutil


def create_user(username, password, email):
    user = User()
    hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user.username = username
    user.password = hashAndSalt
    user.email = email
    user.save()


def login_user(username, password):
    user = User.objects(username=username).first()
    if user:
        if bcrypt.checkpw(password.encode(), user.password):
            return True
    return False


def query_user(username):
    user = User.objects(username=username).first()
    return user


def list_users():
    users = User.objects()
    return users


def delete_user(username):
    user = query_user(username)
    user.delete()


def create_admin():
    if not query_user('admin'):
        create_user('admin', 'password', 'admin@gmail.com')
    else:
        print('User already exist')


def create_contact(firstname, lastname, address, phone, mobile, email, gender, occupation, age, photo):
    contact = Contact()
    contact.firstname = firstname
    contact.lastname = lastname
    contact.address = address
    contact.phone = phone
    contact.mobile = mobile
    contact.email = email
    contact.gender = gender
    contact.occupation = occupation
    contact.age = age
    contact.photo = photo
    contact.save()


def list_contacts():
    contacts = Contact.objects()
    return contacts


def query_contact(email):
    contact = Contact.objects(email=email).first()
    return contact


def delete_contact(email):
    contact = query_contact(email)
    contact.delete()


def edit_contact(cont, firstname, lastname, address, phone, mobile, email, gender, occupation, age, photo):
    contact = cont
    contact.firstname = firstname
    contact.lastname = lastname
    contact.address = address
    contact.phone = phone
    contact.mobile = mobile
    contact.email = email
    contact.gender = gender
    contact.occupation = occupation
    contact.age = age
    contact.photo = photo
    contact.save()


def create_contacts(num):
    fake = Faker()
    contacts = []
    for i in range(num):
        contact = Contact()
        contact.firstname = fake.first_name()
        contact.lastname = fake.last_name()
        contact.address = fake.address()
        contact.phone = fake.phone_number()
        contact.mobile = fake.phone_number()
        contact.email = fake.email()
        contact.age = fake.random_int(20, 60)
        contact.gender = fake.random_element(['Male', 'Female'])
        contact.occupation = fake.profile()['job']
        photo = asyncio.run(get_person()).split('/')[-1]
        contact.photo = 'imageDB/'+photo
        shutil.move('images/'+photo, 'imageDB/'+photo)
        contacts.append(contact)
    Contact.objects.insert(contacts)


connect('Contacts')