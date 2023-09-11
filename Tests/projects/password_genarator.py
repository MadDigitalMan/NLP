import random

DIGITS = '0123456789'
LOWER_CASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
UPPER_CASE_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
PUNCTUATION = '!#$%&*+-=?@^_'
chars = ''
list_password = []
print('Введите количесвто паролей для генерации: ', end='')
input_count = int(input())
print('Введите длину одного пароля: ', end='')
input_length = int(input())
print('Включать ли в пароль цифры 0123456789? ', end='')
choose = input()
if choose == 'да':
    digit_count = random.randint(1, input_length)
    chars += random.choice(DIGITS)

for _ in range(input_count):
    password_length = min(input_length, len(chars))  # Минимум между введенной длиной и длиной строки chars
    password = random.sample(chars, password_length)  # Выбор случайных уникальных символов для пароля
    password_str = ''.join(password)  # Преобразование пароля в строку
    list_password.append(password_str)  # Добавление пароля в список

print('Сгенерированные пароли:', list_password)
