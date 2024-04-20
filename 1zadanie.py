#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def add_flight(
    flights: List[Dict[str, Any]],
    destination: str,
    departure_date: int,
    aircraft_type: str,
) -> List[Dict[str, Any]]:

    flights.append(
        {
            "destination": destination,
            "departure_date": departure_date,
            "aircraft_type": aircraft_type,
        }
    )

    return flights


def display_flights(flights: List[Dict[str, Any]]) -> None:

    if flights:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 8
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^8} |".format(
                "No", "Destination", "Departure Date", "Aircraft Type"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>8} |".format(
                    idx,
                    flight.get("destination", ""),
                    flight.get("departure_date", ""),
                    flight.get("aircraft_type", ""),
                )
            )
            print(line)
    else:
        print("List of flights is empty.")


def select_flights(
    flights: List[Dict[str, Any]], date: int
) -> List[Dict[str, Any]]:

    result = []
    for flight in flights:
        if flight.get("departure_date") == date:
            result.append(flight)
    return result


def save_flights(file_path: Path, flights: List[Dict[str, Any]]) -> None:

    with open(file_path, "w", encoding="utf-8") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_path: Path) -> List[Dict[str, Any]]:

    with open(file_path, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None) -> None:
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    parser = argparse.ArgumentParser("flights")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new flight"
    )
    add.add_argument("filename", action="store", help="The data file name")
    add.add_argument(
        "-d",
        "--destination",
        action="store",
        required=True,
        help="Destination of the flight",
    )
    add.add_argument(
        "-dd",
        "--departure_date",
        action="store",
        required=True,
        help="Departure date of the flight",
    )
    add.add_argument(
        "-at",
        "--aircraft_type",
        action="store",
        required=True,
        help="Aircraft type of the flight",
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all flights"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select flights by departure date",
    )
    select.add_argument(
        "-D",
        "--date",
        action="store",
        required=True,
        help="Departure date to select flights",
    )

    args = parser.parse_args(command_line)

    home_dir = Path.home()
    file_path = home_dir / args.filename

    is_dirty = False
    if file_path.exists():
        flights = load_flights(file_path)
    else:
        flights = []

    if args.command == "add":
        flights = add_flight(
            flights, args.destination, args.departure_date, args.aircraft_type
        )
        is_dirty = True

    elif args.command == "display":
        display_flights(flights)

    elif args.command == "select":
        selected = select_flights(flights, args.date)
        display_flights(selected)

    if is_dirty:
        save_flights(file_path, flights)


if __name__ == "__main__":
    main()
