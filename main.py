import datetime
import time
import json
from json import JSONDecodeError
from os import path

def loading():
    time.sleep(1)
    print(f'****************************\n'
          f'Loading..\n'
          f'Return to the main menu\n')
    time.sleep(2)

def search(value, is_null=True):
    if value.isdigit() or is_null and not value:
        return False
    return True

def string_valid(value, is_null=True):
    if value.isdigit() or is_null and not value:
        return False
    return True

def gender_valid(sex):
    sex_choices = ['male', 'female', 'other', 'm', 'f', 'o', 'м', 'ж']
    if sex.lower() in sex_choices:
        return True

    return False

def date_valid(entry_date):
    entry_date = entry_date.replace('.', '/').replace(',', '/').replace('-', '/').replace(' ', '/')
    validate_result = {'status': True}

    try:
        date = datetime.datetime.strptime(entry_date, "%d/%m/%Y")
        validate_result.update({'date': date})
    except Exception:
        validate_result.update({'status': False, 'error': 'Not valid date!'})
        return validate_result

    return validate_result

def write_data_to_json(input_data):
    try:
        with open('user_data.json', mode='r', encoding='utf-8') as f:
            feeds = json.load(f)

        if feeds is dict:
            feeds = [feeds]

        with open('user_data.json', mode='w', encoding='utf-8') as feedsjson:
            feeds.append(input_data)
            json.dump(feeds, feedsjson)

    except JSONDecodeError:
        f = open('user_data.json', 'w')
        json.dump([], f)
        f.close()

def record_data():
    print('FULL NAME')
    name = input('  *Name: ')
    while not string_valid(name):
        print(f'The name "{name}" is incorrectly, please try again..')
        name = input('\t*Name: ')

    surname = input('  *Surname: ')
    while not string_valid(surname, is_null=False):
        print(f'The surname "{surname}" is incorrectly, please try again..')
        surname = input('\t*Surname: ')

    patronymic = input('  *Patronymic: ')
    while not string_valid(patronymic, is_null=False):
        print(f'The patronymic "{patronymic}" is incorrectly, please try again..')
        patronymic = input('\t*Patronymic: ')

    date_of_birth = input('*Date of birth (d-m-y): ')
    while not date_valid(date_of_birth)['status']:
        print(f'Date of birth "{date_of_birth}" is incorrectly, please try again..')
        date_of_birth = input('*Date of birth (d-m-y): ')

    date_of_death = input('*Date of death (d-m-y or "-"): ')
    if date_of_death in ('', '-'):
        pass
    else:
        while not date_valid(date_of_death)['status']:
            if date_of_death in ('', '-'):
                print(f'Date of death "{date_of_death}" is incorrectly, please try again..')
                date_of_death = input('*Date of death (d-m-y): ')

    sex = input('*Sex (male/female/other): ')
    while not gender_valid(sex):
        print(f'The gender "{sex}" is incorrectly, please try again')
        sex = input('*Sex (male/female/other): ')

    input_data = {'Name': name, 'Surname': surname, 'Patronymic': patronymic,
                  'Date of birth': date_of_birth, 'Date of death': date_of_death, 'Sex': sex}

    if path.isfile('user_data.json') is False:
        f = open('user_data.json', 'x')
        json.dump([], f)
        f.close()
        write_data_to_json(input_data)
    else:
        write_data_to_json(input_data)

    loading()

def find_data():
    search_line = input('Enter the full name or part of the name: ')
    while not search(search_line):
        print(f'The value "{search_line}" is incorrectly, please try again..')
        search_line = input('Enter the full name or part of the name: ')

    try:
        persons = json.load(open('user_data.json', encoding='utf-8'))
        for person in persons:
            person_data = person.values()
            for person_info in person_data:
                if search_line.lower() in person_info.lower():
                    print(person)
                    break
            else:
                print('Found: 0')
    except FileNotFoundError:
        print('! First, create a file \n')

    loading()

def calculate_person_age():
    date = input('Choose your date: ')
    validate_result = date_valid(date)
    if validate_result['status']:
        now_date = datetime.datetime.now()
        user_age = now_date.year - validate_result['date'].year
        if now_date.month < validate_result['date'].month or \
                now_date.month == validate_result['date'].month and \
                now_date.day < validate_result['date'].day:
            user_age -= 1
        print(f'Age: {user_age} \n')
    else:
        print(validate_result['error'])

    loading()

call_function = {1: record_data, 2: find_data, 3: calculate_person_age}

def main():
    while True:

        print(f'****************************\n'
              f'1.Write information about a person\n'
              f'2.Get information about a person\n'
              f'3.Find out the age of a person\n'
              f'4.Exit\n'
              f'****************************\n')

        choice = input('Make your choice: ')

        if not choice.isdigit() or int(choice) > 4 or not choice:
            print('! Input error, please try again.. \n')
            continue

        choice_int = int(choice)
        if choice_int == 4:
            print('Goodbye...')
            break
        else:
            call_function[choice_int]()
main()