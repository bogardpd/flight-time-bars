import argparse
import xml.etree.ElementTree as ET

class Traveler:
    """A person traveling on a trip."""
    def __init__(self, traveler_elem) -> None:
        """Generates a Traveler from a traveler XML element."""
        self.name = traveler_elem.find('name').text
        self.flights = [{
            'direction': flight.attrib['direction'],
            'identifier': flight.find('identifier').text,
        } for flight in traveler_elem.iter('flight')]

def create_flight_time_bars(itinerary_file):
    tree = ET.parse(itinerary_file)
    itinerary = tree.getroot()
    travelers = [Traveler(elem) for elem in itinerary.iter('traveler')]
    for traveler in travelers:
        print(traveler.name)
        for flight in traveler.flights:
            print("\t", flight['direction'], flight['identifier'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("itinerary_file")
    args = parser.parse_args()
    create_flight_time_bars(args.itinerary_file)