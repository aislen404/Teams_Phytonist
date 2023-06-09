import requests
import os
from colorama import init
from termcolor import colored

# Variables globales
user_id = None
access_token = None
group_id = None
equipo_actual = None

def login_usuario():
    borrarPantalla()
    global user_id, access_token
    print(colored("== Proveer Access Token ==",'blue','on_yellow'))
    # token_file = input("Introduce el nombre del archivo que contiene el access_token: ")
    token_file = 'access_token.txt'
    try:
        with open(token_file, 'r') as file:
            access_token = file.read().strip()
        user_id = obtener_user_id()
        if user_id:
            print(colored("¡Inicio de sesión exitoso!",'white','on_black'))
        else:
            print(colored("Error en el inicio de sesión. Verifica el access_token.",'red','on_white'))
    except FileNotFoundError:
        print(colored("Archivo no encontrado. Verifica el nombre y la ubicación del archivo.",'red','on_white'))

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

def listar_mis_teams():
    global access_token
    print(colored("== Listar mis Teams ==",'blue','on_yellow'))
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me/joinedTeams', headers=headers)
    if response.status_code == 200:
        teams = response.json().get('value', [])
        if teams:
            print(colored("Mis Teams:",'white','on_black'))
            for team in teams:
                team_id = team.get('id')
                team_name = team.get('displayName')
                print(f"ID: {team_id} - Nombre: {team_name}")
        else:
            print(colored("No perteneces a ningún Team.",'red','on_white'))
    else:
        print(colored("Error al obtener la lista de Teams:",'red','on_white'))
        print(response.text)

def crear_equipo():
    global equipo_actual
    print(colored("== Crear Teams ==",'blue','on_yellow'))
    display_name = input("Introduce el nombre del Team: ")
    description = input("Introduce la descripción del Team: ")
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
        print(f"Team '{display_name}' creado exitosamente.")
        trabajar_equipo_actual()
    else:
        print (Colored("Error al crear el Team:",'red','on_white'))
        print (response.text)

def conectar_equipo():
    global equipo_actual
    print(colored("== Conectar a Team ==",'blue','on_yellow'))
    equipo_actual = input("Introduce el UID del Team (no se validara hasta su empleo en alguna accion): ")
    trabajar_equipo_actual()

def crear_canal_publico():
    global equipo_actual
    print(colored("== Crear Canal Público ==",'yellow','on_blue'))
    canal_name = input("Introduce el nombre del canal público: ")

    # Código para crear el canal público en el equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "displayName": canal_name,
        "description": "Canal público",
        "auto-pin": "On"
    }
    response = requests.post(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers, json=data)

    if response.status_code == 201:
        channel_id = response.json()['id']
        print(colored(f"Canal público '{canal_name}' creado exitosamente con ID: {channel_id}",'green','on_red'))
    else:
        print(colored("Error al crear el canal público:",'red','on_white'))
        print(response.text)

def crear_canal_privado():
    global equipo_actual
    print(colored("== Crear Canal Privado ==",'yellow','on_blue'))
    canal_name = input("Introduce el nombre del canal privado: ")

    # Código para crear el canal privado en el equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    data = {
        "displayName": canal_name,
        "description": "Canal privado",
        "membershipType": "private",
        "auto-pin": "On"
    }
    response = requests.post(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers, json=data)

    if response.status_code == 201:
        channel_id = response.json()['id']
        print(colored(f"Canal privado '{canal_name}' creado exitosamente con ID: {channel_id}",'green','on_red'))
    else:
        print(colored("Error al crear el canal privado:",'red','on_white'))
        print(response.text)

def listar_canales():
    global equipo_actual
    print(colored("== Listar Canales Disponibles ==",'yellow','on_blue'))

    # Código para obtener y mostrar la lista de canales del equipo actual
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(f"https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels", headers=headers)

    if response.status_code == 200:
        canales = response.json().get('value', [])
        if canales:
            print(colored("Lista de canales:",'white','on_black'))
            for canal in canales:
                canal_id = canal.get('id')
                canal_nombre = canal.get('displayName')
                print(f"ID: {canal_id} - Nombre: {canal_nombre}")
        else:
            print(colored("No se encontraron canales en el equipo.",'red','on_white'))
    else:
        print(colored("Error al obtener la lista de canales:",'red','on_white'))
        print(response.text)

def listar_archivos_en_canal():
    global access_token
    print(colored("== Listar archivos en canal ==",'blue','on_yellow'))

    # Obtener el ID del canal
    canal_id = input("Introduce el ID del canal: ")

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://graph.microsoft.com/v1.0/teams/{equipo_actual}/channels/{canal_id}/filesFolder', headers=headers)
    if response.status_code == 200:
        files = response.json().get('value', [])
        if files:
            print(colored("Archivos en el canal:",'white','on_black'))
            for file in files:
                file_id = file.get('id')
                file_name = file.get('name')
                created_date_time = file.get('createdDateTime')
                last_modified_date_time = file.get('lastModifiedDateTime')
                web_url = file.get('webUrl')
                size = file.get('size')
                drive_id = file.get('parentReference', {}).get('driveId')
                drive_type = file.get('parentReference', {}).get('driveType')
                created_date = file.get('fileSystemInfo', {}).get('createdDateTime')
                last_modified_date = file.get('fileSystemInfo', {}).get('lastModifiedDateTime')
                child_count = file.get('folder', {}).get('childCount')

                print(f"ID: {file_id}")
                print(f"Nombre: {file_name}")
                print(f"Fecha de creación: {created_date_time}")
                print(f"Última fecha de modificación: {last_modified_date_time}")
                print(f"URL: {web_url}")
                print(f"Tamaño: {size} bytes")
                print(f"ID del drive: {drive_id}")
                print(f"Tipo de drive: {drive_type}")
                print(f"Fecha de creación del archivo: {created_date}")
                print(f"Última fecha de modificación del archivo: {last_modified_date}")
                print(f"Número de archivos en la carpeta: {child_count}")
                print("-" * 20)
        else:
            print(colored("No hay archivos en el canal.",'white','on_black'))
    else:
        print(colored("Error al listar archivos:",'red','on_white'))
        print(response.text)

def obtener_url_carpeta_archivos(equipo_id, canal_id):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    url = f"https://graph.microsoft.com/v1.0/teams/{equipo_id}/channels/{canal_id}/filesFolder"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        url_carpeta = data.get('webUrl')
        print(f"La URL de la carpeta de archivos del canal es: {url_carpeta}")
        return url_carpeta
    else:
        print(f"Error al obtener la URL de la carpeta de archivos del canal: {response.text}")
        return None

def cargar_archivo_en_canal(canal_id, ruta_local):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    # Obtener lista de archivos en la carpeta local
    archivos = os.listdir(ruta_local)

    # Copiar cada archivo al canal
    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        url_carpeta = obtener_url_carpeta_archivos(equipo_actual, canal_id)
        if url_carpeta:
            url = f"{url_carpeta}/{nombre_archivo}/content"
            ruta_archivo = os.path.join(ruta_local, archivo)
            with open(ruta_archivo, 'rb') as file:
                response = requests.put(url, headers=headers, data=file)
                if response.status_code == 202:
                    print(f"Archivo '{nombre_archivo}' copiado exitosamente al canal.")
                else:
                    print(colored("Error al copiar el archivo:", 'red', 'on_white'))
                    print(colored(nombre_archivo, 'red', 'on_white'))
                    print(colored(response.text, 'red', 'on_white'))

def copiar_archivos_al_canal():
    global equipo_actual
    print(colored("== Copiar Archivos al Canal ==",'yellow','on_blue'))

    # Obtener el ID del canal
    canal_id = input("Introduce el ID del canal: ")

    # Obtener la ruta local de la carpeta con los archivos a copiar
    ruta_local = os.path.join(os.path.dirname(__file__), 'Prueba')

    if not os.path.isdir(ruta_local):
        print(colored("La ruta especificada no es una carpeta válida.",'red'))
        return

    cargar_archivo_en_canal(canal_id, ruta_local)

def borrarPantalla(): #Definimos la función estableciendo el nombre que queramos
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")

def trabajar_equipo_actual():
    borrarPantalla()
    global equipo_actual
    print(colored(f"\n=== TRABAJANDO SOBRE EL TEAMS {equipo_actual} ===",'green','on_red'))
    while True:
        print(colored("\n=== OPCIONES ===",'blue','on_yellow'))
        print("1. Crear Canal Público")
        print("2. Crear Canal Privado")
        print("3. Listar Canales Disponibles")
        print("4. Listar Archivos en Canal")
        print("5. Copiar Filesystem a Canal")
        print("6. Volver al Menú Principal")

        opcion = input("Selecciona una opción (1-6): ")

        if opcion == '1':
            crear_canal_publico()
        elif opcion == '2':
            crear_canal_privado()
        elif opcion == '3':
            listar_canales()
        elif opcion == '4':
            listar_archivos_en_canal()    
        elif opcion == '5':
            copiar_archivos_al_canal()            
        elif opcion == '6':
            borrarPantalla()
            break
        else:
            print(colored("Opción inválida. Intenta de nuevo.",'red'))

def volver_menu_principal():
    input("\nPresiona Enter para volver al menú principal...")
    borrarPantalla()
    mostrar_menu_principal()

def mostrar_menu_principal():
    opcion = None
    while opcion != '5':
        borrarPantalla()
        print(colored("=== MENÚ PRINCIPAL ===",'green','on_red'))
        print("1. Proveer Access Token")
        print("2. Listar mis Teams")
        print("3. Crear Team")
        print("4. Conectar a un Team")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            login_usuario()
        elif opcion == '2':
            listar_mis_teams()
        elif opcion == '3':
            crear_equipo()
        elif opcion == '4':
            conectar_equipo()
        elif opcion == '5':
            borrarPantalla()
            break
        else:
            print(colored("Opción inválida. Por favor, selecciona una opción válida.",'red','on_white'))
        input("Presiona Enter para continuar...")

mostrar_menu_principal()
