import time
import pandas as pd
from enum import Enum

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ["january", "february", "march", "april", "may", "june", "july", \
            "august", "september", "october", "november", "december"]

DAY_LIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", \
            "sunday"]

Months = Enum("Months", MONTH_LIST)

Days = Enum("Days", DAY_LIST)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = input('City name: ').lower()
    while(city not in ["chicago", "new york city", "washington"]):
        print("Please give a valid city name (chicago, new york city, washington): ", end="")
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Month (type all for all the months):").lower()
    while(month not in [*MONTH_LIST, "all"]):
        print("Please give a valid month (all, january, february, ... , june): ", end="")
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Day of the Week(all, monday, tuesday, ... sunday): ").lower()
    while(day not in ["all", *DAY_LIST]):
        month = input("Please give a valid day of the week ((all, monday, tuesday, ... sunday): ").lower()

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
        data_frame - Pandas DataFrame containing city data filtered by month and day
    """
    data_frame = pd.read_csv(CITY_DATA[city])
    column_name = "Start Time"

    # converting [Start Time] from string to datetime
    data_frame[column_name] = pd.DatetimeIndex(data_frame[column_name])
    
    # filtering month
    if(month != "all"):
        month_num = Months[month].value
        data_frame = data_frame[data_frame[column_name].dt.month == month_num]

    # filtering day
    if(day != 'all'):
        data_frame = data_frame[data_frame[column_name].dt.day_name() == day.capitalize()]

    return data_frame


def time_stats(data_frame):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # most_common_month_num = data_frame["Start Time"].dt.month.value_counts().idxmax()
    try:
        most_common_month_num = data_frame["Start Time"].dt.month.mode().item()
        most_common_month = Months(most_common_month_num).name
    except ValueError:
        most_common_month = "NA"
    
    print("Most Common Month:", most_common_month)

    # display the most common day of week
    # most_common_day = data_frame["Start Time"].dt.day_name().value_counts().idxmax()
    try:
        most_common_day = data_frame["Start Time"].dt.day_name().mode().item()
    except ValueError:
        most_common_day = "NA"
    print("Most Common Day of the Week:", most_common_day)

    # display the most common start hour
    # most_common_hour = data_frame["Start Time"].dt.hour.value_counts().idxmax()
    try:
        most_common_hour = data_frame["Start Time"].dt.hour.mode().item()
    except ValueError:
        most_common_hour = "NA"
    print("Most Common Start Hour:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(data_frame):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_common_start_station = data_frame["Start Station"].apply(lambda x: x.strip()).mode().item()
    except ValueError:
        most_common_start_station = "NA"
    print("Most Commonly Used Start Station:", most_common_start_station)

    # display most commonly used end station
    try:
        most_common_end_station = data_frame["End Station"].apply(lambda x: x.strip()).mode().item()
    except ValueError:
        most_common_end_station = "NA"
    print("Most Commonly Used End Station:", most_common_end_station)

    # display most frequent combination of start station and end station trip

    # Removing NANs
    data_frame = data_frame[data_frame["Start Station"].notna() & data_frame["End Station"].notna()]

    data_frame["Start End Station"] = data_frame["Start Station"] + "**" + data_frame["End Station"]
    try:
        most_common_start_end_combo = data_frame["Start End Station"].mode().item()
    except ValueError:
        most_common_start_end_combo = "NA**"
    print("Most Frequent Combination of Start Station and End Station Trip", most_common_start_end_combo.split("**"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(data_frame):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    data_frame['End Time'] = pd.DatetimeIndex(data_frame['End Time'])
    data_frame['Duration'] = data_frame["End Time"] - data_frame["Start Time"]
    total_travel_time = data_frame['Duration'].sum()
    print("Total Travel Time:", total_travel_time)

    # display mean travel time
    mean_travel_time = data_frame['Duration'].mean()
    print("Mean Travel Time:", mean_travel_time.seconds, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(data_frame):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = data_frame['User Type'].unique()
    print("Count of User Types:", len(user_types))

    try:
        # Display counts of gender
        gender_types = data_frame['Gender'].unique()
        print("Count of Gender Types:", len(gender_types))

        # Display earliest, most recent, and most common year of birth
        earliest_yob = data_frame['Birth Year'].min()
        most_recent_yob = data_frame['Birth Year'].max()
        most_common_yob = data_frame['Birth Year'].mode().item()
        print("Earliest Year of Birth:", int(earliest_yob))
        print("Most Recent Year of Birth:", int(most_recent_yob))
        print("Most Common Year of Birth:", int(most_common_yob))
    except:
        print("Data not found for Gender and Year of Birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    city, month, day = get_filters()
    data_frame = load_data(city, month, day)
    time_stats(data_frame)
    station_stats(data_frame)
    trip_duration_stats(data_frame)
    user_stats(data_frame)

    show_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    row_num = 0
    while(show_data == 'yes' and row_num < len(data_frame)):
        print(data_frame.iloc[row_num: row_num+5])
        row_num += 5
        show_data = input("Do you wish to continue?: ").lower()


if __name__ == "__main__":
	main()
