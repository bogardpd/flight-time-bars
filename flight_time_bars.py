import argparse
import xml.etree.ElementTree as ET

def create_flight_time_bars(itinerary_file):
    tree = ET.parse(itinerary_file)
    root = tree.getroot()
    for traveler in root.iter('traveler'):
        print(traveler.find('name').text)
        for flight in traveler.iter('flight'):
            print("\t", flight.attrib['direction'], flight.find('identifier').text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("itinerary_file")
    args = parser.parse_args()
    create_flight_time_bars(args.itinerary_file)