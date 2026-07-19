import csv
from enum import Enum
import json


class RouteType(Enum):
    U_BAHN = 400
    S_BAHN = 109

routes = {}
route_colors = {}
with open('../GTFS/routes.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_type = int(row['route_type'])
        route_name = row.get('route_short_name', '')
        route_id = row['route_id']
        route_color = row['route_color']
        route_text_color = row['route_text_color']
        if route_type == RouteType.U_BAHN.value or route_type == RouteType.S_BAHN.value:
            if route_name == 'S4':
                continue
            routes[route_id] = route_name
            route_colors[route_name] = {
                'color': route_color,
                'text_color': route_text_color,
            }

route_to_trip = {}
with open('../GTFS/trips.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_id = row['route_id']
        trip_id = row['trip_id']
        if route_id in routes and route_id not in route_to_trip:
            route_to_trip[route_id] = row['trip_id']

trip_to_stops = {}
with open('../GTFS/stop_times.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        trip_id = row['trip_id']
        if trip_id in set(route_to_trip.values()):
            trip_to_stops.setdefault(trip_id, []).append(row['stop_id'])

stop_to_lines = {}
for route_id, trip_id in route_to_trip.items():
    line_name = routes[route_id]
    for stop_id in trip_to_stops.get(trip_id, []):
        stop_to_lines.setdefault(stop_id, set()).add(line_name)

stop_names_to_lines = {}
with open('../GTFS/stops.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stop_id = row['stop_id']
        if stop_id in stop_to_lines:
            stop_name = row['stop_name'].replace(' (Berlin)', '')
            stop_names_to_lines.setdefault(stop_name, set()).update(stop_to_lines[stop_id])


stop_names_to_lines_final = {}
for name, lines in stop_names_to_lines.items():
    stop_names_to_lines_final[name] = list(lines)

with open('data.json', 'w') as file:
    json.dump({
        'lines': route_colors,
        'stops': stop_names_to_lines_final
    }, file, indent=2)

# todo: anzahl aller stops ausgeben lassen und verifizieren
# todo: GTFS Daten runterladen