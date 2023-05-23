import mysql.connector
from mysql.connector import Error

def get_interest_rate():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='bank',
                                             user='root',
                                             password='LOCALHOST PASSWORD HERE')

        select_query = "SELECT * FROM interest"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        for row in records:
            id = row["ID"]
            bank_name = row["bank_name"]
            interest_rate = row["interest_rate"]
            print(id, bank_name, interest_rate)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

get_interest_rate()