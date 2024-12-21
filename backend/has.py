from flask_bcrypt import Bcrypt

# Inicializa bcrypt
bcrypt = Bcrypt()

# Lista de contraseñas en texto plano
passwords = [
    'password1', 'password2', 'password3', 'password4', 'password5',
    'password6', 'password7', 'password8', 'password9', 'password10'
]

# Generar hashes de contraseñas
hashed_passwords = [(password, bcrypt.generate_password_hash(password).decode('utf-8')) for password in passwords]

# Imprime los resultados
for plain, hashed in hashed_passwords:
    print(f"'{plain}': '{hashed}'")
