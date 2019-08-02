import time
import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november' 'december']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # DONE: Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input('Which city would you like to analyze?: ')).lower()
    while city not in CITY_DATA:
        print("That's not a city we can analyze.  Please choose chicago, washington, or new york city.")
        print()
        city = str(input('Which city would you like to analyze?: ')).lower()

    # DONE: Get user input for month (all, january, february, ... , june)
    month = str(input("Which month would you like to filter by?  Type 'all' for no filter.: ")).lower()

    while month != 'all' and month not in months:
         print("That's not a month we recognize.  Please type the full name of a month you would like to analyze, or type 'all' for all months. /n")
         print()
         month = str(input("Which month would you like to filter by?  Type 'all' for no filter.: ")).lower()

    # DONE: Get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("Which day of the week would you like to filter by? Type 'all' for no filter.: ")).lower()

    while day != 'all' and day not in days:
         print("That's not a day of the week we recognize.  Please type the full name of a day you would like to analyze, or type 'all' for all days.")
         print()
         day = str(input("Which day of the week would you like to filter by? Type 'all' for no filter.: ")).lower()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # And start hour in its own column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # DONE: Display the most common month
    num_month = df['month'].mode()[0]
    popular_month = months[num_month - 1]
    print("The most popular month of travel is", popular_month.title())

    # DONE: Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most popular day of travel is", popular_day)

    # DONE: Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour of travel is", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # DONE: Display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most popular start station is", popular_start)

    # DONE: Display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most popular end station is", popular_end)

    # DONE: Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = str(df['Trip'].mode()).strip("0   ")
    print("The most popular trip is from", popular_trip)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # DONE: Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time for all trips during your selected timeframe is", time.strftime('%H hours, %M minutes, and %S seconds', time.gmtime(total_travel_time)),"or", total_travel_time, "seconds total")

    # DONE: Display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print("The mean travel time for all trips during your selected timeframe is", time.strftime('%M minutes, and %S seconds', time.gmtime(travel_mean)), "or", travel_mean, "seconds total")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # DONE: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Users by Type:")
    print(user_types)

    # DONE: Display counts of gender
    print("\nUsers by Gender:")
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print("We do not have gender information for users in Washington.")

    # DONE: Display earliest, most recent, and most common year of birth
    print("\nUser Birth Year Information:")
    try:
        birth_year_old = df['Birth Year'].min()
        birth_year_young = df['Birth Year'].max()
        birth_year_pop = df['Birth Year'].mode()
        print("The user with the earliest date of birth is", int(birth_year_old))
        print("The user with the most recent date of birth is", int(birth_year_young))
        print("The most common year of birth for the users is", int(birth_year_pop))
    except KeyError:
        print("We do not have birth year information for users in Washington.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Displaying lines of data for the user
        show_lines = input('\nWould you like to view the first 5 lines of data? Enter yes or no.\n')

        # Setting up the variable for the .head function
        line_start = 5

        if show_lines.lower() == 'yes':
            print(df.head())

            # Add 5 to number of lines being displayed
            line_start += 5
            show_more_lines = input('\nWould you like to view additional lines of data? Enter yes or no.\n')

            while show_more_lines.lower() == 'yes':
               print(df.head(line_start))
               line_start += 5
               show_more_lines = input('\nWould you like to view additional lines of data? Enter yes or no.\n')

        # Placed this section in the else area for data loop
        else:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break


if __name__ == "__main__":
	main()
