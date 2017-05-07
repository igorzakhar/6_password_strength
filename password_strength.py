import re
import string
import argparse
import getpass

from terminaltables import AsciiTable


def input_user_password():
    password = input('Enter password: ')
    return password


def get_number_characters_score(password):
    number_characters_count = len(password)
    number_characters_score = number_characters_count * 4
    return number_characters_score, number_characters_count


def get_uppercase_score_req(password):
    upper_letters_score = 0
    upper_letter = re.findall(r'[A-Z]', password)
    upper_letters_count = len(upper_letter)
    if upper_letter:
        upper_letters_score = (len(password) - upper_letters_count) * 2
    return upper_letters_score, upper_letters_count


def get_lowercase_score_req(password):
    lower_letters_score = 0
    lower_letter = re.findall(r'[a-z]', password)
    lower_letter_count = len(lower_letter)
    if lower_letter:
        lower_letters_score = (len(password) - lower_letter_count) * 2
    return lower_letters_score, lower_letter_count


def get_numbers_score_req(password):
    numbers_score = 0
    digits_list = re.findall(r'\d+', password)
    digits_count = len(''.join(digits_list))
    if not password.isdigit() and digits_list:
        numbers_score = digits_count * 4
    return numbers_score, digits_count


def get_symbol_score_req(password):
    symbols_score = 0
    symbols = ''.join(re.findall(r'[^a-zA-Z0-9_]', password))
    symbols_count = len(symbols)
    if symbols:
        symbols_score = symbols_count * 6
    return symbols_score, symbols_count


def get_middle_num_symb_score(password):
    middle_num_symb_score = 0
    midle_num_symb = ''.join(re.findall(r'[^a-zA-Z_]+', password[1:-1]))
    midle_num_symb_count = len(midle_num_symb)
    if midle_num_symb:
        middle_num_symb_score = midle_num_symb_count * 2
    return middle_num_symb_score, midle_num_symb_count


def get_letters_only_score(password):
    letters_only_score = 0
    letters_only = ''.join(re.findall(r'^[a-zA-Z]+$', password))
    letters_only_count = len(letters_only)
    if letters_only:
        letters_only_score = -letters_only_count
    return letters_only_score, letters_only_count


def get_numbers_only_score_req(password):
    numbers_only_score = 0
    numbers_only = ''.join(re.findall(r'^\d+$', password))
    numbers_only_count = len(numbers_only)
    if numbers_only:
        numbers_only_score = -numbers_only_count
    return numbers_only_score, numbers_only_count


def get_consecutive_upper_score(password):
    consecutive_upper_score = 0
    consecutive_upper_list = re.findall(r'[A-Z]{2,}', password)
    consecutive_upper_count = sum(
        [(len(item)-1) for item in consecutive_upper_list])
    if consecutive_upper_count:
        consecutive_upper_score = -(consecutive_upper_count * 2)
    return consecutive_upper_score, consecutive_upper_count


def get_consecutive_lower_score(password):
    consecutive_lower_score = 0
    consecutive_lower_list = re.findall(r'[a-z]{2,}', password)
    consecutive_lower_count = sum(
        [(len(item)-1) for item in consecutive_lower_list])
    if consecutive_lower_count:
        consecutive_lower_score = -(consecutive_lower_count * 2)
    return consecutive_lower_score, consecutive_lower_count


def get_consecutive_number_score(password):
    consecutive_number_score = 0
    consecutive_num_list = re.findall(r'[0-9]{2,}', password)
    consecutive_num_count = sum(
        [(len(item)-1) for item in consecutive_num_list])
    if consecutive_num_count:
        consecutive_number_score = -(consecutive_num_count * 2)
    return consecutive_number_score, consecutive_num_count


def get_sequential_letters_score(password):
    sequential_letters_count = 0
    sequential_letters_score = 0
    for item in range(len(string.ascii_lowercase)):
        str_forward = string.ascii_lowercase[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
            sequential_letters_count += 1
    if sequential_letters_count:
        sequential_letters_score = -(sequential_letters_count * 3)
    return sequential_letters_score, sequential_letters_count


def get_sequential_numbers_score(password):
    sequential_numbers_count = 0
    sequential_numbers_score = 0
    for item in range(len(string.digits)):
        str_forward = string.digits[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
            sequential_numbers_count += 1
    if sequential_numbers_count:
        sequential_numbers_score = -(sequential_numbers_count * 3)
    return sequential_numbers_score, sequential_numbers_count


def password_strength_calculate(password):
    global_dict = globals()
    requirements = 0
    requirements_score = 0
    if len(password) > 8:
        requirements += 1
    score_dict = {}
    func_dict = { k : v for k,v in global_dict.items() if k.startswith('get_')}
    for key, value in func_dict.items():
        score_dict[key[4:]] = value(password)
        if key[-3:] == 'req' and value(password)[0]:
            requirements += 1
            if requirements == 5:
                score_dict['requirements'] = (requirements * 2, requirements)
            else:
                score_dict['requirements'] = (0, requirements)
    password_strength = sum(score[0] for score in score_dict.values())
    return password_strength, score_dict


def output_console(verbose, password_strength, score_dict):
    password_strength_score = round(password_strength/10)
    if password_strength_score > 10:
        password_strength_score = 10   
    elif password_strength_score < 1:
        password_strength_score = 1
    print('Total strength score: {}/10'.format(password_strength_score))
    if verbose:
        output_verbose_mode(score_dict)
        

def output_verbose_mode(score_dict):

    table_data = [['---------- Additions ----------', 'Rate','Count','Score'],
                  ['Number of Characters', '+(n*4)', 
                   score_dict['number_characters_score'][1], 
                   '+' + str(score_dict['number_characters_score'][0])],
                  ['Uppercase Letters', '+((len-n)*2)', 
                   score_dict['uppercase_score_req'][1],
                   '+' + str(score_dict['uppercase_score_req'][0])],
                  ['Lowercase Letters', '+((len-n)*2)', 
                   score_dict['lowercase_score_req'][1], 
                   '+' + str(score_dict['lowercase_score_req'][0])],
                  ['Numbers', '+(n*4)', 
                   score_dict['numbers_score_req'][1],
                   '+' + str(score_dict['numbers_score_req'][0])],
                  ['Symbols', '+(n*6)', 
                   score_dict['symbol_score_req'][1],
                   '+' + str(score_dict['symbol_score_req'][0])],
                  ['Middle Numbers or Symbols', '+(n*2)', 
                   score_dict['middle_num_symb_score'][1], 
                   '+' + str(score_dict['middle_num_symb_score'][0])],
                  ['Requirements', '+(n*2)', 
                   score_dict['requirements'][1], 
                   '+' + str(score_dict['requirements'][0])],
                  ['---------- Deductions ----------','', '', ''], 
                  ['Letters Only', '-n', 
                   score_dict['letters_only_score'][1],
                   score_dict['letters_only_score'][0]],
                  ['Numbers Only', '-n', 
                   score_dict['numbers_only_score_req'][1], 
                   score_dict['numbers_only_score_req'][0]],
                  ['Consecutive Uppercase Letters', '-(n*2)', 
                   score_dict['consecutive_upper_score'][1],
                   score_dict['consecutive_upper_score'][0]],
                  ['Consecutive Lowercase Letters', '-(n*2)', 
                   score_dict['consecutive_lower_score'][1],
                   score_dict['consecutive_lower_score'][0]],
                  ['Consecutive Numbers', '-(n*2)', 
                   score_dict['consecutive_number_score'][1],
                   score_dict['consecutive_number_score'][0]],
                  ['Sequential Letters (3+)', '-(n*3)', 
                   score_dict['sequential_letters_score'][1],
                   score_dict['sequential_letters_score'][0]],
                  ['Sequential Numbers (3+)', '-(n*3)', 
                   score_dict['sequential_numbers_score'][1],
                    score_dict['sequential_numbers_score'][0]],
                    ]      
    
    verbose_table = AsciiTable(table_data)
    verbose_table.inner_row_border = True
    verbose_table.justify_columns = {0: 'left', 1: 'center', 
                                 2: 'center', 3: 'center'}
    
    print(verbose_table.table)


def process_args():
    parser = argparse.ArgumentParser(description='Most starred repos find')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output issues urls')
    return  parser.parse_args()


if __name__ == '__main__':
  
    args = process_args()
    password = input_user_password()
    if not password:
         print('Password field cannot be empty')
    else:
        password_strength, score_dict = password_strength_calculate(password)
        output_console(args.verbose, password_strength, score_dict)
