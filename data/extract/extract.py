import csv
from enum import Enum
import json
import datetime as dt


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
        self.stops = set()

    def add_trip(self, trip_id):
        self.trips.add(trip_id)

    def add_stops(self, stops):
        self.stops = self.stops.union(stops)

    def __str__(self):
        return f'{self.name} ({self.color}, {self.text_color}) with stops: {", ".join(self.stops)}'


class Stop:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)


class ServiceStorage:
    def __init__(self):
        self.calendar_service_days, self.start_date, self.end_date = self.get_calendar_service_days()
        self.service_days = self.get_adjusted_service_days(self.calendar_service_days)

    def is_regular_service(self, service_id):
        return self.service_days.get(service_id, 0) > 100
        # return self.calendar_service_days[service_id] <= self.service_days[service_id]

    @staticmethod
    def get_calendar_service_days():
        service_days = {}
        min_date = None
        max_date = None
        with open('../GTFS/calendar.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                service_id = row['service_id']
                monday, tuesday, wednesday, thursday, friday, saturday, sunday = row['monday'], row['tuesday'], row['wednesday'], row['thursday'], row['friday'], row['saturday'], row['sunday']
                start_date, end_date = ServiceStorage.convert_date(row['start_date']), ServiceStorage.convert_date(row['end_date'])
                days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
                min_date = start_date if min_date is None or start_date < min_date else min_date
                max_date = end_date if max_date is None or end_date > max_date else max_date

                count = ServiceStorage.get_day_count_in_range( start_date, end_date, days)
                service_days[service_id] = count
        return service_days, min_date, max_date

    @staticmethod
    def get_adjusted_service_days(service_days):
        with open('../GTFS/calendar_dates.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                service_id, exception_type = row["service_id"], row["exception_type"]
                if exception_type == '1':
                    service_days[service_id] += 1
                elif exception_type == '2':
                    service_days[service_id] -= 1
        return service_days

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


class StopTranslator:
    def __init__(self):
        self.stop_names = {}
        with open('../GTFS/stops.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stop_id = row['stop_id']
                stop_name = row['stop_name']
                self.stop_names[stop_id] = stop_name.replace(' (Berlin)', '')

    def translate(self, stop_id):
        return self.stop_names.get(stop_id)


class LineStorage:
    def __init__(self):
        self.stop_translator = StopTranslator()
        self.lines = LineStorage.read_u_and_s_lines()
        self.add_stops()

    @staticmethod
    def read_u_and_s_lines():
        lines = {}
        with open('../GTFS/routes.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_type = int(row['route_type'])
                route_id = row['route_id']
                if route_type != RouteType.U_BAHN.value and route_type != RouteType.S_BAHN.value:
                    continue
                route_name = row.get('route_short_name', '')
                route_color = row['route_color']
                if len(route_color) == 0:
                    continue
                lines[route_id] = Line(route_id, route_type, route_name, route_color, row['route_text_color'])
        return lines

    def add_stops(self):
        services = ServiceStorage()
        trips = set()
        with open('../GTFS/trips.txt', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                route_id = row['route_id']
                if route_id in self.lines:
                    trip_id = row['trip_id']
                    service_id = row['service_id']
                    if services.is_regular_service(service_id):
                        self.lines[route_id].add_trip(trip_id)
                        trips.add(trip_id)
        stop_storage = StopStorage(trips)
        for _, line in self.lines.items():
            for trip_id in line.trips:
                line.add_stops([self.stop_translator.translate(stop_id) for stop_id in stop_storage.get_stops(trip_id)])

    def get_lines_per_stop(self):
        stops = {}
        for line in self.lines.values():
            for stop in line.stops:
                stops.setdefault(stop, set()).add(line.name)
        for stop, line_names in stops.items():
            stops[stop] = sorted(list(line_names))
        return stops

    def get_all_line_colors(self):
        colors = {}
        for line in self.lines.values():
            colors[line.name] = {
                'color': line.color,
                'text_color': line.text_color
            }
        return colors

#1055
#1056
#1078
#976
#978
def main():
    line_storage = LineStorage()
    for line in line_storage.lines.values():
        if line.name == 'S41':
            print(line)
    with open('data.json', 'w') as file:
        stop = line_storage.get_lines_per_stop()
        json.dump({
            'lines': line_storage.get_all_line_colors(),
            'stops': stop
        }, file, indent=2, sort_keys=True, ensure_ascii=False)

main()

# todo: GTFS Daten runterladen
# todo: encoding in data.json