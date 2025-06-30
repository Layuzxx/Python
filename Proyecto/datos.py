import os
import json

CARPETA_DATOS = "Proyecto/datos"

def inicializar_carpeta_datos():
    """Crea la carpeta 'datos' si no existe."""
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)
        print(f"Carpeta '{CARPETA_DATOS}' creada.")

def guardar_dato(nombre_archivo, datos: dict):
    """
    Guarda los datos proporcionados (un diccionario) en un archivo .txt
    dentro de la carpeta 'datos' en formato JSON.
    """
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)
        return True
    except IOError as e:
        print(f"Error al guardar el archivo '{nombre_archivo}': {e}")
        return False

def cargar_datos_desde_archivo(nombre_archivo) -> dict | None:
    """
    Carga los datos desde un archivo .txt específico en la carpeta 'datos'.
    Retorna un diccionario con los datos o None si hay un error.
    """
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    try:
        with open(ruta_completa, 'r', encoding='utf-8') as f:
            return json.load(f) # Carga los datos como un diccionario
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en el archivo '{nombre_archivo}'.")
        return None
    except IOError as e:
        print(f"Error al cargar el archivo '{nombre_archivo}': {e}")
        return None

def buscar_dato_existente(tipo_dato: str, valor_buscado: str) -> str | None:
    """
    Busca si un 'valor_buscado' para un 'tipo_dato' específico
    ya existe en algún archivo .txt guardado.
    Retorna el nombre del archivo si lo encuentra, de lo contrario None.
    """
    for archivo in os.listdir(CARPETA_DATOS):
        if archivo.endswith(".txt"):
            datos = cargar_datos_desde_archivo(archivo)
            if datos and isinstance(datos, dict) and datos.get(tipo_dato) == valor_buscado:
                return archivo
    return None

def eliminar_archivo_dato(nombre_archivo: str) -> bool:
    """
    Elimina un archivo .txt específico de la carpeta 'datos'.
    """
    ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
    try:
        os.remove(ruta_completa)
        return True
    except OSError as e:
        print(f"Error al eliminar el archivo '{nombre_archivo}': {e}")
        return False

def obtener_archivos_guardados() -> tuple:
    """
    Retorna una tupla de todos los nombres de archivos .txt en la carpeta 'datos'.
    """
    # Se convierte la lista a tupla para cumplir con el requisito de usar tuplas
    return tuple(f for f in os.listdir(CARPETA_DATOS) if f.endswith(".txt"))

def actualizar_contenido_archivo(nombre_archivo: str, nuevos_datos: dict) -> bool:
    """
    Actualiza el contenido de un archivo .txt con los nuevos datos (un diccionario).
    """
    return guardar_dato(nombre_archivo, nuevos_datos)

def eliminar_archivos(lista_archivos: tuple) -> bool:
    """
    Elimina una tupla de archivos de la carpeta 'datos'.
    Retorna True si todos se eliminaron, False si hubo algún error.
    """
    todos_eliminados = True
    for archivo in lista_archivos:
        if not eliminar_archivo_dato(archivo):
            todos_eliminados = False
    return todos_eliminados

def renombrar_archivo(nombre_archivo_original: str, nuevo_nombre_archivo: str) -> bool:
    """
    Renombra un archivo en la carpeta 'datos'.
    """
    ruta_original = os.path.join(CARPETA_DATOS, nombre_archivo_original)
    ruta_nueva = os.path.join(CARPETA_DATOS, nuevo_nombre_archivo)
    try:
        os.rename(ruta_original, ruta_nueva)
        return True
    except OSError as e:
        print(f"Error al renombrar el archivo '{nombre_archivo_original}' a '{nuevo_nombre_archivo}': {e}")
        return False