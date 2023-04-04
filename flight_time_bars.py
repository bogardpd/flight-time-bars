"""Creates a time bar visualization for multiple travelers' flights."""
import argparse
from lxml import etree
from datetime import timezone
from dateutil.parser import parse
from tabulate import tabulate

XML_SCHEMA = 'itinerary.xsd'

class Traveler:
    """A person traveling on a trip."""
    def __init__(self, traveler_elem) -> None:
        """Generates a Traveler from a traveler XML element."""
        self.name = traveler_elem.find('Name').text
        self.flights = [Flight(elem) for elem in traveler_elem.iter('Flight')]


class Flight:
    """An individual flight segment taken by a Traveler."""
    def __init__(self, flight_elem) -> None:
        """Generates a Flight from a flight XML element."""
        self.direction = flight_elem.attrib['direction']

        ident = flight_elem.find('Identifier')
        self.identifier = (
            str(ident.attrib['iata']), str(ident.attrib['number']),
        )

        codeshare_elems = [e for e in flight_elem.iter('Codeshare')]
        self.codeshares = [
            (str(cse.attrib['iata']), str(cse.attrib['number']))
            for cse in codeshare_elems
        ]
        
        orig = flight_elem.find('Origin')
        self.orig_iata = orig.attrib['iata']
        self.orig_sched = parse(orig.attrib['departure'])
        
        dest = flight_elem.find('Destination')
        self.dest_iata = dest.attrib['iata']
        self.dest_sched = parse(dest.attrib['arrival'])


def create_flight_time_bars(itinerary_file):
    tree = etree.parse(itinerary_file)
    etree.XMLSchema(etree.parse(XML_SCHEMA)).assertValid(tree)

    itinerary = tree.getroot()
    travelers = [Traveler(elem) for elem in itinerary.iter('Traveler')]
    for traveler in travelers:
        print(traveler.name)
        flight_table = [[
            flight.direction,
            flight.identifier,
            flight.codeshares,
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
    parser.add_argument('itinerary_file')
    args = parser.parse_args()
    create_flight_time_bars(args.itinerary_file)