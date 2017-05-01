#Sources of inspiration:  http://www.passwordmeter.com/

import re

from terminaltables import AsciiTable


def get_password_strength(password):
    if not password:
        return

    lenght = len(password)
    numbers_score = 0
    lower_letters_score = 0
    upper_letters_score = 0
    symbols_score = 0
    requirements = 0
    requirements_score = 0
    midle_num_symb_score = 0
    letters_only_score = 0
    numbers_only_score = 0

#---------/regexp/-----------------
    #requirements_pattern = r'^.*(?=.{1,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~!@#$%^&+=]).*$'
    #requirements = re.search(requirements_pattern, password)
    digits = ''.join(re.findall(r'\d+', password))
    upper_letter = re.findall(r'[A-Z]', password)
    print('Uppercase: ', upper_letter)
    lower_letter = re.findall(r'[a-z]', password)
    print('Lowercase: ', lower_letter)
    #symbols = ''.join(re.findall(r'[~!@#$%^&*+=]+', password))
    symbols = ''.join(re.findall(r'[^a-zA-Z0-9_]', password))
    midle_num_symb = ''.join(re.findall(r'[^a-zA-Z_]+', password[1:-1]))
    print('Middle: ', midle_num_symb)
    print('Symbols: ', symbols)
    numbers_only = ''.join(re.findall(r'^\d+$', password))
    letters_only = ''.join(re.findall(r'^[a-zA-Z]+$', password))
    

#---------/Additions/-----------------
    
    characters_score = lenght * 4       
    if numbers_only:
        numbers_only_score = len(numbers_only)
        requirements += 1
    else:
        numbers_score = len(digits) * 4
        requirements += 1
    #if not numbers_only:
    #    numbers_score = len(digits) * 4
    #    requirements += 1
    
    if lower_letter:
        lower_letters_score = (lenght - len(lower_letter)) * 2
        requirements += 1
    if upper_letter:
        upper_letters_score = (lenght - len(upper_letter)) * 2
        requirements += 1
    if symbols:
        symbols_score = len(symbols) * 6
        requirements += 1
    if lenght >= 8:
        requirements += 1
    if requirements == 5:
        requirements_score = requirements * 2
    if midle_num_symb:
        midle_num_symb_score = len(midle_num_symb) * 2

#---------/Deductions/-----------------

    if letters_only:
        letters_only_score = len(letters_only)
        requirements += 1

    #if numbers_only:
    #    numbers_only_score = len(numbers_only)
    #    requirements += 1
    
    print('Length: ', lenght, 'symbols')
    
    total = (characters_score + upper_letters_score + lower_letters_score + numbers_score + symbols_score + requirements_score + midle_num_symb_score - letters_only_score - numbers_only_score)


    table_data = [['Metric\'s', 'Rate','Count','Score'],
                  ['Number of Characters', '+(n*4)', 
                   lenght, '+' + str(characters_score)],
                  ['Uppercase Letters', '+((len-n)*2)', 
                   len(upper_letter), '+' + str(upper_letters_score)],
                  ['Lowercase Letters', '+((len-n)*2)', 
                   len(lower_letter), '+' + str(lower_letters_score)],
                  ['Numbers', '+(n*4)', 
                   len(digits), '+' + str(numbers_score)],
                  ['Symbols', '+(n*6)', 
                   len(symbols), '+' + str(symbols_score)],
                   ['Middle Numbers or Symbols', '+(n*2)', 
                   len(midle_num_symb), '+' + str(midle_num_symb_score)],
                   ['Requirements', '+(n*2)', 
                   requirements, '+' + str(requirements_score)], 
                   ['Letters Only', '-n', 
                   len(letters_only), '-' + str(letters_only_score)],
                   ['Numbers Only', '-n', 
                   len(numbers_only), '-' + str(numbers_only_score)],
                  ['','', 'Total', total]
                  ]

    table = AsciiTable(table_data)
    table.inner_row_border = True
    table.justify_columns = {0: 'left', 1: 'center', 2: 'center', 3: 'center'}
    print(table.table)
    
    #return digits, lower_letter, upper_letter, symbols

def get_user_password():
    password = input('Enter password: ')
    if not password:
        print('Password field cannot be empty')
    else:
        return password


if __name__ == '__main__':
    password = get_user_password()
    get_password_strength(password)


"""
    phone_regex = r"(?:\+?(\d{1,4}))?[-. (]*(\d{1,4})[-. )]*(\d{1,3})[-. ]*(\d{4})(?: *x(\d+))?"
    if re.search(phone_regex, password):
        print("ZAPRET")
    else:
        return strength_score
"""

"""
print(
        'Number of Char.(+(n*4)). n = {}. Score = {}'.format(
            lenght, characters_score))
    print(
        'Lower Letters. +((len-n)*2). n = {}. Score = {}'.format(
            len(lower_letter), lower_letters_score))
    print(
        'Upper Letters. +((len-n)*2). n = {}. Score = {}'.format(
            len(upper_letter), upper_letters_score))
    print(
        'Numbers +(n*4). n = {}. Score = {}'.format(
            len(digits), numbers_score))
"""