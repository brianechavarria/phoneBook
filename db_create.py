import psycopg2

with open('phonebook credentials.txt') as f:
    lines = f.read().splitlines()

USER = lines[0]
PASS = lines[1]
conn = psycopg2.connect(
    dbname='phonebook',
    user=USER,
    password=PASS)



point = conn.cursor()

command = ("CREATE TABLE contacts ( contact_id SERIAL PRIMARY KEY, contact_name VARCHAR(255), phone_number VARCHAR(12) NOT NULL)")

point.execute(command)




point.close()
conn.commit()