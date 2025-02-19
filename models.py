from db import conn

def create_employees():
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            create table if not exists employees (
                id serial primary key,
                name varchar(100) not null,
                email varchar(100) not null unique,
                position varchar(100) not null,
                salary numeric not null,
                createdAt timestamp default current_timestamp
            )    
        ''')

        conn.commit()
        print('Tables created successfully.')

    else:
        print('No database connection available. Cannot create tables.')