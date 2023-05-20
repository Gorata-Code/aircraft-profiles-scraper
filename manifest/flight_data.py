import csv
import sys
import random
import requests
from requests import Response
import manifest.constants as const
from bs4 import BeautifulSoup, ResultSet


def search_query(user_search_query: str) -> None:

    ALL_AIRCRAFT: [str] = const.CIVIL_AIR_TRANSPORT_LIST + const.MILITARY_AIR_TRANSPORT_LIST

    RANDOM_AIRCRAFT: str = ''

    for aircraft in random.choices(ALL_AIRCRAFT):
        RANDOM_AIRCRAFT = aircraft

    if user_search_query == 'A':
        profile_to_search_for = input(f'\nPlease type aircraft name here in full(e.g. {RANDOM_AIRCRAFT}): ').strip(). \
            replace(' ', '_')

        if profile_to_search_for.replace("_", " ") not in ALL_AIRCRAFT:
            print(f'\n\tSorry, we do not have a record of the aircraft name "{profile_to_search_for}".')

        elif profile_to_search_for.replace("_", " ") in ALL_AIRCRAFT:
            single_aircraft_profile(profile_to_search_for)

    elif user_search_query == 'B':
        profile_to_search_for = f'{RANDOM_AIRCRAFT.strip().replace(" ", "_")}'
        print(f'\n\t\tSearching for {profile_to_search_for.replace("_", " ")} aircraft info...')
        single_aircraft_profile(profile_to_search_for)

    elif user_search_query == 'C':
        fetch_entire_aircraft_inventory(ALL_AIRCRAFT)

    else:
        print('\nInvalid input.')


def single_aircraft_profile(aircraft_to_profile):

    print('\n\t\t>>>>>>>>>> And we have lift off >>>>>>>>\n')

    DEPARTURES: Response = requests.get(const.AIRCRAFT_BASE_URL + aircraft_to_profile)
    IN_FLIGHT: BeautifulSoup = BeautifulSoup(DEPARTURES.content, 'lxml')
    ARRIVALS = IN_FLIGHT.find(class_='infobox')

    RECORD_HEADINGS: [str] = []
    RECORD_VALUES: [str] = []

    try:

        FULL_AIRCRAFT_PROFILE: ResultSet = ARRIVALS.find('tbody').find_all('tr')
        FULL_AIRCRAFT_PROFILE: ResultSet = FULL_AIRCRAFT_PROFILE[2:]

        for record_entry in FULL_AIRCRAFT_PROFILE:
            try:
                record_heading = record_entry.find('th').text
                record_value = record_entry.find('td').text

                if 'Type of aircraft' in record_value:
                    record_value = record_value.replace('Type of aircraft', '')

                if 'Produced' in record_heading:
                    record_value = record_value.replace('–', ' - ')

                if 'Primary' in record_heading:
                    record_heading = 'Primary User(s)'

                record_heading = str(record_heading).replace('\n', '')
                record_value = str(record_value).replace('\n', '')
                RECORD_HEADINGS.append(record_heading.upper())
                RECORD_VALUES.append(record_value)
            except AttributeError:
                pass

    except AttributeError:
        print('******************************************************************************')
        print('\tMAYDAY! Information on this aircraft is currently unavailable, sorry.')
        print('******************************************************************************')
        input('\nPress Enter to Exit & Try Again.')
        sys.exit(0)

    write_to_file(f'{aircraft_to_profile.replace("_", " ")} Aircraft Profile.csv', RECORD_HEADINGS, RECORD_VALUES)


def fetch_entire_aircraft_inventory(aircraft_lists: [[str]]):

    print(f'\n\tFetching Aircraft data for all {len(aircraft_lists)} listed aircraft.\n')

    ALL_AIRCRAFT_RECORDS: [[str]] = []

    RECORD_HEADINGS: [str] = ['Aircraft Name', 'Role', 'National origin', 'Manufacturer', 'First flight',
                              'Introduction', ' Retired', 'Status', 'Primary user', 'Produced', 'Number built',
                              'Developed from', 'Variants']

    AIRCRAFT_LOG: int = 1

    for aircraft in aircraft_lists:
        DEPARTURES: Response = requests.get(const.AIRCRAFT_BASE_URL + aircraft)
        IN_FLIGHT: BeautifulSoup = BeautifulSoup(DEPARTURES.content, 'lxml')
        FLIGHT_DATA = IN_FLIGHT.find(class_='infobox')

        SINGLE_AIRCRAFT_DATA: [str] = [f'{aircraft}']  # Preloading the aircraft name at the start of each aircraft
        # record.
        RECORD_VALUE: str = ''

        try:
            FULL_RECORD: ResultSet = FLIGHT_DATA.find('tbody').find_all('tr')
            print(f'\n\t\t\t\t#{AIRCRAFT_LOG}. {aircraft}')
            for current_column_heading in RECORD_HEADINGS[1:]:
                for full_record_entry in FULL_RECORD:

                    if full_record_entry.find('th') and full_record_entry.find('td'):
                        RECORD_HEADER = str(full_record_entry.find('th').text)

                        if RECORD_HEADER.strip() == current_column_heading:
                            RECORD_VALUE = full_record_entry.find('td').text

                            if 'Type of aircraft' in RECORD_VALUE:  # Stripping off unwanted text - probably a typo.
                                RECORD_VALUE = RECORD_VALUE.replace('Type of aircraft', '')

                            if RECORD_HEADER.strip() == 'Produced':
                                RECORD_VALUE = RECORD_VALUE.replace('–', ' - ')
                            break

                        elif RECORD_HEADER.strip() != current_column_heading:
                            if 'Primary' in RECORD_HEADER.strip() and 'Primary' in current_column_heading:
                                RECORD_VALUE = full_record_entry.find('td').text  # Compensating for HTML text errors.
                                break
                            else:
                                RECORD_VALUE = '(N/A)'  # When the particular aircraft has no info matching the column.

                SINGLE_AIRCRAFT_DATA.append(RECORD_VALUE)  # Add current value to the current aircraft's profile.

            print(f'\n\t\t\t{aircraft} added successfully!.')

            AIRCRAFT_LOG += 1

            ALL_AIRCRAFT_RECORDS.append(SINGLE_AIRCRAFT_DATA)  # Add the complete aircraft profile to the profiles list.

        except AttributeError:
            pass

    RECORD_HEADINGS: [str] = [HEADING.upper() for HEADING in RECORD_HEADINGS]

    write_to_file('All Aircraft Profiles.csv', RECORD_HEADINGS, [record for record in ALL_AIRCRAFT_RECORDS], ' ')


def write_to_file(file_name, columns, rows, row_status=None):

    with open(file_name, 'w', newline='', encoding='UTF-8') as info_file:
        csv_writer = csv.writer(info_file)
        csv_writer.writerow(columns)

        try:
            if row_status:
                for row in rows:
                    csv_writer.writerow(row)
            else:
                csv_writer.writerow(rows)

        except UnicodeEncodeError:
            pass

    print('\n\tYour information has been successfully written to a spreadsheet file!\n')
    print('\n\t\t>>>>>>>>>> Thank You For Flying With Us. >>>>>>>>\n')
