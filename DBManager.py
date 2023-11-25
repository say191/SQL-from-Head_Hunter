import psycopg2  # Импортируем библиотеку для работы с БД


class DBManager:  # Создаем класс для работы с БД
    conn = psycopg2.connect(
        host='localhost',
        database='head_hunter',
        user='postgres',
        password='sayMe123')
    cur = conn.cursor()

    # Записываем подключение и курсор в атрибуты класса, чтобы каждый раз
    # при вызове методов не инициализировать их заново

    @staticmethod
    def get_companies_and_vacancies_count():
        DBManager.cur.execute('SELECT name_company, COUNT(id_vacancy)'
                              'FROM vacancies GROUP BY name_company')
        result = DBManager.cur.fetchall()
        for row in result:
            print(f"{row[0]} - {row[1]}")
        DBManager.cur.close()
        DBManager.conn.close()

        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

    @staticmethod
    def get_all_vacancies():
        DBManager.cur.execute('SELECT *'
                              'FROM vacancies')
        result = DBManager.cur.fetchall()
        for row in result:
            print(f"{row[1]} | {row[2]} | {row[3]} {row[4]}")
        DBManager.cur.close()
        DBManager.conn.close()

        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """

    @staticmethod
    def get_avg_salary():
        DBManager.cur.execute("SELECT CAST (AVG(salary) AS integer)"
                              "FROM vacancies WHERE currency = 'RUR'")
        result = DBManager.cur.fetchall()
        print(f"{result[0][0]} RUB")
        DBManager.cur.close()
        DBManager.conn.close()

        """
        Получает среднюю зарплату по вакансиям.
        """

    @staticmethod
    def get_vacancies_with_higher_salary():
        DBManager.cur.execute("SELECT * "
                              "FROM vacancies "
                              "WHERE currency = 'RUR' "
                              "AND salary > (SELECT AVG(salary) FROM vacancies WHERE currency = 'RUR')")
        result = DBManager.cur.fetchall()
        for row in result:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} {row[4]} | {row[5]}")
        DBManager.cur.close()
        DBManager.conn.close()

        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

    @staticmethod
    def get_vacancies_with_keyword():
        key_word = input('Enter a key word for searching inside BD:\n')
        DBManager.cur.execute("select * "
                              "from vacancies "
                              f"where name_vacancy like '%{key_word}%'")
        result = DBManager.cur.fetchall()
        for row in result:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} {row[4]} | {row[5]}")
        if len(result) == 0:
            print('There are not vacancies with this key word.')
        DBManager.cur.close()
        DBManager.conn.close()

        """
        Получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python.
        """
