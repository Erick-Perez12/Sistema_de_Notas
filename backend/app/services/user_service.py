from app.connectionPool.pool import MySQLPool

mysql_pool = MySQLPool()

def get_all_users():
    sql = "SELECT * FROM Usuarios"
    return mysql_pool.execute(sql)

def create_user(nombre, email, contrasena, rol):
    sql = """
        INSERT INTO Usuarios (nombre, email, contrasena, rol) 
        VALUES (%s, %s, AES_ENCRYPT(%s, 'secret_key'), %s)
    """
    mysql_pool.execute(sql, (nombre, email, contrasena, rol), commit=True)
