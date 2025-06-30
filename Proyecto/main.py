from programa import iniciar_interfaz
from datos import inicializar_carpeta_datos

def main():
    """
    Función principal que inicializa la aplicación.
    """
    inicializar_carpeta_datos()
    iniciar_interfaz()

if __name__ == "__main__":
    main()