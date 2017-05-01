#Sources of inspiration:  http://www.passwordmeter.com/

import re

from terminaltables import AsciiTable


def get_count_sequential(sequense):
    sequential_score = 0
    for characters in sequense:
        for item in range(len(characters)):
            char_pair = characters[item + 1:item + 3]
            if (len(char_pair) == 2 and 
                    (ord(char_pair[0]) - ord(char_pair[1]) == -1)):
                sequential_score += 1
    return sequential_score


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
    consecutive_upper_score = 0
    consecutive_lower_score = 0
    consecutive_number_score = 0
    sequential_letters_score = 0
    sequential_numbers_score = 0
    #sequential_symbols_score = 0
    
#---------/regexp/-----------------
    digits_list = re.findall(r'\d+', password)
    digits = ''.join(digits_list)
    print(digits_list)
    print(digits)
    upper_letter = re.findall(r'[A-Z]', password)
    lower_letter = re.findall(r'[a-z]', password)
    symbols = ''.join(re.findall(r'[^a-zA-Z0-9_]', password))
    midle_num_symb = ''.join(re.findall(r'[^a-zA-Z_]+', password[1:-1]))
    numbers_only = ''.join(re.findall(r'^\d+$', password))
    letters_only = ''.join(re.findall(r'^[a-zA-Z]+$', password))
    
    consecutive_upper_list = re.findall(r'[A-Z]{2,}', password)
    consecutive_lower_list = re.findall(r'[a-z]{2,}', password)
    consecutive_num_list = re.findall(r'[0-9]{2,}', password)
    
    consecutive_upper = sum([(len(item)-1) for item in consecutive_upper_list])
    consecutive_lower = sum([(len(item)-1) for item in consecutive_lower_list])
    consecutive_num = sum([(len(item)-1) for item in consecutive_num_list])

    sequense_letters = re.findall(r'[A-Za-z]{3,}', password)
    sequense_numbers = re.findall(r'[0-9]{3,}', password)
    #sequense_symbols = re.findall(r'[^a-zA-Z_0-9\s]{3,}', password)
    sequential_letters_score = get_count_sequential(sequense_letters)
    sequential_numbers_score = get_count_sequential(sequense_numbers)
    #sequential_symbols_score = get_count_sequential(sequense_symbols)

    print('sequential_letters_score', sequential_letters_score)
    print('sequential_numbers_score', sequential_numbers_score)
    

    characters_score = lenght * 4       

    if numbers_only:
        numbers_only_score = len(numbers_only)
        requirements += 1
       
    if not numbers_only and digits.isdigit():
        numbers_score = len(digits) * 4
        requirements += 1
    
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

    if letters_only:
        letters_only_score = len(letters_only)

    if consecutive_upper:
        consecutive_upper_score = consecutive_upper * 2
    
    if consecutive_lower:
        consecutive_lower_score = consecutive_lower * 2
    
    if consecutive_num:
        consecutive_number_score = consecutive_num * 2
       

    print('Length: ', lenght, 'symbols')
    
    total = (characters_score + upper_letters_score + lower_letters_score + numbers_score + symbols_score + requirements_score + midle_num_symb_score - letters_only_score - numbers_only_score - consecutive_upper_score - consecutive_lower_score - consecutive_number_score)


    table_data = [['---------- Additions ----------', 'Rate','Count','Score'],
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
                   ['---------- Deductions ----------','', '', ''], 
                   ['Letters Only', '-n', 
                   len(letters_only), '-' + str(letters_only_score)],
                   ['Numbers Only', '-n', 
                   len(numbers_only), '-' + str(numbers_only_score)],
                   ['Consecutive Uppercase Letters', '-(n*2)', 
                   consecutive_upper, '-' + str(consecutive_upper_score)],
                   ['Consecutive Lowercase Letters', '-(n*2)', 
                   consecutive_lower, '-' + str(consecutive_lower_score)],
                   ['Consecutive Numbers', '-(n*2)', 
                   consecutive_num, '-' + str(consecutive_number_score)],
                  ['','', 'Total', total]
                  ]

    table = AsciiTable(table_data)
    table.inner_row_border = True
    table.justify_columns = {0: 'left', 1: 'center', 2: 'center', 3: 'center'}
    print(table.table)
    
    total_total = print(round(total/10))
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