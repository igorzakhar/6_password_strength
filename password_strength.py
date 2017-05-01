#Sources of inspiration:  http://www.passwordmeter.com/

import re
import argparse

from terminaltables import AsciiTable


def check_sequential_alphas(password):
    string_alphas = "abcdefghijklmnopqrstuvwxyz"
    sequential_score = 0
    for item in range(len(string_alphas)):
        str_forward = string_alphas[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
            sequential_score += 1
    return sequential_score

def check_sequential_numerics(password):
    string_numerics = "01234567890"
    sequential_score = 0
    for item in range(len(string_numerics)):
        str_forward = string_numerics[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
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
    total_score = []

    digits_list = re.findall(r'\d+', password)
    digits = ''.join(digits_list)
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
    
    characters_score = lenght * 4  
    total_score.append(characters_score)

#--------------/Additions/--------------- 
    
    if not numbers_only and digits.isdigit():
        numbers_score = len(digits) * 4
        total_score.append(numbers_score)
        requirements += 1
    
    if lower_letter:
        lower_letters_score = (lenght - len(lower_letter)) * 2
        total_score.append(lower_letters_score)
        requirements += 1
        
    if upper_letter:
        upper_letters_score = (lenght - len(upper_letter)) * 2
        total_score.append(upper_letters_score)
        requirements += 1
        
    if symbols:
        symbols_score = len(symbols) * 6
        total_score.append(symbols_score)
        requirements += 1
        
    if lenght >= 8:
        requirements += 1
        
    if requirements == 5:
        requirements_score = requirements * 2
        total_score.append(requirements_score)

    if midle_num_symb:
        midle_num_symb_score = len(midle_num_symb) * 2
        total_score.append(midle_num_symb_score)

#--------------/Deductions/---------------

    if numbers_only:
        numbers_only_score = len(numbers_only)
        total_score.append(-numbers_only_score)
        requirements += 1

    if letters_only:
        letters_only_score = len(letters_only)
        total_score.append(-letters_only_score)

    if consecutive_upper:
        consecutive_upper_score = consecutive_upper * 2
        total_score.append(-consecutive_upper_score)
    
    if consecutive_lower:
        consecutive_lower_score = consecutive_lower * 2
        total_score.append(-consecutive_lower_score)
    
    if consecutive_num:
        consecutive_number_score = consecutive_num * 2
        total_score.append(-consecutive_number_score)
    
    sequential_letters_count = check_sequential_alphas(password)
    if sequential_letters_count:
        sequential_letters_score = sequential_letters_count * 3
        total_score.append(-sequential_letters_score)
    
    sequential_numbers_count = check_sequential_numerics(password)
    if sequential_numbers_count:
        sequential_numbers_score = sequential_numbers_count * 3
        total_score.append(-sequential_numbers_score)


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
                   ['Sequential Letters (3+)', '-(n*3)', 
                   sequential_letters_count, '-' + str(
                       sequential_letters_score)],
                   ['Sequential Numbers (3+)', '-(n*3)', 
                   sequential_numbers_count, '-' + str(
                       sequential_numbers_score)],
                  ['','', 'Total', '']
                  ]

    return sum(total_score), table_data


def get_user_password():
    password = input('Enter password: ')
    if not password:
        print('Password field cannot be empty')
    else:
        return password


def console_output(verbose, total_score, table_data):
    if round(total_score/10) > 10:
            strength_score = 10    
    else:
        strength_score = round(total_score/10)
    print('Total strength score: {}/10'.format(strength_score))
    if verbose:
        table = AsciiTable(table_data)
        table.inner_row_border = True
        table.justify_columns = {0: 'left', 1: 'center', 
                                 2: 'center', 3: 'center'}
        print(table.table)


def process_args():
    parser = argparse.ArgumentParser(description='Most starred repos find')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output issues urls')
    return  parser.parse_args()


if __name__ == '__main__':
    args = process_args()
    password = get_user_password()
    total_score, table_data = get_password_strength(password)
    console_output(args.verbose, total_score, table_data)

