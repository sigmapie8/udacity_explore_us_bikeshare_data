import time
import pandas as pd
import numpy as np
from enum import Enum
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

DAY_LIST = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    column_name = "Start Time"

    # converting [Start Time] from string to datetime
    df[column_name] = pd.DatetimeIndex(df[column_name])
    
    # filtering month
    if(month != "all"):
        month_num = Months[month].value
        df = df[df[column_name].dt.month == month_num]

    # filtering day
    if(day != 'all'):
        df = df[df[column_name].dt.day_name() == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # most_common_month_num = df["Start Time"].dt.month.value_counts().idxmax()
    try:
        most_common_month_num = df["Start Time"].dt.month.mode().item()
        most_common_month = Months(most_common_month_num).name
    except ValueError:
        most_common_month = "NA"
    
    print("Most Common Month:", most_common_month)

    # display the most common day of week
    # most_common_day = df["Start Time"].dt.day_name().value_counts().idxmax()
    try:
        most_common_day = df["Start Time"].dt.day_name().mode().item()
    except ValueError:
        most_common_day = "NA"
    print("Most Common Day of the Week:", most_common_day)

    # display the most common start hour
    # most_common_hour = df["Start Time"].dt.hour.value_counts().idxmax()
    try:
        most_common_hour = df["Start Time"].dt.hour.mode().item()
    except ValueError:
        most_common_hour = "NA"
    print("Most Common Start Hour:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    try:
        most_common_start_station = df["Start Station"].apply(lambda x: x.strip()).mode().item()
    except ValueError:
        most_common_start_station = "NA"
    print("Most Commonly Used Start Station:", most_common_start_station)

    # display most commonly used end station
    try:
        most_common_end_station = df["End Station"].apply(lambda x: x.strip()).mode().item()
    except ValueError:
        most_common_end_station = "NA"
    print("Most Commonly Used End Station:", most_common_end_station)

    # display most frequent combination of start station and end station trip

    # Removing NANs
    df = df[df["Start Station"].notna() & df["End Station"].notna()]

    df["Start End Station"] = df["Start Station"] + "**" + df["End Station"]
    try:
        most_common_start_end_combo = df["Start End Station"].mode().item()
    except ValueError:
        most_common_start_end_combo = "NA**"
    print("Most Frequent Combination of Start Station and End Station Trip", most_common_start_end_combo.split("**"))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.DatetimeIndex(df['End Time'])
    df['Duration'] = df["End Time"] - df["Start Time"]
    total_travel_time = df['Duration'].sum()
    print("Total Travel Time:", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Duration'].mean()
    print("Mean Travel Time:", mean_travel_time.seconds, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].unique()
    print("Count of User Types:", len(user_types))

    try:
        # Display counts of gender
        gender_types = df['Gender'].unique()
        print("Count of Gender Types:", len(gender_types))

        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode().item()
        print("Earliest Year of Birth:", int(earliest_yob))
        print("Most Recent Year of Birth:", int(most_recent_yob))
        print("Most Common Year of Birth:", int(most_common_yob))
    except:
        print("Data not found for Gender and Year of Birth")

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
