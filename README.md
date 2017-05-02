# Password Strength Calculator

Программа предназначена для оценки сложности пароля. Метрики и формулы для вычисления веса каждой метрики взяты из приложения [http://www.passwordmeter.com/](http://www.passwordmeter.com/). Для оценки пароля используется бальная система от 1 до 10. 1- очень слабый пароль, 10 - очень сильный.

# Описание
Минимальные требования для пароля:
 - Одна заглавная буква;
 - Одна строчная буква;
 - Одна цифра;
 - Один символ (~!@#$%^&*+=...);

Все метрики делятся на две части:

## Additions (добавляют баллы к общей оценке сложности)
- Number of Characters - Количество символов; 
- Uppercase Letters - Заглавные буквы;
- Lowercase Letters - Строчные буквы;
- Numbers - Числа;
- Symbols - Символы;
- Middle Numbers or Symbols - Числа и символы в середине пароля;
- Requirements - Минимальные требования.

## Deductions (вычитают баллы из общей оценке сложности)
- Numbers Only - Пароль состоит только из цифр;
- Consecutive Uppercase Letters  - В пароле встречаются последовательности букв верхнего регистра;
- Consecutive Lowercase Letters - В пароле встречаются последовательности букв нижнего регистра;
- Consecutive Numbers - В пароле встречаются последовательности цифр;
- Sequential Letters (3+) - Последовательность букв следующих в алфавитном(обратном) порядке;
- Sequential Numbers (3+) - Последовательность цифр в порядке возрастания(убывания).

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
