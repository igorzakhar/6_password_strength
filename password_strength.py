#sources of inspiration  http://www.passwordmeter.com/

import re


def get_password_strength(password):
    lenght = len(password)

    digits = re.findall('\d+', password)
    lower_letter = re.findall('[a-z]', password)
    upper_letter = re.findall('[A-Z]', password)
    symbols = re.findall('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]', password)

    num_of_characters = lenght * 4
    numbers = len(digits)
    num_lower_letters = len(lower_letter)

    print(num_of_characters)
    print(digits)
    print(lower_letter, num_lower_letters)
    
    #return digits, lower_letter, upper_letter, symbols

def get_user_password():
    return input('Enter password: ')


if __name__ == '__main__':
    password = get_user_password()
    print(get_password_strength(password))



"""
    phone_regex = r"(?:\+?(\d{1,4}))?[-. (]*(\d{1,4})[-. )]*(\d{1,3})[-. ]*(\d{4})(?: *x(\d+))?"
    if re.search(phone_regex, password):
        print("ZAPRET")
    else:
        return strength_score
"""