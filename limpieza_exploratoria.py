import pandas as pd

def main():
    print("=====================================================")
    print("🚀 SCRIPT DE LIMPIEZA Y ANÁLISIS EXPLORATORIO (F1) 🚀")
    print("=====================================================\n")

    # Emulación del do/while en Python
    while True:
        # 1. EL SISTEMA PIDE EL ARCHIVO AL USUARIO
        ruta_archivo = input("\nPor favor, ingresa el nombre o la ruta del archivo CSV a procesar (ej. results.csv): ")

        try:
            # Carga del dataset reconociendo '\N' como nulo
            print(f"\n[INFO] Cargando '{ruta_archivo}'...")
            df = pd.read_csv(ruta_archivo, na_values=r'\N')
            print(f"[ÉXITO] Archivo cargado correctamente. Dimensiones iniciales: {df.shape}\n")
            
        except FileNotFoundError:
            # MENÚ EN CASO DE ERROR
            print(f"[ERROR] No se encontró el archivo '{ruta_archivo}'. Verifica la ruta.")
            opcion_error = input("¿Deseas intentar con otro archivo? (S/N): ").strip().upper()
            if opcion_error == 'S':
                continue  # Vuelve al inicio del bucle
            else:
                print("Saliendo del programa. ¡Hasta luego!")
                break     # Rompe el bucle y cierra el programa

        # 2. DIAGNÓSTICO PREVIO
        print("--- DIAGNÓSTICO DE NULOS PRE-LIMPIEZA ---")
        nulos = df.isnull().sum()
        print(nulos[nulos > 0].sort_values(ascending=False).head(), "\n")

        # 3. LIMPIEZA RIGUROSA
        print("[INFO] Iniciando proceso de limpieza...")
        
        df_clean = df.drop_duplicates().copy()
        
        # Validación extra por si el dataset cargado no tiene esta columna
        if 'fastestLapSpeed' in df_clean.columns:
            df_clean['fastestLapSpeed'] = df_clean['fastestLapSpeed'].astype(float)
            mediana_velocidad = df_clean['fastestLapSpeed'].median()
            df_clean['fastestLapSpeed'] = df_clean['fastestLapSpeed'].fillna(mediana_velocidad)
        
        if 'grid' in df_clean.columns and 'laps' in df_clean.columns:
            df_clean = df_clean[(df_clean['grid'] > 0) & (df_clean['laps'] > 0)]
        
        df_clean = df_clean.reset_index(drop=True)

        print(f"[ÉXITO] Limpieza finalizada. Nuevas dimensiones: {df_clean.shape}\n")

        # 4. AGREGACIONES DE NEGOCIO
        print("=====================================================")
        print("📊 RESULTADOS DEL ANÁLISIS DE NEGOCIO 📊")
        print("=====================================================\n")

        if 'constructorId' in df_clean.columns and 'points' in df_clean.columns:
            print("1. Top 5 Escuderías con Más Puntos Históricos:")
            top_escuderias = df_clean.groupby('constructorId')['points'].sum().sort_values(ascending=False).head(5)
            print(top_escuderias.to_string())
            print("\n-----------------------------------------------------\n")

        if 'grid' in df_clean.columns and 'fastestLapSpeed' in df_clean.columns:
            print("2. Promedio de Velocidad Punta (km/h) por Posición de Salida (Top 5):")
            velocidad_por_parrilla = df_clean.groupby('grid')['fastestLapSpeed'].mean().sort_index().head(5)
            print(velocidad_por_parrilla.to_string())
            print("\n-----------------------------------------------------\n")

        if 'driverId' in df_clean.columns and 'positionOrder' in df_clean.columns:
            print("3. Top 5 Pilotos con Mayor Cantidad de Podios:")
            podios = df_clean[df_clean['positionOrder'] <= 3]
            top_pilotos = podios.groupby('driverId')['positionOrder'].count().sort_values(ascending=False).head(5)
            print(top_pilotos.to_string())

        # MENÚ AL FINALIZAR CON ÉXITO
        print("\n=====================================================")
        opcion_exito = input("Análisis completado. ¿Deseas subir y analizar otro archivo? (S/N): ").strip().upper()
        if opcion_exito != 'S':
            print("Cerrando el pipeline de datos. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()