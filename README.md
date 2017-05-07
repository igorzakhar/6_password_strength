# Password Strength Calculator

Программа предназначена для оценки сложности пароля. Метрики и формулы для вычисления веса каждой метрики взяты из приложения [http://www.passwordmeter.com/](http://www.passwordmeter.com/). Для оценки пароля используется бальная система от 1 до 10. 1- очень слабый пароль, 10 - очень сильный.

# Установка

Программа требует для своей работы установленного интерпретатора Python версии 3.5.  
В программе используется сторонняя библиотека [terminaltables](https://pypi.python.org/pypi/terminaltables).
Используйте команду pip для установки  библиотеки из файла зависимостей (или pip3 если есть конфликт с предустановленным Python 2):
```bash
pip install -r requirements.txt # В качестве альтернативы используйте pip3
```
Рекомендуется устанавливать зависимости в виртуальном окружении, используя [virtualenv](https://github.com/pypa/virtualenv), [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) или [venv](https://docs.python.org/3/library/venv.html).  

Библиотека terminaltables используется для  вывода всех показателей из которых складывается общая оценка сложности пароля (см. "Использование").  

# Описание

Минимальные требования для пароля:
 - Одна заглавная буква;
 - Одна строчная буква;
 - Одна цифра;
 - Один символ (~!@#$%^&*+=...);
 - Длина пароля > 8 символов.

Все метрики, из которых складывается общая оценка, делятся на две части:

## Additions (добавляют баллы к общей оценке сложности)
- Number of Characters - Количество символов; 
- Uppercase Letters - Заглавные буквы;
- Lowercase Letters - Строчные буквы;
- Numbers - Числа;
- Symbols - Символы;
- Middle Numbers or Symbols - Числа и символы в середине пароля;
- Requirements - Минимальные требования.

## Deductions (вычитают баллы из общей оценки сложности)
- Numbers Only - Пароль состоит только из цифр;
- Consecutive Uppercase Letters  - В пароле встречаются последовательности букв верхнего регистра;
- Consecutive Lowercase Letters - В пароле встречаются последовательности букв нижнего регистра;
- Consecutive Numbers - В пароле встречаются последовательности цифр;
- Sequential Letters (3+) - Последовательность букв следующих в алфавитном(обратном) порядке;
- Sequential Numbers (3+) - Последовательность цифр в порядке возрастания(убывания).

# Использование

### Параметры командной строки:

**-v --verbose** - вывод всех показателей из которых складывается общая оценка сложности пароля.  

Пример запуска в Linux, Python 3.5.2:

```#!bash
$ python password_strength.py
Enter password: 123esgd
Total strength score: 4/10
```

Пример запуска с параметром -v(--verbose)
```#!bash
$ python password_strength.py -v
Enter password: 
Total strength score: 9/10
+----------------------------------+--------------+-------+-------+
| ---------- Additions ----------  |     Rate     | Count | Score |
+----------------------------------+--------------+-------+-------+
| Number of Characters             |    +(n*4)    |   8   |  +32  |
+----------------------------------+--------------+-------+-------+
| Uppercase Letters                | +((len-n)*2) |   2   |  +12  |
+----------------------------------+--------------+-------+-------+
| Lowercase Letters                | +((len-n)*2) |   2   |  +12  |
+----------------------------------+--------------+-------+-------+
| Numbers                          |    +(n*4)    |   2   |   +8  |
+----------------------------------+--------------+-------+-------+
| Symbols                          |    +(n*6)    |   2   |  +12  |
+----------------------------------+--------------+-------+-------+
| Middle Numbers or Symbols        |    +(n*2)    |   3   |   +6  |
+----------------------------------+--------------+-------+-------+
| Requirements                     |    +(n*2)    |   5   |  +10  |
+----------------------------------+--------------+-------+-------+
| ---------- Deductions ---------- |              |       |       |
+----------------------------------+--------------+-------+-------+
| Letters Only                     |      -n      |   0   |   -0  |
+----------------------------------+--------------+-------+-------+
| Numbers Only                     |      -n      |   0   |   -0  |
+----------------------------------+--------------+-------+-------+
| Consecutive Uppercase Letters    |    -(n*2)    |   1   |   -2  |
+----------------------------------+--------------+-------+-------+
| Consecutive Lowercase Letters    |    -(n*2)    |   1   |   -2  |
+----------------------------------+--------------+-------+-------+
| Consecutive Numbers              |    -(n*2)    |   1   |   -2  |
+----------------------------------+--------------+-------+-------+
| Sequential Letters (3+)          |    -(n*3)    |   0   |   -0  |
+----------------------------------+--------------+-------+-------+
| Sequential Numbers (3+)          |    -(n*3)    |   0   |   -0  |
+----------------------------------+--------------+-------+-------+
```

# Цели проекта

Код написан для образовательных целей. Учебный курс для веб-разработчиков - [DEVMAN.org](https://devman.org)
