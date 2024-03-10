import psycopg2
import os

database_host = os.getenv('DATABASE_HOST', 'localhost')

 # DB Connect
def DBconnect():
    try:
        global cur, conn
        print("자 드가자")
        conn = psycopg2.connect(user= "myuser", password = "mypassword", host = database_host, port = 5432, database="mydatabase")
        print("자 들어갔다")
        cur = conn.cursor()
        print("Database Connect Success")
        return cur, conn
    except Exception as err:
        print(str(err))
        
# DB Close
def DBdisconnect():
    try:
        conn.close()
        cur.close()
        print("DB Connect Close")
    except:
        print("Error: ", "Database Not Connected")