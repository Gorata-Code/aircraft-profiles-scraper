from manifest.flight_data import *


def script_summary() -> None:
    print('''
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     \t***------------------------------------------------------------------------***\n
              
        \t"AIRCRAFT-PROFILES-SCRAPER" Version 1.0.0\n
        
        This script will help you collect information on all the Civilian and Military Aircraft ever made,
        sourced from Wikipedia. The information is essentially in the form of profiles including categories
        such as Manufacturer, Country of Origin, Usage, Year Introduced etc. You have the option of searching
        for individual aircraft (either specific or random) and searching for the complete list of all aircraft. 
        The collected aircraft information will then be saved to a CSV file (spreadsheet / excel type of file) 
        within the same directory as this Aircraft Profiles executable file.
        
        Cheers!!!
    ''')


def black_box(search_params) -> None:
    try:
        search_query(search_params)

    except Exception as exp:

        if 'INTERNET' in str(exp):

            print(''''

                            Please make sure you are connected to the internet and Try again.

                            Cheers!

                            ''')

            input('\nPress Enter To Exit.\n')
            sys.exit(1)

        elif 'Timed out receiving message from renderer' or 'cannot determine loading status' in str(exp):
            print(str(exp))
            print('\nPlease try again.')

        elif 'ERR_NAME_NOT_RESOLVED' or 'ERR_CONNECTION_CLOSED' or 'unexpected command response' in str(exp):
            print('\nYour internet connection may have been interrupted.')
            print('Please make sure you\'re still connected to the internet and try again.')

        else:
            print(str(exp))
            print('\nPlease try again.')

        input('\nPress Enter to Exit & Try Again.')
        sys.exit(1)


def main() -> None:
    script_summary()
    search_params = input('\tType "A" to search for a specific aircraft\'s profile by name: \n\tType "B" to search '
                          'for a random aircraft\'s profile: \n\tType "C" to search for all available aircraft '
                          'profiles: ').strip().capitalize()
    black_box(search_params)


if __name__ == '__main__':
    main()
