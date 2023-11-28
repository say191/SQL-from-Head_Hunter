from DBManager import DBManager  # Импортируем класс для работы с БД
import requests  # Импортируем библиотеку для дальнейшей работы с api
import json  # Импортируем библиотеку для работы с информацией в удобном формате json
import psycopg2  # Импортируем библиотеку для работы с БД

key_word = input('Welcome dear guest!\n'
                 'You need to enter next parameters for searching vacancies from Head Hunter.\n'
                 'Enter a key word for searching certain profession:\n')
# Приветствуем пользователя и спрашиваем по какому ключевому слову
# мы будем искать вакансии с платформы HeadHunter

params = {'text': key_word,
          'only_with_salary': True,
          'per_page': 100}
# Инициализируем необходимые параметры поиска вакансий
response = requests.get("https://api.hh.ru/vacancies", params)
data = json.loads(response.text)
# Записываем всю информацию о вакансиях в формате json
employers = []
# Создаем пустой список, где будут храниться уникальные значения из id работодателей
# для того, чтобы исключить повторения работодателей и наименований компаний

with psycopg2.connect(
        host='localhost',
        database='head_hunter',
        user='postgres',
        password='sayMe123') as conn:
    with conn.cursor() as cur:
        for vacancy in data['items']:  # Проходимся по каждой из вакансий
            if vacancy['type']['id'] == 'anonymous':
                continue
                # Пропускаем вакансии с анонимными работодателями
            else:
                if vacancy['employer']['id'] not in employers:
                    # Если в списке уже есть такой работодатель, то мы его пропускаем
                    # т к нам нужны уникальный значения (id работодателя) без повторения
                    employers.append(vacancy['employer']['id'])  # Добавляем в список id работодателя или компании
                    cur.execute('INSERT INTO companies VALUES (%s, %s, %s, %s)',
                                (vacancy['employer']['id'], vacancy['employer']['name'],
                                 vacancy['employer']['alternate_url'], vacancy['employer']['trusted']))
                    # Заполняем таблицу companies в БД

            salary = 0
            # Т к на Head Hunter формат з/п имеет атрибут "от" и "до",
            # а нам нужен целочисленный формат значения з/п, придется
            # сделать ряд манипуляций, указанных ниже
            if vacancy['salary']['from'] is None and vacancy['salary']['to'] is not None:
                salary = vacancy['salary']['to']
            # Если у з/п указана только верхняя планка "до", то записываем это значение в переменную з/п
            elif vacancy['salary']['from'] is not None and vacancy['salary']['to'] is None:
                salary = vacancy['salary']['from']
            # Если у з/п указана только нижняя планка "от", то записываем это значение в переменную з/п
            elif vacancy['salary']['from'] is not None and vacancy['salary']['to'] is not None:
                salary = vacancy['salary']['from']
            # Если у з/п указаны и нижняя и верхняя планки, то записываем нижнюю планку в переменную з/п
            cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)',
                        (vacancy['id'], vacancy['name'], vacancy['employer']['name'],
                         salary, vacancy['salary']['currency'], vacancy['alternate_url']))
            # Заполняем таблицу vacancies в БД

conn.close()  # Закрываем подключение
while True:  # Запускаем бесконечный цикл, чтобы контексное меню вызывалось повторно, при вводе неверного значения
    user_action = input('Choose tne next action:\n'
                        '1 - get list of all companies and quantity of vacancies for each company.\n'
                        '2 - get list of all vacancies with name company, name vacancy, salary and url.\n'
                        '3 - get the average salary of all vacancies.\n'
                        '4 - get list of vacancies with a salary higher than the average for all vacancies.\n'
                        '5 - get list of vacancies with using key word for searching.\n'
                        '6 - exit.\n')
    database = DBManager  # Инициализируем экземпляр класса
    if user_action == '1':
        database.get_companies_and_vacancies_count()
        break
    elif user_action == '2':
        database.get_all_vacancies()
        break
    elif user_action == '3':
        database.get_avg_salary()
        break
    elif user_action == '4':
        database.get_vacancies_with_higher_salary()
        break
    elif user_action == '5':
        database.get_vacancies_with_keyword()
        break
    elif user_action == '6':
        quit()
    else:
        print('Please enter a correct number for action.\n')
        continue
    # В зависимости, какое действие будет выбирать пользователь,
    # у класса будет вызываться соответствующий метод или
    # будет осуществлен выход из программы
