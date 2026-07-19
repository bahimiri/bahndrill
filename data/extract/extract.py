import csv
from enum import Enum
import json


class RouteType(Enum):
    U_BAHN = 400
    S_BAHN = 109


def get_line_information():
    routes = {}
    route_colors = {}
    with open('../GTFS/routes.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route_type = int(row['route_type'])
            route_id = row['route_id']
            if route_type == RouteType.U_BAHN.value or route_type == RouteType.S_BAHN.value:
                route_name = row.get('route_short_name', '')
                if route_name != 'S42':
                    continue
                routes[route_id] = route_name
                route_colors[route_name] = {
                    'color': row['route_color'],
                    'text_color': row['route_text_color'],
                }
    return routes, route_colors


def get_exceptional_service_ids():
    excluded_ids = set()
    ones = 0
    twos = 0
    with open('../GTFS/calendar_dates.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['exception_type'] == '2':
                ones += 1
                excluded_ids.add(row['service_id'])
            else:
                twos += 1
    print(ones, twos)
    return excluded_ids


def get_regular_service_ids():
    regular_ids = set()
    with open('../GTFS/calendar.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            monday = int(row['monday'])
            tuesday = int(row['tuesday'])
            wednesday = int(row['wednesday'])
            thursday = int(row['thursday'])
            friday = int(row['friday'])
            if sum([monday, tuesday, wednesday, thursday, friday]) >= 5:
                regular_ids.add(row['service_id'])
    return regular_ids


def get_trips(routes):
    exceptional_services = get_exceptional_service_ids()
    regular_services = get_regular_service_ids()
    trip_to_route = {}
    with open('../GTFS/trips.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route_id = row['route_id']
            trip_id = row['trip_id']
            if route_id in routes and route_id not in trip_to_route:
                service_id = row['service_id']
                # print(service_id)
                # if service_id not in exceptional_services and service_id in regular_services:
                # if service_id not in exceptional_services:
                if service_id in regular_services:
                    trip_to_route[trip_id] = routes[route_id]
    return trip_to_route


def get_stops_for_trips(trips):
    trip_to_stops = {}
    with open('../GTFS/stop_times.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_id = row['trip_id']
            if trip_id in trips:
                # if row['stop_id'] == 'de:11000:900193002:1:50':
                #     print('trip_id',trip_id)
                trip_to_stops.setdefault(trip_id, []).append(row['stop_id'])
    return trip_to_stops


def get_lines_per_stop_id(routes):
    trip_to_route = get_trips(routes)
    trip_to_stops = get_stops_for_trips(trip_to_route.keys())
    stop_to_lines = {}
    for trip_id, line_name in trip_to_route.items():
        for stop_id in trip_to_stops.get(trip_id, []):
            stop_to_lines.setdefault(stop_id, set()).add(line_name)
    return stop_to_lines


def get_stop_translations():
    stop_names = {}
    with open('../GTFS/stops.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop_id = row['stop_id']
            stop_name = row['stop_name']
            stop_names[stop_id] = stop_name.replace(' (Berlin)', '')
    return stop_names


def get_lines_per_stop_name(routes):
    stop_to_lines = get_lines_per_stop_id(routes)
    stop_translations = get_stop_translations()
    stop_names_to_lines = {}
    for stop_id, stop_lines in stop_to_lines.items():
        # if stop_translations[stop_id] == 'S Adlershof':
        #     print(stop_id)
        stop_names_to_lines.setdefault(stop_translations[stop_id], set()).update(stop_lines)

    for name, line_names in stop_names_to_lines.items():
        stop_names_to_lines[name] = sorted(list(line_names))
    return stop_names_to_lines


lines, line_colors = get_line_information()
lines_per_stop = get_lines_per_stop_name(lines)

with open('data.json', 'w') as file:
    json.dump({
        'lines': line_colors,
        'stops': lines_per_stop
    }, file, indent=2, sort_keys=True)

# todo: GTFS Daten runterladen
# todo pathways, z.b. u wilmersdorfer str <-> s charlottenburg