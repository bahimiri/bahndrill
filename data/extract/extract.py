import csv
from enum import Enum
import json


class RouteType(Enum):
    U_BAHN = 400
    S_BAHN = 109

routes = {}
with open('../GTFS/routes.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_type = int(row['route_type'])
        route_name = row.get('route_short_name', '')
        route_id = row['route_id']
        route_color = row['route_color']
        route_text_color = row['route_text_color']
        if route_type == RouteType.U_BAHN.value or route_type == RouteType.S_BAHN.value:
            routes[route_id] = {
                'name': route_name,
                'color': route_color,
                'text_color': route_text_color,
            }

# lines = sorted([routes[route_id] for route_id in routes])
# print(lines)
# print(routes)

route_to_trip = {}
with open('../GTFS/trips.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_id = row['route_id']
        trip_id = row['trip_id']
        if route_id in routes and route_id not in route_to_trip:
            route_to_trip[route_id] = row['trip_id']
# print(route_to_trip)

trip_to_stops = {}
with open('../GTFS/stop_times.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        trip_id = row['trip_id']
        if trip_id in set(route_to_trip.values()):
            trip_to_stops.setdefault(trip_id, []).append(row['stop_id'])

stop_to_lines = {}
for route_id, trip_id in route_to_trip.items():
    line_name = routes[route_id]['name']
    for stop_id in trip_to_stops.get(trip_id, []):
        stop_to_lines.setdefault(stop_id, set()).add(line_name)

# print(stop_to_lines)
#
# result = []
stop_names_to_lines = {}
with open('../GTFS/stops.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stop_id = row['stop_id']
        if stop_id in stop_to_lines:
            stop_names_to_lines.setdefault(row['stop_name'], set()).update(stop_to_lines[stop_id])
            # result.append({
            #     'name': row['stop_name'],
            #     'lines': sorted(stop_to_lines[stop_id])
            # })


# for stop in result:
#     print(f"{stop['name']}: {' ,'.join(stop['lines'])}")
for name, lines in stop_names_to_lines.items():
    print(f"{name}: {', '.join(lines)}")


# Writing JSON to a file
stop_names_to_lines_final = {}
for name, lines in stop_names_to_lines.items():
    stop_names_to_lines_final[name] = list(lines)
data = {
    'routes': routes,
    'stops': stop_names_to_lines_final
}
with open('data.json', 'w') as file:
    json.dump(data, file, indent=2)

# todo: anzahl aller stops ausgeben lassen und verifizieren
# todo: GTFS Daten runterladen