import datetime
import json
from json import JSONDecodeError
from os import path


# def menu(user_choice=None):
#     if user_choice == '1':
#         add_new_user_info()
#     elif user_choice == '2':
#         search_user()
#     elif user_choice == '3':
#         calculate_user_age()
#     print(f'****************************\n'
#           f'1.Write new data about user\n'
#           f'2.Search user\n'
#           f'3.User Age\n'
#           f'****************************\n')


def record_data():
    print('FULL NAME')
    name = input(' *Name: ')
    surname = input(' *Surname: ')
    patronymic = input(' *Patronymic: ')
    date_of_birth = input(' *Date of birth (d-m-y): ')
    date_of_death = input(' *Date of death (d-m-y or "-"): ')
    sex = input(' *Sex: ')
    input_data = {'Name': name, 'Surname': surname, 'Patronymic': patronymic, 'Date of birth': date_of_birth, 'Date of death': date_of_death, 'Sex': sex}

    if path.isfile('user_data.json') is False:
        f = open("user_data.json", "x")
        json.dump([], f)
        f.close()
    else:
        try:
            with open("user_data.json", mode='r', encoding='utf-8') as f:
                feeds = json.load(f)

            if feeds is dict:
                feeds = [feeds]

            with open("user_data.json", mode='w') as feedsjson:
                feeds.append(input_data)
                json.dump(feeds, feedsjson)

        except JSONDecodeError:
            f = open("user_data.json", "w")
            json.dump([], f)
            f.close()

def find_data():
    search_line = input('Enter the full name or part of the name: ')
    persons = json.load(open('user_data.json'))

    for person in persons:
        person_datas = person.values()
        for person_info in person_datas:
            if search_line.lower() in person_info.lower():
                print(person)

def change_and_validate_date(date_in_text):
    date_in_text = date_in_text.replace('.', '/')  # 12/10/2000
    splitted_date = date_in_text.split('/')  # ['12', '10', '2000']
    validate_result = {'status': True}
    try:
        date = datetime.datetime.strptime(date_in_text, "%d/%m/%Y")
        validate_result.update({'date': date})
    except:
        validate_result.update({'status': False, 'error': 'Not valid date!'})
        return validate_result
    for number in splitted_date:
        try:
            number = int(number)
        except:
            validate_result.update({'status': False, 'error': 'Not valid date!'})
            break

    return validate_result


def calculate_user_age():
    date = input('Choose your date: ')
    validate_result = change_and_validate_date(date)
    if validate_result['status']:
        now_date = datetime.datetime.now()
        user_age = now_date.year - validate_result['date'].year
        if now_date.month < validate_result['date'].month or \
                now_date.month == validate_result['date'].month and\
                now_date.day < validate_result['date'].day:
            user_age -= 1

        print(user_age)
    else:
        print(validate_result['error'])




# user_choice = 1
# menu()
# while user_choice != 0:
#     user_choice = input('Enter your choice: ')
#     menu(user_choice)

call_function = {1: record_data, 2: find_data, 3: calculate_user_age}

while True:

    print(f'****************************\n'
          f'1.Write information about a person\n'
          f'2.Get information about a person\n'
          f'3.Find out the age of a person\n'
          f'4.Exit\n'
          f'****************************\n')

    choice = input('Make your choice: ')

    if not choice.isdigit() or int(choice) > 4:
        print('Input error, please try again..')
        continue

    choice_int = int(choice)
    if choice_int == 4:
        print('Goodbye...')
        break
    else:
        call_function[choice_int]()
