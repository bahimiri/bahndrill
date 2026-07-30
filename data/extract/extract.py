import csv
from enum import Enum
import json
import datetime as dt
from typing import Dict


class RouteType(Enum):
    U_BAHN = 400
    S_BAHN = 109


class Line:
    def __init__(self, line_id, line_type, name, color, text_color):
        self.id = line_id
        self.type = line_type
        self.name = name
        self.color = color
        self.text_color = text_color
        self.trips = set()

    def add_trip(self, trip_id):
        self.trips.add(trip_id)

    def __str__(self):
        return f'{self.name} ({self.color}, {self.text_color})'


class Stop:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)


class ServiceStorage:
    def __init__(self):
        self.service_days = {}
        with open('../GTFS/calendar.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date = row['service_id'], row['monday'], row['tuesday'], row['wednesday'], row['thursday'], row['friday'], row['saturday'], row['sunday'], row['start_date'], row['end_date']
                days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
                count = ServiceStorage.get_day_count_in_range(
                    ServiceStorage.convert_date(start_date),
                    ServiceStorage.convert_date(end_date),
                    days)
                self.service_days[service_id] = count

        with open('../GTFS/calendar_dates.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                service_id, exception_type = row["service_id"], row["exception_type"]
                if exception_type == '1':
                    self.service_days[service_id] += 1
                elif exception_type == '2':
                    self.service_days[service_id] -= 1

    @staticmethod
    def weekday_count(start_date, end_date):
        week = {}
        for i in range((end_date - start_date).days + 1):
            day = (start_date + dt.timedelta(days=i)).weekday()
            week[day] = week[day] + 1 if day in week else 1
        for day in range(7):
            if day not in week:
                week[day] = 0
        return week

    @staticmethod
    def get_day_count_in_range(start_date, end_date, days):
        weekday_counts = ServiceStorage.weekday_count(start_date, end_date)
        return sum(weekday_counts[i] * int(days[i]) for i in range(len(days)))

    @staticmethod
    def convert_date(date_string):
        return dt.datetime.strptime(date_string, '%Y%m%d')


class StopStorage:
    def __init__(self, trips):
        self.stops = {}
        with open('../GTFS/stop_times.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trip_id = row['trip_id']
                if trip_id in trips:
                    self.stops.setdefault(trip_id, []).append(row['stop_id'])

    def get_stops(self, trip_id):
        return self.stops.get(trip_id, [])


class LineStorage:
    def __init__(self):
        self.lines = {}
        with open('../GTFS/routes.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_type = int(row['route_type'])
                route_id = row['route_id']
                if route_type != RouteType.U_BAHN.value and route_type != RouteType.S_BAHN.value:
                    continue
                route_name = row.get('route_short_name', '')
                route_color = row['route_color']
                if route_name == 'S4' or len(route_color) == 0: # todo braucht man s4 check noch?
                    continue
                self.lines[route_id] = Line(route_id, route_type, route_name, route_color, row['route_text_color'])

    def add_trips(self):
        services = ServiceStorage()
        with open('../GTFS/trips.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_id = row['route_id']
                if route_id in self.lines:
                    trip_id = row['trip_id']
                    service_id = row['service_id']
                    if services.service_days[service_id] > 100:
                        self.lines[route_id].add_trip(trip_id)


# for route_id, line in lines.items():
#     print(route_id, line)
# print(len(lines))








#
#
# def get_lines_per_stop_id(routes):
#     trip_to_route, trip_to_service_id = get_trips(routes)
#     relevant_trips = filter_trips(trip_to_service_id)
#     trip_to_stops = get_stops_for_trips(trip_to_route.keys())
#     stop_to_lines = {}
#     for trip_id, line_name in trip_to_route.items():
#         if trip_id not in relevant_trips:
#             continue
#         for stop_id in trip_to_stops.get(trip_id, []):
#             stop_to_lines.setdefault(stop_id, set()).add(line_name)
#     return stop_to_lines
#
#
# def get_stop_translations():
#     stop_names = {}
#     with open('../GTFS/stops.txt', 'r') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             stop_id = row['stop_id']
#             stop_name = row['stop_name']
#             stop_names[stop_id] = stop_name.replace(' (Berlin)', '')
#     return stop_names
#
#
# def get_lines_per_stop_name(routes):
#     stop_to_lines = get_lines_per_stop_id(routes)
#     stop_translations = get_stop_translations()
#     stop_names_to_lines = {}
#     for stop_id, stop_lines in stop_to_lines.items():
#         stop_names_to_lines.setdefault(stop_translations[stop_id], set()).update(stop_lines)
#
#     for name, line_names in stop_names_to_lines.items():
#         stop_names_to_lines[name] = sorted(list(line_names))
#     return stop_names_to_lines
#
#
# lines, line_colors = get_line_information()
# lines_per_stop = get_lines_per_stop_name(lines)
#
# with open('data.json', 'w') as file:
#     json.dump({
#         'lines': line_colors,
#         'stops': lines_per_stop
#     }, file, indent=2, sort_keys=True)

def main():
    lines = LineStorage()
    lines.add_trips()

main()

# todo: GTFS Daten runterladen
# todo: encoding in data.json