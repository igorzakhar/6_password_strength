import re
import string
import argparse
import getpass

from terminaltables import AsciiTable


def get_user_password(hide):
    if hide:
        password = getpass.getpass(prompt='Enter password: ')
    else:
        password = input('Enter password: ')
    return password


def check_sequential_alphas(password):
    sequential_score = 0
    for item in range(len(string.ascii_lowercase)):
        str_forward = string.ascii_lowercase[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
            sequential_score += 1
    return sequential_score


def check_sequential_numerics(password):
    sequential_score = 0
    for item in range(len(string.digits)):
        str_forward = string.digits[item:item + 3]
        str_reverse = str_forward[::-1]
        if (password.lower().find(str_forward) != -1 or
            password.lower().find(str_reverse) != -1):
            sequential_score += 1
    return sequential_score


def get_additions_type(password):
    length = len(password)
    digits_list = re.findall(r'\d+', password)
    upper_letter = re.findall(r'[A-Z]', password)
    lower_letter = re.findall(r'[a-z]', password)
    symbols = ''.join(re.findall(r'[^a-zA-Z0-9_]', password))
    midle_num_symb = ''.join(re.findall(r'[^a-zA-Z_]+', password[1:-1]))
    numbers_only = ''.join(re.findall(r'^\d+$', password))

    return (length, digits_list, upper_letter, lower_letter,
            symbols, midle_num_symb, numbers_only)


def get_deductions_type(password):
    numbers_only = ''.join(re.findall(r'^\d+$', password))
    letters_only = ''.join(re.findall(r'^[a-zA-Z]+$', password))

    consecutive_upper_list = re.findall(r'[A-Z]{2,}', password)
    consecutive_lower_list = re.findall(r'[a-z]{2,}', password)
    consecutive_num_list = re.findall(r'[0-9]{2,}', password)
    consecutive_upper_count = sum(
        [(len(item)-1) for item in consecutive_upper_list])
    consecutive_lower_count = sum(
        [(len(item)-1) for item in consecutive_lower_list])
    consecutive_num_count = sum(
        [(len(item)-1) for item in consecutive_num_list])

    sequense_letters = re.findall(r'[A-Za-z]{3,}', password)
    sequense_numbers = re.findall(r'[0-9]{3,}', password)

    return (numbers_only, letters_only, 
            consecutive_upper_count, consecutive_lower_count, consecutive_num_count, sequense_letters, sequense_numbers)


def get_additions_score(additions_type):
    (lenght, digits_list, 
     upper_letter, lower_letter,
     symbols, midle_num_symb, numbers_only) = additions_type
    
    numbers_score = 0
    lower_letters_score = 0
    upper_letters_score = 0
    symbols_score = 0
    midle_num_symb_score = 0
    requirements = 0
    requirements_score = 0

    number_characters_score = lenght * 4
        
    if not numbers_only and digits_list:
        numbers_score = len(''.join(digits_list)) * 4
        requirements += 1
    elif numbers_only:
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
    
    return (number_characters_score ,numbers_score, lower_letters_score, 
            upper_letters_score, symbols_score, midle_num_symb_score, requirements, requirements_score)


def get_deductions_score(deductions_type, seq_letters, seq_numbers):
    (numbers_only, letters_only, 
     consecutive_upper_count, 
     consecutive_lower_count, 
     consecutive_num_count, 
     sequense_letters, sequense_numbers)  = deductions_type
    
    letters_only_score = 0
    numbers_only_score = 0
    consecutive_upper_score = 0
    consecutive_lower_score = 0
    consecutive_number_score = 0
    sequential_letters_score = 0
    sequential_numbers_score = 0

    if letters_only:
        letters_only_score = -(len(letters_only))
        
    if numbers_only:
        numbers_only_score = -(len(numbers_only))

    if consecutive_upper_count:
        consecutive_upper_score = -(consecutive_upper_count * 2)
            
    if consecutive_lower_count:
        consecutive_lower_score = -(consecutive_lower_count * 2)
        
    if consecutive_num_count:
        consecutive_number_score = -(consecutive_num_count * 2)
       
    if seq_letters:
        sequential_letters_score = -(seq_letters * 3)
    
    if seq_numbers:
        sequential_numbers_score = -(seq_numbers * 3)
    
    return (letters_only_score, numbers_only_score, consecutive_upper_score,
            consecutive_lower_score, consecutive_number_score,
            sequential_letters_score, sequential_numbers_score,
            seq_letters, seq_numbers)


def get_password_strength(additions_score, deductions_score):
    total_score = []
    total_score.extend(additions_score + deductions_score)
    password_strength = round(sum(total_score)/10)
    if password_strength > 10:
        password_strength = 10   
    elif password_strength < 1:
        password_strength = 1
    return password_strength


def output_verbose_mode(add_type, deduct_type, add_score, deduct_score):
    (lenght, digits_list, 
     upper_letter, lower_letter,
     symbols, midle_num_symb, numbers_only) = add_type
    
    (numbers_only, letters_only, 
     consecutive_upper_count, 
     consecutive_lower_count, 
     consecutive_num_count, 
     sequense_letters, sequense_numbers)  = deduct_type

    (number_characters_score ,numbers_score, 
     lower_letters_score, upper_letters_score, 
     symbols_score, midle_num_symb_score, 
     requirements, requirements_score) = add_score

    (letters_only_score, numbers_only_score, 
     consecutive_upper_score, consecutive_lower_score,
     consecutive_number_score, sequential_letters_score, sequential_numbers_score, seq_letters, seq_numbers) = deduct_score

    table_data = [['---------- Additions ----------', 'Rate','Count','Score'],
                  ['Number of Characters', '+(n*4)', 
                   lenght, '+' + str(number_characters_score)],
                  ['Uppercase Letters', '+((len-n)*2)', 
                   len(upper_letter), '+' + str(upper_letters_score)],
                  ['Lowercase Letters', '+((len-n)*2)', 
                   len(lower_letter), '+' + str(lower_letters_score)],
                  ['Numbers', '+(n*4)', 
                   len(''.join(digits_list)), '+' + str(numbers_score)],
                  ['Symbols', '+(n*6)', 
                   len(symbols), '+' + str(symbols_score)],
                   ['Middle Numbers or Symbols', '+(n*2)', 
                   len(midle_num_symb), '+' + str(midle_num_symb_score)],
                   ['Requirements', '+(n*2)', 
                   requirements, '+' + str(requirements_score)],
                   ['---------- Deductions ----------','', '', ''], 
                   ['Letters Only', '-n', 
                   len(letters_only), str(letters_only_score)],
                   ['Numbers Only', '-n', 
                   len(numbers_only), str(numbers_only_score)],
                   ['Consecutive Uppercase Letters', '-(n*2)', 
                   consecutive_upper_count, str(consecutive_upper_score)],
                   ['Consecutive Lowercase Letters', '-(n*2)', 
                   consecutive_lower_count, str(consecutive_lower_score)],
                   ['Consecutive Numbers', '-(n*2)', 
                   consecutive_num_count, str(consecutive_number_score)],
                   ['Sequential Letters (3+)', '-(n*3)', 
                    seq_letters, str(sequential_letters_score)],
                   ['Sequential Numbers (3+)', '-(n*3)', 
                    seq_numbers, str(sequential_numbers_score)],
                    ]      
    
    verbose_table = AsciiTable(table_data)
    verbose_table.inner_row_border = True
    verbose_table.justify_columns = {0: 'left', 1: 'center', 
                                 2: 'center', 3: 'center'}
    
    return verbose_table.table


def output_console(verbose, password):
    seq_letters = check_sequential_alphas(password)
    seq_numbers = check_sequential_numerics(password)
    add_type = get_additions_type(password)
    ded_type = get_deductions_type(password)
    add_score = get_additions_score(add_type)
    ded_score = get_deductions_score(ded_type, seq_letters, seq_numbers)
    password_strength = get_password_strength(add_score, ded_score)

    print('Total strength score: {}/10'.format(password_strength))
    if args.verbose:
        print(output_verbose_mode(add_type, ded_type, add_score, ded_score))


def process_args():
    parser = argparse.ArgumentParser(description='Most starred repos find')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='output issues urls')
    parser.add_argument('-hp', '--hide', action='store_true',
                        help='Hide input password')
    return  parser.parse_args()


if __name__ == '__main__':
    args = process_args()
    password = get_user_password(args.hide)
    output_console(args.verbose, password)



