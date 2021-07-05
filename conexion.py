import psycopg2

conexion = psycopg2.connect(
    user = "postgres",
    password = "J8v5.f675",
    host="127.0.0.1",
    port = "5432",
    database = "granjas_tester"

)
cursor = conexion.cursor()

print(cursor)