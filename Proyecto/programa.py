from datos import (
    guardar_dato, buscar_dato_existente, eliminar_archivo_dato,
    obtener_archivos_guardados, cargar_datos_desde_archivo,
    actualizar_contenido_archivo, eliminar_archivos, renombrar_archivo
)
import os

# Diccionario para almacenar temporalmente los datos ingresados por el usuario
datos_actuales = {
    "nombre": None,
    "apellido": None,
    "telefono": None,
    "email": None
}

def limpiar_datos_actuales():
    """Limpia los datos ingresados por el usuario."""
    global datos_actuales
    datos_actuales = {
        "nombre": None,
        "apellido": None,
        "telefono": None,
        "email": None
    }

def mostrar_menu_principal():
    """Muestra el menú principal de opciones."""
    print("\n--- Menú Principal ---")
    print("1. Agregar Nombre")
    print("2. Agregar Apellido")
    print("3. Agregar Teléfono")
    print("4. Agregar Email")
    print("5. Eliminar Dato (temporal)")
    print("6. Guardar y Salir")
    print("7. Datos Guardados")
    print("8. Salir")
    print("----------------------")

def mostrar_menu_datos_guardados():
    """Muestra el submenú de gestión de datos guardados."""
    print("\n--- Gestión de Datos Guardados ---")
    print("1. Ver Datos")
    print("2. Editar Datos")
    print("3. Eliminar Datos")
    print("4. Regresar")
    print("---------------------------------")

def agregar_dato(tipo_dato):
    """
    Permite al usuario agregar un tipo de dato específico (nombre, apellido, etc.).
    Valida si el dato ya fue ingresado y si existe en otros archivos.
    """
    global datos_actuales
    if datos_actuales[tipo_dato] is not None:
        print(f"\n¡Ya has ingresado un {tipo_dato}: {datos_actuales[tipo_dato]}!")
        return

    valor = input(f"Ingresa el {tipo_dato}: ").strip()
    if not valor:
        print(f"El {tipo_dato} no puede estar vacío.")
        return

    # Validar si el dato ya existe en algún archivo .txt
    archivo_existente = buscar_dato_existente(tipo_dato, valor)
    if archivo_existente:
        print(f"\n¡Advertencia! Ya existe un archivo '{archivo_existente}' que contiene el {tipo_dato} '{valor}'.")
        respuesta = input("¿Deseas eliminar este archivo existente? (s/n): ").lower()
        if respuesta == 's':
            if eliminar_archivo_dato(archivo_existente):
                print(f"Archivo '{archivo_existente}' eliminado correctamente.")
            else:
                print(f"No se pudo eliminar el archivo '{archivo_existente}'.")
            return # Después de eliminar, no se agrega el dato actual para evitar duplicidad inmediata
        else:
            print(f"El {tipo_dato} '{valor}' no se agregará para evitar duplicidad.")
            return

    datos_actuales[tipo_dato] = valor
    print(f"{tipo_dato.capitalize()} '{valor}' agregado temporalmente.")

def eliminar_dato_temporal():
    """Permite al usuario eliminar un dato temporalmente ingresado."""
    global datos_actuales
    datos_disponibles = [key for key, value in datos_actuales.items() if value is not None]

    if not datos_disponibles:
        print("No hay datos temporales para eliminar.")
        return

    print("\n--- Datos Temporales Ingresados ---")
    for i, dato in enumerate(datos_disponibles):
        print(f"{i+1}. {dato.capitalize()}: {datos_actuales[dato]}")
    print(f"{len(datos_disponibles) + 1}. Cancelar")

    try:
        opcion = int(input("Selecciona el número del dato a eliminar o cancelar: "))
        if 1 <= opcion <= len(datos_disponibles):
            dato_a_eliminar = datos_disponibles[opcion - 1]
            valor_eliminado = datos_actuales[dato_a_eliminar]
            datos_actuales[dato_a_eliminar] = None
            print(f"El {dato_a_eliminar} '{valor_eliminado}' ha sido eliminado temporalmente.")
        elif opcion == len(datos_disponibles) + 1:
            print("Operación cancelada.")
        else:
            print("Opción inválida.")
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.")

def guardar_y_salir():
    """
    Guarda los datos temporales en un archivo .txt y sale del programa.
    Valida que todos los datos necesarios estén presentes.
    """
    global datos_actuales
    if not all(datos_actuales.values()):
        print("\n¡Error! Faltan datos por ingresar para guardar el archivo.")
        for key, value in datos_actuales.items():
            if value is None:
                print(f"- Falta: {key.capitalize()}")
        return False # Indica que no se pudo guardar y por lo tanto no se debe salir

    while True:
        nombre_archivo = input("Ingresa un nombre para el archivo (sin .txt): ").strip()
        if not nombre_archivo:
            print("El nombre del archivo no puede estar vacío.")
            continue
        nombre_archivo_completo = nombre_archivo + ".txt"
        if guardar_dato(nombre_archivo_completo, datos_actuales):
            print(f"Datos guardados exitosamente en '{nombre_archivo_completo}'.")
            limpiar_datos_actuales() # Limpiar después de guardar
            return True # Indica que se guardó y se puede salir
        else:
            print("Hubo un error al guardar los datos. Inténtalo de nuevo.")
            return False # En caso de error al guardar, no se debe salir

def ver_datos_guardados():
    """Muestra una lista de todos los archivos .txt guardados y permite ver su contenido."""
    archivos = obtener_archivos_guardados()
    if not archivos:
        print("No hay archivos de datos guardados.")
        return

    print("\n--- Archivos de Datos Guardados ---")
    for i, archivo in enumerate(archivos):
        print(f"{i+1}. {archivo}")
    print("---------------------------------")

    while True:
        opcion_ver = input("Ingresa el número del archivo para ver su contenido, o '0' para regresar: ")
        if opcion_ver == '0':
            break
        try:
            indice_archivo = int(opcion_ver) - 1
            if 0 <= indice_archivo < len(archivos):
                mostrar_contenido_archivo(archivos[indice_archivo])
            else:
                print("Opción inválida.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def mostrar_contenido_archivo(nombre_archivo):
    """Muestra el contenido de un archivo de datos específico."""
    datos = cargar_datos_desde_archivo(nombre_archivo)
    if datos:
        print(f"\n--- Contenido de '{nombre_archivo}' ---")
        for key, value in datos.items():
            print(f"{key.capitalize()}: {value}")
        print("----------------------------------")
    else:
        print(f"No se pudo cargar el contenido del archivo '{nombre_archivo}'.")

def editar_datos_guardados():
    """Permite al usuario editar el nombre o el contenido de un archivo .txt."""
    archivos = obtener_archivos_guardados()
    if not archivos:
        print("No hay archivos para editar.")
        return

    ver_datos_guardados() # Muestra la lista de archivos para que el usuario elija
    try:
        opcion_archivo = int(input("Selecciona el número del archivo a editar: "))
        if 1 <= opcion_archivo <= len(archivos):
            nombre_archivo_original = archivos[opcion_archivo - 1]
            print(f"\n--- Editando '{nombre_archivo_original}' ---")
            print("1. Renombrar Archivo")
            print("2. Editar Contenido")
            print("3. Cancelar")
            sub_opcion = input("Selecciona una opción: ")

            if sub_opcion == '1':
                nuevo_nombre = input("Ingresa el nuevo nombre para el archivo (sin .txt): ").strip()
                if not nuevo_nombre:
                    print("El nuevo nombre no puede estar vacío.")
                    return
                nuevo_nombre_completo = nuevo_nombre + ".txt"
                if renombrar_archivo(nombre_archivo_original, nuevo_nombre_completo):
                    print(f"Archivo renombrado a '{nuevo_nombre_completo}' exitosamente.")
                else:
                    print("No se pudo renombrar el archivo.")
            elif sub_opcion == '2':
                datos_del_archivo = cargar_datos_desde_archivo(nombre_archivo_original)
                if not datos_del_archivo:
                    print("No se pudo cargar el contenido del archivo.")
                    return

                print("\nContenido actual del archivo:")
                for key, value in datos_del_archivo.items():
                    print(f"{key.capitalize()}: {value}")

                while True:
                    campo_a_editar = input("¿Qué campo deseas editar? (nombre, apellido, telefono, email, o 'salir'): ").lower().strip()
                    if campo_a_editar == 'salir':
                        break
                    if campo_a_editar in datos_del_archivo:
                        nuevo_valor = input(f"Ingresa el nuevo valor para '{campo_a_editar}': ").strip()
                        if not nuevo_valor:
                            print("El valor no puede estar vacío.")
                            continue
                        datos_del_archivo[campo_a_editar] = nuevo_valor
                        print(f"'{campo_a_editar.capitalize()}' actualizado a '{nuevo_valor}'.")
                    else:
                        print("Campo no válido. Intenta de nuevo.")

                if actualizar_contenido_archivo(nombre_archivo_original, datos_del_archivo):
                    print("Contenido del archivo actualizado exitosamente.")
                else:
                    print("No se pudo actualizar el contenido del archivo.")

            elif sub_opcion == '3':
                print("Edición cancelada.")
            else:
                print("Opción inválida.")
        else:
            print("Opción de archivo inválida.")
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.")

def eliminar_datos_guardados():
    """Permite al usuario eliminar uno o todos los archivos .txt guardados."""
    archivos = obtener_archivos_guardados()
    if not archivos:
        print("No hay archivos para eliminar.")
        return

    ver_datos_guardados() # Muestra la lista de archivos para que el usuario elija
    print("\n--- Opciones de Eliminación ---")
    print("1. Eliminar un archivo específico")
    print("2. Eliminar todos los archivos")
    print("3. Cancelar")
    opcion_eliminacion = input("Selecciona una opción: ")

    if opcion_eliminacion == '1':
        try:
            opcion_archivo = int(input("Selecciona el número del archivo a eliminar: "))
            if 1 <= opcion_archivo <= len(archivos):
                archivo_a_eliminar = archivos[opcion_archivo - 1]
                confirmacion = input(f"¿Estás seguro de eliminar '{archivo_a_eliminar}'? (s/n): ").lower()
                if confirmacion == 's':
                    if eliminar_archivo_dato(archivo_a_eliminar):
                        print(f"Archivo '{archivo_a_eliminar}' eliminado exitosamente.")
                    else:
                        print("No se pudo eliminar el archivo.")
                else:
                    print("Eliminación cancelada.")
            else:
                print("Opción de archivo inválida.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")
    elif opcion_eliminacion == '2':
        confirmacion = input("¿Estás seguro de eliminar TODOS los archivos? Esta acción es irreversible. (s/n): ").lower()
        if confirmacion == 's':
            if eliminar_archivos(archivos):
                print("Todos los archivos han sido eliminados exitosamente.")
            else:
                print("Hubo un error al intentar eliminar todos los archivos.")
        else:
            print("Eliminación de todos los archivos cancelada.")
    elif opcion_eliminacion == '3':
        print("Operación de eliminación cancelada.")
    else:
        print("Opción inválida.")


def iniciar_interfaz():
    """
    Función principal que ejecuta el bucle de la interfaz de usuario.
    """
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            agregar_dato("nombre")
        elif opcion == '2':
            agregar_dato("apellido")
        elif opcion == '3':
            agregar_dato("telefono")
        elif opcion == '4':
            agregar_dato("email")
        elif opcion == '5':
            eliminar_dato_temporal()
        elif opcion == '6':
            if guardar_y_salir():
                break # Sale del bucle principal si se guarda exitosamente
        elif opcion == '7':
            while True:
                mostrar_menu_datos_guardados()
                sub_opcion = input("Selecciona una opción: ")
                if sub_opcion == '1':
                    ver_datos_guardados()
                elif sub_opcion == '2':
                    editar_datos_guardados()
                elif sub_opcion == '3':
                    eliminar_datos_guardados()
                elif sub_opcion == '4':
                    break # Regresa al menú principal
                else:
                    print("Opción inválida. Intenta de nuevo.")
        elif opcion == '8':
            confirmacion = input("¿Estás seguro de salir? (s/n): ").lower()
            if confirmacion == 's':
                if any(datos_actuales.values()):
                    print("¡Advertencia! Tienes datos ingresados que no han sido guardados.")
                    confirmar_anular = input("Si continúas, los datos se anularán. ¿Deseas salir de todas formas? (s/n): ").lower()
                    if confirmar_anular == 's':
                        print("Saliendo del programa. Los datos no guardados han sido anulados.")
                        break
                    else:
                        print("Operación de salida cancelada.")
                else:
                    print("Saliendo del programa.")
                    break
            else:
                print("Operación de salida cancelada.")
        else:
            print("Opción inválida. Por favor, selecciona una opción del 1 al 8.")