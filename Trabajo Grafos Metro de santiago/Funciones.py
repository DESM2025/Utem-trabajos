import heapq
from datetime import datetime, timedelta
from metro_map import metro_map  # Importar el mapa del metro desde metro_map.py

# Algoritmo de Dijkstra para encontrar la ruta más corta
def dijkstra(graph, start, end):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {station: float('inf') for station in graph}
    distances[start] = 0
    previous_nodes = {station: None for station in graph}

    while queue:
        current_distance, current_station = heapq.heappop(queue)

        if current_station == end:
            break

        for neighbor, weight in graph[current_station].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_station
                heapq.heappush(queue, (distance, neighbor))

    path = []
    station = end
    while previous_nodes[station]:
        path.insert(0, station)
        station = previous_nodes[station]
    path.insert(0, station)

    return path, distances[end]

# Encontrar la mejor ruta
def find_best_route(start, end, minimize_transfers=False):
    if minimize_transfers:
        # Penalizar transbordos manteniendo los tiempos de viaje reales
        graph_with_penalized_transfers = {}

        for station, neighbors in metro_map.items():
            graph_with_penalized_transfers[station] = {}
            for neighbor, time in neighbors.items():
                # Si ambas estaciones contienen 'linea', evaluar penalización de transbordo
                if "linea" in station and "linea" in neighbor:
                    # Si el transbordo ocurre entre líneas diferentes, añadir penalización
                    if station.split(" linea ")[1] != neighbor.split(" linea ")[1]:
                        graph_with_penalized_transfers[station][neighbor] = time + 10  # Penalización de 10 min
                    else:
                        # Sin transbordo, usar el tiempo real
                        graph_with_penalized_transfers[station][neighbor] = time
                else:
                    # Si no hay 'linea', mantener el tiempo real
                    graph_with_penalized_transfers[station][neighbor] = time

        return dijkstra(graph_with_penalized_transfers, start, end)
    else:
        # Encontrar la ruta más rápida basada en los tiempos reales
        return dijkstra(metro_map, start, end)




# Validar estaciones
def valid_station(station):
    return station in metro_map

# Solicitar input al usuario con validación
def get_valid_station(prompt):
    while True:
        station = input(prompt).strip()
        if valid_station(station):
            return station
        else:
            print("Estación no válida. Por favor ingrese una estación existente.")

# Función para obtener una hora válida
def get_valid_time(prompt):
    while True:
        time_str = input(prompt)
        try:
            # Convertir la entrada a un objeto datetime con formato de 24 horas
            return datetime.strptime(time_str, "%H:%M")
        except ValueError:
            print("Formato inválido. Por favor ingrese la hora en formato HH:MM (24 horas).")
