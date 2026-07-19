import csv

routes = {}
with open('../GTFS/routes.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        route_type = int(row['route_type'])
        route_name = row.get('route_short_name', '')
        if route_type == 400:
            routes[row['route_id']] = route_name
        elif route_type == 109 and route_name.startswith('S'):
            routes[row['route_id']] = route_name

# lines = sorted([routes[route_id] for route_id in routes])
# print(lines)

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

result = []
with open('../GTFS/stops.txt', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stop_id = row['stop_id']
        if stop_id in stop_to_lines:
            result.append({
                'name': row['stop_name'],
                'lines': sorted(stop_to_lines[stop_id])
            })


for stop in result:
    print(f"{stop['name']}: {' ,'.join(stop['lines'])}")