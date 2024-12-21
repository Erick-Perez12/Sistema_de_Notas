import bcrypt
from app.connectionPool.pool import MySQLPool
from werkzeug.security import generate_password_hash, check_password_hash

mysql_pool = MySQLPool()

class UserModel:
    def __init__(self, id=None, nombre=None, email=None, contrasena=None, rol=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.rol = rol
    
    @classmethod
    def get_by_email(cls, email):
        sql = "SELECT * FROM Usuarios WHERE email = %s"
        result = mysql_pool.execute(sql, (email,))
        if result:
            user_data = result[0]
            user_data = list(user_data)
            user_data[3] = user_data[3].decode('utf-8') if isinstance(user_data[3], (bytes, bytearray)) else user_data[3]
            print(user_data)
            return user_data
        return None

    @classmethod
    def get_by_id(cls, user_id):
        sql = "SELECT id, nombre, email, rol* FROM Usuarios WHERE id = %s"
        result = mysql_pool.execute(sql, (user_id,))
        if result:
            user_data = result[0]
            return cls(*user_data)
        return None

    @classmethod
    def add_user(cls, nombre, email, contrasena, rol):
        sql = """
            INSERT INTO Usuarios (nombre, email, contrasena, rol)
            VALUES (%s, %s, %s, %s)
        """
        mysql_pool.execute(sql, (nombre, email, contrasena, rol), commit=True)
        return True

    def check_password(self, password):
        # Decrypt the stored password and check against the provided password
        stored_password = self.contrasena
        return check_password_hash(stored_password, password)

    def set_password(self, password):
        # Encrypt password using bcrypt and update the user's password
        self.contrasena = generate_password_hash(password)
