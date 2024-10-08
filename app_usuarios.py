import sqlite3
import hashlib

# Conectar a la base de datos SQLite (se creará si no existe)
conexion = sqlite3.connect('usuarios.db')
cursor = conexion.cursor()

# Crear la tabla de usuarios (si no existe)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT UNIQUE NOT NULL,
        hash_contraseña TEXT NOT NULL
    )
''')
conexion.commit()

# Función para hashear la contraseña
def hashear_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Función para registrar un usuario
def registrar_usuario(nombre, correo, contraseña):
    try:
        # Validar si el correo ya está registrado
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        if cursor.fetchone():
            print("El correo ya está registrado.")
            return False
        
        # Hashear la contraseña
        hash_contraseña = hashear_contraseña(contraseña)
        
        # Insertar el usuario en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, correo, hash_contraseña) VALUES (?, ?, ?)", 
                       (nombre, correo, hash_contraseña))
        conexion.commit()
        print("Usuario registrado exitosamente.")
        return True
    except sqlite3.Error as e:
        print(f"Error al registrar usuario: {e}")
        return False

# Función para iniciar sesión
def iniciar_sesion(correo, contraseña):
    try:
        # Obtener el usuario por correo
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        
        if usuario:
            id, nombre, correo_db, hash_contraseña_db = usuario
            # Verificar la contraseña
            if hashear_contraseña(contraseña) == hash_contraseña_db:
                print(f"Sesión iniciada. ¡Bienvenido, {nombre}!")
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print("No se encontró ningún usuario con ese correo.")
            return False
    except sqlite3.Error as e:
        print(f"Error al iniciar sesión: {e}")
        return False

# Ejemplo básico de uso
if __name__ == "__main__":
    while True:
        print("\n1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            contraseña = input("Contraseña: ")
            registrar_usuario(nombre, correo, contraseña)
        
        elif opcion == '2':
            correo = input("Correo: ")
            contraseña = input("Contraseña: ")
            iniciar_sesion(correo, contraseña)

        elif opcion == '3':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida.")

