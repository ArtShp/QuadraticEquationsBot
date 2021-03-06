import telebot
from fractions import Fraction
from math import sqrt
import os
from flask import Flask, request
import logging
TOKEN = '1040628806:AAHLkb6i6BhQCVQq81bIJabXMRelXJ3vEKk'

startMessage = '''
Это бот квадратных уравнений, трёхчленов и функций(парабол).
Для получения ответа введите 3 числа через пробелы.
Для полной информации напишите /help.
Советую сразу написать /help.
'''

helpMessage = f'''*
•Для стартового сообщения введите /start
•Для помощи введите /help*
Это бот по решению квадратных уравнений.
Работают полные и неполные уравнения.
Для ответа, введите через пробелы 3 числа.
Например:(22 4.8 -33).
Если оно неполное, то пишите ноль, на месте того члена.
Например:(0 2 -6).
Работает с целыми числами + десятичные и обыкновенные дроби.
Пример написания обычной дроби:(2/5).

*!ВАЖНО*
Есть небольшой баг:
Если у одно из корня знаменатель кратен 3
Например:(3, 6, 9, 12, и т.д.), то будут выводить не как 1/3, а как 0.33333333 и т.д.

*И ещё пару фич:
•Не работает с корнями!
•Знак "<=>" означает равенство дву частей, одна из которых записана десятичными дробями,
а другая обыкновенными.*
Например:(x1 = 0.666666 <=> x1=2/3), отчевидно, что лучше писать обыкновенные дроби в ответе,
но бывают баги и получается кривое число, и иногда приходится использовать десятичную дробь.
*•Слово "или" показывает на два корня в уравнениях, где x² равно какому-то числу и имеет два корня.*
Например:(x² = 9; x = 3 или x = -3).
'''

errorMessage = '''
Ошибка!
Вы неверно ввели данные, повторите попытку!
'''

strIF1 = '•Если это уравнение:'
strIF2 = '•Если это квадратный трёхчлен:'
strIF3 = '•Если это квадратичная функция:'
strIF4 = '•Если это квадратное неравенство:'

bot = telebot.TeleBot(TOKEN)

def quadratic_trinomial(a, d, x1, x2, strUravnenie):
    str_quad_trinomial_1 = ''
    str_quad_trinomial_2 = ''
    x1 = float(x1)
    x2 = float(x2)
    if d > 0:
        if x1 < 0:
            if a != 1:
                str_quad_trinomial_1 = f'{a}'
                str_quad_trinomial_2 = f'{a}'
            str_quad_trinomial_1 += f'(x + {-x1})'
            str_quad_trinomial_2 += f'(x + {-Fraction(x1)})'
        elif x1 > 0:
            if a != 1:
                str_quad_trinomial_1 = f'{a}'
                str_quad_trinomial_2 = f'{a}'
            str_quad_trinomial_1 += f'(x - {x1})'
            str_quad_trinomial_2 += f'(x - {Fraction(x1)})'
        else:
            if a != 1:
                str_quad_trinomial_1 = f'{a}'
                str_quad_trinomial_2 = f'{a}'
            str_quad_trinomial_1 += f'x'
            str_quad_trinomial_2 += f'x'

        if x2 < 0:
            str_quad_trinomial_1 += f'(x + {-x2})'
            str_quad_trinomial_2 += f'(x + {-Fraction(x2)})'
        elif x2 > 0:
            str_quad_trinomial_1 += f'(x - {x2})'
            str_quad_trinomial_2 += f'(x - {Fraction(x2)})'
        else:
            if x1 == 0:
                if a != 1:
                    str_quad_trinomial_1 = f'{a}x²'
                    str_quad_trinomial_2 = f'{a}x²'
                else:
                    str_quad_trinomial_1 = f'x²'
                    str_quad_trinomial_2 = f'x²'
            elif x1 > 0:
                if a != 1:
                    str_quad_trinomial_1 = f'{a}x(x - {x1})'
                    str_quad_trinomial_2 = f'{a}x(x - {Fraction(x1)})'
                else:
                    str_quad_trinomial_1 = f'x(x - {x1})'
                    str_quad_trinomial_2 = f'x(x - {Fraction(x1)})'
            elif x1 < 0:
                if a != 1:
                    str_quad_trinomial_1 = f'{a}x(x + {-x1})'
                    str_quad_trinomial_2 = f'{a}x(x + {-Fraction(x1)})'
                else:
                    str_quad_trinomial_1 = f'x(x + {-x1})'
                    str_quad_trinomial_2 = f'x(x + {-Fraction(x1)})'
    elif d == 0:
        if x1 < 0:
            if a != 1:
                str_quad_trinomial_1 = f'{a}(x + {-x1})²'
                str_quad_trinomial_2 = f'{a}(x + {-Fraction(x1)})²'
            else:
                str_quad_trinomial_1 = f'(x + {-x1})²'
                str_quad_trinomial_2 = f'(x + {-Fraction(x1)})²'
        elif x1 > 0:
            if a != 1:
                str_quad_trinomial_1 = f'{a}(x - {x1})²'
                str_quad_trinomial_2 = f'{a}(x - {Fraction(x1)})²'
            else:
                str_quad_trinomial_1 = f'(x - {x1})²'
                str_quad_trinomial_2 = f'(x - {Fraction(x1)})²'
        else:
            if a != 1:
                str_quad_trinomial_1 = f'{a}x²'
                str_quad_trinomial_2 = f'{a}x²'
            else:
                str_quad_trinomial_1 = f'x²'
                str_quad_trinomial_2 = f'x²'

    str_quad_trinomial_1 = strUravnenie[0:len(strUravnenie)-1] + str_quad_trinomial_1
    str_quad_trinomial_1 += f'\n--------------------<=>--------------------\n'
    str_quad_trinomial_1 += strUravnenie[0:len(strUravnenie)-1] + str_quad_trinomial_2
    return str_quad_trinomial_1

def quadratic_function(x1, x2, a, b, c, d):
    branch_direction = ''
    if a > 0:
        branch_direction = f'a = {a} > 0, ветви вверх'
    elif a < 0:
        branch_direction = f'a = {a} < 0, ветви вниз'
    else:
        pass

    x_top = -b / (2 * a)
    y_top = a*x_top*x_top + b*x_top+c
    top_cords = f'x = {x_top} y = {y_top}; ({x_top}; {y_top})-вершина параболы'
    if d > 0:
        crossing_Ox = f'x1 = {x1}, x2 = {x2}; ({x1}; 0) и ({x2}; 0) - нули функции'
    elif d == 0:
        crossing_Ox = f'x = {x_top}, ({x_top}; 0) - точка касания'
    else:
        crossing_Ox = f'Нет точек пересечения с Ox'

    crossing_Oy = f'Пересечение с Oy: (0, {c})'

    E = ''
    max_min_y = ''
    if a > 0:
        E = f'E = [{y_top}; +∞)'
        max_min_y = f'Наименьшее y = {y_top}'
    elif a < 0:
        E = f'E = (-∞; {y_top}]'
        max_min_y = f'Наибольшее y = {y_top}'

    strMonot = ''
    if a > 0:
        strMonot = f'(-∞; {x_top}]-промежуток убывания\n  '
        strMonot += f'[{x_top}; +∞)-промежуток возрастания'
    elif a < 0:
        strMonot = f'(-∞; {x_top}]-промежуток возрастания\n  '
        strMonot += f'[{x_top}; +∞)-промежуток убывания'
    else:
        pass

    strPromZnakPost = ''
    if a > 0:
        if d > 0:
            strPromZnakPost = f'y > 0 при x ϵ (-∞; {min(x1, x2)}) υ ({max(x1, x2)}; +∞)\n'
            strPromZnakPost += f'  y < 0 при x ϵ ({min(x1, x2)}; {max(x1, x2)})'
        elif d == 0:
            strPromZnakPost = f'y > 0 при x ϵ (-∞; {x_top}) υ ({x_top}; +∞)'
        else:
            strPromZnakPost = f'y > 0 при x ϵ R <=> (-∞; +∞)'
    elif a < 0:
        if d > 0:
            strPromZnakPost = f'y > 0 при x ϵ ({min(x1, x2)}; {max(x1, x2)})\n'
            strPromZnakPost += f'  y < 0 при x ϵ (-∞; {min(x1, x2)}) υ ({max(x1, x2)}; +∞)'
        elif d == 0:
            strPromZnakPost = f'y < 0 при x ϵ (-∞; {x_top}) υ ({x_top}; +∞)'
        else:
            strPromZnakPost = f'y < 0 при x ϵ R <=> (-∞; +∞)'
    else:
        pass

    strAll = f'1){branch_direction}' + '\n'
    strAll += f'2){top_cords}' + '\n'
    strAll += f'3){crossing_Ox}' + '\n'
    strAll += f'4){crossing_Oy}' + '\n'
    strAll += f'5){E}' + '\n'
    strAll += f'6){max_min_y}\n'
    strAll += f'7){strMonot}\n'
    strAll += f'8){strPromZnakPost}'

    return strAll

def quadratic_inequality():
    pass

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}.' + startMessage)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, helpMessage, parse_mode= "Markdown")

@bot.message_handler(content_types=['text'])
def enter_a_b_c(message):
    try:
        global a, b, c
        x1 = 0
        x2 = 0
        a = ''
        b = ''
        c = ''
        strDiss = ''
        strX1 = ''
        strX2 = ''
        str_quad_trinomial = ''
        i = 0
        while message.text[i] != ' ':
            a = str(a)
            a += message.text[i]
            i += 1
        while message.text[i + 1] != ' ':
            b = str(b)
            b += message.text[i + 1]
            i += 1
        for i in range(i + 2, len(message.text)):
            c = str(c)
            c += message.text[i]

        a = Fraction(a)
        b = Fraction(b)
        c = Fraction(c)

        if a != 0:
            strUravnenie = f'{a}x² '
            if b > 0:
                strUravnenie += f'+ {b}x '
            elif b < 0:
                strUravnenie += f'- {-b}x '
            else:
                strUravnenie += ' '
            if c > 0:
                strUravnenie += f'+ {c} '
            elif c < 0:
                strUravnenie += f'- {-c} '
            strUravnenie += '= 0'

            if b == 0:
                if a*c < 0:
                    strUravnenie += f' <=> {a}x² = {-c}'
                    strX1 = f'x² = {float(-c/a)} <=> x² = {Fraction(-c/a)}'
                    strX2 = f'x = {float(sqrt(-c/a))} <=> x = {Fraction(sqrt(-c/a))}'
                    strX2 += f'\n----------ИЛИ----------\n'
                    strX2 += f'x = -{float(sqrt(-c/a))} <=> x = -{Fraction(sqrt(-c/a))}'
                    x1 = Fraction(sqrt(-c/a))
                    x2 = -Fraction(sqrt(-c/a))
                elif a*c > 0:
                    strX1 = 'Нет корней'
                else:
                    strX1 = 'x = 0'
                    x1 = 0
                    x2 = 0
            else:
                d = Fraction(b * b - 4 * a * c)
                strDiss = f'd = {float(d)} <=> d = {d}'

                if d > 0:
                    strDiss += f'\n√d = {float(sqrt(d))} <=> √d = {Fraction(sqrt(d))}'
                    x1 = (-b - sqrt(d)) / (2 * a)
                    x2 = (-b + sqrt(d)) / (2 * a)

                    strX1 = f'x1 = {float(x1)} <=> x1 = {Fraction((-b - sqrt(d)) / (2 * a))}'
                    strX2 = f'x2 = {float(x2)} <=> x2 = {Fraction((-b + sqrt(d)) / (2 * a))}'
                    str_quad_trinomial = quadratic_trinomial(a, d, x1, x2, strUravnenie)
                elif d == 0:
                    x1 = -b / (2 * a)
                    x2 = x1
                    strX1 = f'x = {float(x1)} <=> x = {Fraction(-b / (2 * a))}'
                    str_quad_trinomial = quadratic_trinomial(a, d, x1, 0, strUravnenie)
                elif d < 0:
                    strX1 = 'Нет корней'
        else:
            if c == 0:
                if b == 0:
                    strUravnenie = '0x = 0'
                    strX1 = 'x - любое число'
                else:
                    strUravnenie = f'{b}x = 0'
                    strX1 = 'x = 0'
            elif b == 0:
                strUravnenie = '0x '
                if c > 0:
                    strUravnenie += f'+ {c} '
                elif c < 0:
                    strUravnenie += f'- {-c} '
                strUravnenie += f'= 0 <=> 0x = {-c}'
                strX1 = 'Нет корней'
            else:
                strUravnenie = f'{b}x '
                if c > 0:
                    strUravnenie += f'+ {c} '
                elif c < 0:
                    strUravnenie += f'- {-c} '
                strUravnenie += f'= 0 <=> {b}x = {-c}'
                strX1 = f'x = {float(-c/b)} <=> x = {Fraction(-c/b)}'
                x1 = Fraction(-c/b)
                x2 = x1

        strParabola = quadratic_function(x1, x2, a, b, c, Fraction(b * b - 4 * a * c))

        strALL = strIF1 + '\n' + strUravnenie
        if strDiss != '':
            strALL += '\n' + strDiss
        if strX1 != '':
            strALL += 2*'\n' + strX1
        if strX2 != '':
            strALL += '\n' + strX2
        if str_quad_trinomial != '':
            strALL += 2 * '\n' + strIF2 + '\n' + str_quad_trinomial
        strALL += 2*'\n' + strIF3 + '\n' + strParabola
        bot.send_message(message.chat.id, strALL)
        print(f'Пользователь {message.chat.first_name}(id={message.chat.id}) '
              f'отправил боту сообщение: "{message.text}". Сообщение успешно.')
    except:
        print(f'Пользователь {message.chat.first_name}(id={message.chat.id}) '
              f'отправил боту сообщение: "{message.text}". Получена ошибка.')
        bot.send_message(message.chat.id, errorMessage)

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)


    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(
            url="https://quadraticequationsbot.herokuapp.com/")  # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
#bot.polling(none_stop=True, interval=0)
