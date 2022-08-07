from sqlalchemy import create_engine
import MySQLdb

# Connecting to the SQL database.
con = MySQLdb.connect(host = '3.25.191.104',
                      user = 'mysql',
                      passwd = 'TP08',
                      db = 'tp08_website')

# Engine used to upload data to the database.
engine = create_engine('mysql://mysql:TP08@3.25.191.104:3306/tp08_website')

# Establishing a cursor to allow SQL queries.
cur = con.cursor()