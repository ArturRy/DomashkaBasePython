import psycopg2

# data_base = 'domashka1'
# user = 'postgres'
# password = 'Frdfkfyu'
conn = psycopg2.connect(database="domashka", user="postgres", password="Frdfkfyu")


#      Домашнее задание к лекции «Работа с PostgreSQL из Python»


# with conn.cursor() as cur:
#     cur.execute('''
#         DROP TABLE tel_number;
#         DROP TABLE client;
#         ''')
#     conn.commit()


#     Функция, создающая структуру БД (таблицы)


def create_clients_db():
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            second_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NULL);
                ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tel_number(
            client_id INTEGER REFERENCES client(client_id),
            tel_number INTEGER PRIMARY KEY NOT NULL);
                ''')
        conn.commit()
        

    # Функция, позволяющая добавить нового клиента


def add_client(cl_id: int, first_n: str, second_n: str, mail: str):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO client(client_id, first_name, second_name, email) VALUES(%s, %s, %s, %s);
            ''', (cl_id, first_n, second_n, mail))
        conn.commit()
        

# Функция, позволяющая добавить телефон для существующего клиента


def add_tel_number(client_id: int, tel_numb: int):
    with conn.cursor() as cur:
        cur.execute('''
            INSERT INTO tel_number(client_id, tel_number) VALUES(%s, %s);
            ''', (client_id, tel_numb))
        conn.commit()
        

# Функция, позволяющая получить информаю о клиенте по его ID)


def client_data(client_id: int):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT c.first_name, c.second_name, c.email, t.tel_number FROM client c
            LEFT JOIN tel_number t ON c.client_id = t.client_id
            WHERE c.client_id = %s;
            ''', (client_id,))
        print(cur.fetchall())
        

    # Функция, позволяющая изменить данные о клиенте.


def client_modify(client_id):
    info = input('Введите параметр, который вы хотели бы изменить')
    info2 = str(input('Введите новое значение параметра'))
    with conn.cursor() as cur:
        cur.execute(f'''
            UPDATE client
            SET {info} = %s
            WHERE client_id = %s;
            ''', (info2, client_id,))

        conn.commit()
        



# client_modify(1)


def tel_del(clint_id: int):
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM tel_number
            WHERE client_id = %s;
            ''', (clint_id,))
        conn.commit()
        

    # Функция, позволяющая удалить существующего клиента.


def client_del(client_id: int):
    tel_del(client_id)
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM client
            WHERE client_id = %s
            ''', (client_id,))
        conn.commit()
        

    # Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.


def search_client(info):
    with conn.cursor() as cur:
        if type(info) == int:
            cur.execute('''
                SELECT c.client_id FROM client c
                LEFT JOIN tel_number t ON c.client_id = t.client_id
                WHERE t.tel_number = %s
                ''', (info,))
            c_id = list(cur.fetchone())[0]
            for id_c in c_id:
                print('ID клиента:', list(id_c))
                client_data(id_c)
        elif type(info) == str:
            cur.execute('''
                SELECT client_id FROM client 
                WHERE first_name = %s OR second_name = %s OR email = %s;
                ''', (info, info, info,))
            c_id = list(cur.fetchall())
            for id_c in c_id:
                print('ID клиента:', list(id_c))
                client_data(id_c)
        else:
            print('Некорректный тип данных')


# ЕЩЕ одна функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(first_name=None, second_name=None, email=None, tel_number=None):
    with conn.cursor() as cur:
        cur.execute('''
            SELECT c.client_id from client c
            LEFT JOIN tel_number t ON c.client_id = t.client_id
            WHERE (c.first_name = %(first_name)s or %(first_name)s IS NULL)
            AND (c.second_name = %(second_name)s or %(second_name)s IS NULL)
            AND (c.email = %(email)s or %(email)s IS NULL)
            AND (t.tel_number = %(tel_number)s or %(tel_number)s IS NULL);
            ''', {'first_name': first_name, 'second_name': second_name, 'email': email, 'tel_number': tel_number},)
        print(cur.fetchall())


conn.close()
