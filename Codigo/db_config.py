import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Estabelece e retorna uma conexão com o banco de dados."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Se você definiu uma senha no XAMPP, coloque-a aqui
            database="sistema_clientes"
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None 