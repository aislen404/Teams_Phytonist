import requests
import os

# Variables globales
user_id = None
access_token = None
group_id = None
equipo_actual = None

def login_usuario():
    global user_id, access_token
    print("== Proveer Access Token ==")
    # token_file = input("Introduce el nombre del archivo que contiene el access_token: ")
    token_file = 'access_token.txt'
    try:
        with open(token_file, 'r') as file:
            access_token = file.read().strip()
        user_id = obtener_user_id()
        if user_id:
            print("¡Inicio de sesión exitoso!")
        else:
            print("Error en el inicio de sesión. Verifica el access_token.")
    except FileNotFoundError:
        print("Archivo no encontrado. Verifica el nombre y la ubicación del archivo.")

def obtener_user_id():
    global access_token
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    if response.status_code == 200:
        return response.json().get('id')
    return None

def crear_equipo():
    global equipo_actual
    print("== Crear Teams ==")
    display_name = input("Introduce el nombre del grupo: ")
    description = input("Introduce la descripción del grupo: ")
    group_data = {
        'template@odata.bind': "https://graph.microsoft.com/v1.0/teamsTemplates('standard')",
        'displayName': display_name,
        'description': description,
        'groupTypes': ['Unified']
    }
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.post('https://graph.microsoft.com/v1.0/teams', headers=headers, json=group_data)
    if response.status_code == 202:
        location = response.headers['Location']
        group_id_start = location.find("(") + 1
        group_id_end = location.find(")")
        group_id = location[group_id_start:group_id_end]
        group_id = group_id[1:]
        group_id = group_id[:-1]
        equipo_actual = group_id
        print(f"Equipo '{display_name}' creado exitosamente.")
        trabajar_equipo_actual()
    else:
        print("Error al crear el equipo:", response.text)

def trabajar_equipo_actual():
    global equipo_actual
    print(f"\n=== TRABAJANDO SOBRE EL EQUIPO {equipo_actual} ===")
    while True:
        print("\n=== OPCIONES ===")
        print("1. Crear Canal Público")
        print("2. Crear Canal Privado")
        print("3. Listar Canales Disponibles")
        print("4. Volver al Menú Principal")

        opcion = input("Selecciona una opción (1-4): ")

        if opcion == '1':
            crear_canal_publico()
        elif opcion == '2':
            crear_canal_privado()
        elif opcion == '3':
            listar_canales()
        elif opcion == '4':
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

def crear_canal_publico():
    global equipo_actual
    print("== Crear Canal Público ==")
    canal_name = input("Introduce el nombre del canal público: ")

    # Código para crear el canal público en el equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "displayName": canal_name,
        "description": "Canal público"
    }
    response = requests.post(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers, json=data)

    if response.status_code == 201:
        channel_id = response.json()['id']
        print(f"Canal público '{canal_name}' creado exitosamente con ID: {channel_id}")
    else:
        print("Error al crear el canal público:", response.text)

def crear_canal_privado():
    global equipo_actual
    print("== Crear Canal Privado ==")
    canal_name = input("Introduce el nombre del canal privado: ")

    # Código para crear el canal privado en el equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "displayName": canal_name,
        "description": "Canal privado",
        "membershipType": "private"
    }
    response = requests.post(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers, json=data)

    if response.status_code == 201:
        channel_id = response.json()['id']
        print(f"Canal privado '{canal_name}' creado exitosamente con ID: {channel_id}")
    else:
        print("Error al crear el canal privado:", response.text)

def listar_canales():
    global equipo_actual
    print("== Listar Canales Disponibles ==")

    # Código para obtener y mostrar la lista de canales del equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers)

    if response.status_code == 200:
        canales = response.json().get('value', [])
        if canales:
            print("Lista de canales:")
            for canal in canales:
                canal_id = canal.get('id')
                canal_nombre = canal.get('displayName')
                print(f"ID: {canal_id} - Nombre: {canal_nombre}")
        else:
            print("No se encontraron canales en el equipo.")
    else:
        print("Error al obtener la lista de canales:", response.text)

def borrarPantalla(): #Definimos la función estableciendo el nombre que queramos
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")

def volver_menu_principal():
    input("\nPresiona Enter para volver al menú principal...")
    mostrar_menu_principal()

def mostrar_menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Proveer Access Token")
        print("2. Crear Equipo")
        print("3. Salir")

        opcion = input("Selecciona una opción (1-3): ")

        if opcion == '1':
            login_usuario()
        elif opcion == '2':
            if user_id and access_token:
                crear_equipo()
            else:
                print("Primero debes iniciar sesión.")
        elif opcion == '3':
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

        if opcion == '3':
            break

# Ejecución del script
mostrar_menu_principal()
