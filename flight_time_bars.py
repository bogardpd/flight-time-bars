"""Creates a time bar visualization for multiple travelers' flights."""
import argparse
import xml.etree.ElementTree as ET
from datetime import timezone
from dateutil.parser import parse
from tabulate import tabulate

class Traveler:
    """A person traveling on a trip."""
    def __init__(self, traveler_elem) -> None:
        """Generates a Traveler from a traveler XML element."""
        self.name = traveler_elem.find('name').text
        self.flights = [Flight(elem) for elem in traveler_elem.iter('flight')]


class Flight:
    """An individual flight segment taken by a Traveler."""
    def __init__(self, flight_elem) -> None:
        """Generates a Flight from a flight XML element."""
        orig = flight_elem.find('origin')
        dest = flight_elem.find('destination')
        self.direction = flight_elem.attrib['direction']
        self.identifier = flight_elem.find('identifier').text
        self.orig_iata = orig.attrib['iata']
        self.orig_sched = parse(orig.attrib['scheduled_departure'])
        self.dest_iata = dest.attrib['iata']
        self.dest_sched = parse(dest.attrib['scheduled_arrival'])


def create_flight_time_bars(itinerary_file):
    tree = ET.parse(itinerary_file)
    itinerary = tree.getroot()
    travelers = [Traveler(elem) for elem in itinerary.iter('traveler')]
    for traveler in travelers:
        print(traveler.name)
        flight_table = [[
            flight.direction,
            flight.identifier,
            flight.orig_iata,
            flight.orig_sched,
            # flight.orig_sched.astimezone(timezone.utc),
            flight.dest_iata,
            flight.dest_sched,
            # flight.dest_sched.astimezone(timezone.utc),
        ] for flight in traveler.flights]
        print(tabulate(flight_table))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("itinerary_file")
    args = parser.parse_args()
    create_flight_time_bars(args.itinerary_file)