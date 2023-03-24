import argparse

def create_flight_time_bars(itinerary_file):
    print(itinerary_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("itinerary_file")
    args = parser.parse_args()
    create_flight_time_bars(args.itinerary_file)