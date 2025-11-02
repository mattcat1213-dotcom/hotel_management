import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crea y retorna una conexión a la base de datos hotel_db"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',           # Cambia por tu usuario MySQL
            password='1234', # Cambia por tu contraseña
            database='hotel_db'
        )
        return connection
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def verify_user(username, password):
    """Verifica las credenciales de usuario"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

def get_clients():
    """Retorna la lista de clientes"""
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, apellido, dni, estado FROM clients")
        clients = cursor.fetchall()
        cursor.close()
        conn.close()
        return clients
    return []
