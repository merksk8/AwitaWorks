import mysql.connector
import config


# INICIO DE MYSQL CONECTOR
mydb = mysql.connector.connect(
    host = config.databaseUrl,
    user = config.databaseUser,
    password = config.databasePassword,
    database = config.databaseName
)