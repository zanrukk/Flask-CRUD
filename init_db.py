import os
import psycopg2

conn = psycopg2.connect(
        host='0.0.0.0',
        port=54325,
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'username varchar (16) NOT NULL,'
                                 'password varchar (32) NOT NULL,'
                                 'real_name varchar(32) NOT NULL,'
                                 'subscription_start date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO users (username, password, real_name)'
            'VALUES (%s, %s, %s)',
            ('hayreddin123',
             '12345',
             'Hayreddin Kurnaz'),
            ('ali123',
             '12345',
             'Ali Veli')
            )


conn.commit()

cur.close()
conn.close()










