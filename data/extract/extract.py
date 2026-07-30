import csv
from enum import Enum
import json
import datetime as dt


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
                route_color = row['route_color']
                if route_name == 'S4' or len(route_color) == 0:
                    continue
                routes[route_id] = route_name
                route_colors[route_name] = {
                    'color': route_color,
                    'text_color': row['route_text_color'],
                }
    return routes, route_colors


def get_trips(routes):
    trip_to_route = {}
    trip_to_service_id = {}
    with open('../GTFS/trips.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route_id = row['route_id']
            trip_id = row['trip_id']
            if route_id in routes:
                trip_to_route[trip_id] = routes[route_id]
                trip_to_service_id[trip_id] = row['service_id']
    return trip_to_route, trip_to_service_id


def weekday_count(start_date, end_date):
    week        = {}
    for i in range((end_date - start_date).days):
        day       = (start_date + dt.timedelta(days=i+1)).weekday()
        week[day] = week[day] + 1 if day in week else 1
    for day in range(7):
        if day not in week:
            week[day] = 0
    return week


def get_day_count_in_range(start_date, end_date, days):
    weekday_counts = weekday_count(start_date, end_date)
    return sum(weekday_counts[i] * int(days[i]) for i in range(len(days)))


def convert_date(date_string):
    return dt.datetime.strptime(date_string, '%Y%m%d')
    return dt.date.fromisoformat(f'{date_string[:4]}-{date_string[4:6]}-{date_string[6:]}')


def get_service_days():
    totals = {}
    # calendar = {}
    with open('../GTFS/calendar.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date = row['service_id'], row['monday'], row['tuesday'], row['wednesday'], row['thursday'], row['friday'], row['saturday'], row['sunday'], row['start_date'], row['end_date']
            days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
            count = get_day_count_in_range(convert_date(start_date), convert_date(end_date), days)
            # calendar[service_id] = {
            #     'start_date': convert_date(start_date),
            #     'end_date': convert_date(end_date),
            #     'days': days
            # }
            totals[service_id] = count

    with open('../GTFS/calendar_dates.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_id, exception_type = row["service_id"], row["exception_type"]
            if exception_type == '1':
                totals[service_id] += 1
            elif exception_type == '2':
                totals[service_id] -= 1
    print(totals)
    return totals


def filter_trips(trip_to_service_id):
    service_days = get_service_days()
    filtered = []
    for trip_id, service_id in trip_to_service_id.items():
        if service_days[service_id] > 100: # todo cutoff wählen
            print(trip_id, service_id, service_days[service_id])
            filtered.append(trip_id)
    return filtered


def get_stops_for_trips(trips):
    trip_to_stops = {}
    with open('../GTFS/stop_times.txt', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip_id = row['trip_id']
            if trip_id in trips:
                trip_to_stops.setdefault(trip_id, []).append(row['stop_id'])
    return trip_to_stops


def get_lines_per_stop_id(routes):
    trip_to_route, trip_to_service_id = get_trips(routes)
    relevant_trips = filter_trips(trip_to_service_id)
    trip_to_stops = get_stops_for_trips(trip_to_route.keys())
    stop_to_lines = {}
    for trip_id, line_name in trip_to_route.items():
        if trip_id not in relevant_trips:
            continue
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
            print(stop_name)
            stop_names[stop_id] = stop_name.replace(' (Berlin)', '')
    return stop_names


def get_lines_per_stop_name(routes):
    stop_to_lines = get_lines_per_stop_id(routes)
    stop_translations = get_stop_translations()
    stop_names_to_lines = {}
    for stop_id, stop_lines in stop_to_lines.items():
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