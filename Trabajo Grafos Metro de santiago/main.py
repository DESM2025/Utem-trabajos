from Funciones import get_valid_station, find_best_route, get_valid_time  # Importar las funciones necesarias
from datetime import timedelta

#Diego Silva Madariaga 
#20.965.500-4


def main():
    print("Bienvenido al sistema de rutas del Metro de Santiago.")

    # Solicitar la hora de salida
    start_time = get_valid_time("Ingrese la hora de salida (HH:MM en formato 24 horas): ")

    # Validar las estaciones de origen y destino
    start_station = get_valid_station("Ingrese la estación de origen: ")
    end_station = get_valid_station("Ingrese la estación de destino: ")

    # Validar opción de minimizar transbordos
    minimize_transfers = input("¿Desea minimizar transbordos? (si/no): ").lower() == 'si'

    # Encontrar la mejor ruta
    path, time = find_best_route(start_station, end_station, minimize_transfers)

    # Calcular la hora de llegada sumando el tiempo estimado en minutos
    arrival_time = start_time + timedelta(minutes=time)

    # Imprimir los resultados
    print(f"Ruta: {' -> '.join(path)}")
    print(f"Tiempo estimado: {time} minutos")
    print(f"Hora de llegada estimada: {arrival_time.strftime('%H:%M')}")

if __name__ == "__main__":
    main()
