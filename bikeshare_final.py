import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    """
    Asks user for city input

    """
    while True:
        city = input ("Enter the name of the city you want information about: chicago, new york city or washington: \n").lower()
        cities = ('chicago','new york city','washington')
        if city in cities:
            return city
            break
        else:
            print ("You didn't enter a valid city, please try again")


def get_month():
    """
    Asks user for month input

    """
    while True:
        month = input("Would you like to filter by month or see data on all months? Type in one of following: january, februari, march, april, may, june or all: \n").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june','all']
        if month not in months:
            print("You didn't enter a valid month, please try again")
        else:
            return month
        break


def get_day():
    """
    Asks user for day input

    """
    while True:
        day = input("would you like to filter by day or see data for all days? Input one of the following: monday, tuesday, wednesday, thurseday, friday, saturday, sunday or all: \n" ).lower()
        days = ['all','monday','tuesday', 'wednesday','thurseday','friday','saturday','sunday']
        if day not in days:
            print("You didn't enter a valid day, please try again")
        else:
            return day
        break



filter_city = get_city()
filter_month = get_month()
filter_day = get_day()



def load_data(filter_city, filter_month, filter_day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df=pd.read_csv(CITY_DATA[filter_city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if filter_month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(filter_month) + 1
        df = df[df['month'] == month]
        if filter_day != 'all':
            df = df[df['day_of_week'] == filter_day.title()]
    return df

filtered_data = load_data(filter_city,filter_month,filter_day)


def time_stats(filtered_data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month= filtered_data['month'].max()
    popular_day= filtered_data['day_of_week'].max()

    print( "\n The most common month is", popular_month)
    print( "\n The most common day of the week is", popular_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

time_stats(filtered_data)

def station_stats(filtered_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station= filtered_data['Start Station'].max()
    popular_ending_station= filtered_data['End Station'].max()
    filtered_data['Combination_of_stations']= filtered_data['Start Station'].astype(str) + ' AND ' + filtered_data['End Station'].astype(str)
    popular_combination_of_stations= filtered_data['Combination_of_stations'].max()

    print( "\n The most common starting station is", popular_start_station)
    print( "\n The most common ending station is", popular_ending_station)
    print( "\n The most common combination of starting and ending sations is", popular_combination_of_stations)

station_stats(filtered_data)

def trip_duration_stats(filtered_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time= filtered_data['Trip Duration'].sum()
    to_hours= total_travel_time / 360
    print('Total travel time [in hours] is', to_hours)

    total_travel_time= filtered_data['Trip Duration'].mean()
    to_mean_hours= total_travel_time / 360
    print('Mean travel time [in hours] is', to_mean_hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

trip_duration_stats(filtered_data)

def user_stats(filtered_data):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_count= filtered_data.groupby(['User Type'])['User Type'].count()
    print('The count per user type is as follows \n ', user_type_count)

    if filter_city =='chicago' or filter_city == 'new york city':
        user_gender_count= filtered_data.groupby(['Gender'])['Gender'].count()
        print('The count per gender is as follows \n ', user_gender_count)
    else:
        print('Sorry, there is no gender data for washington')


    if filter_city =='chicago' or filter_city == 'new york city':
        user_birthdate_max= filtered_data['Birth Year'].max()
        user_birthdate_min= filtered_data['Birth Year'].min()
        user_birthdate_common= filtered_data['Birth Year'].mode()
        print('The youngest birthdate is as follows \n ', user_birthdate_min)
        print('The oldest birthdate is as follows \n ', user_birthdate_max)
        print('The most common birthdate is as follows \n ', user_birthdate_common)
    else:
        print('Sorry, there is no Birth date data for washington')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


user_stats(filtered_data)

def show_raw_data(filtered_data):
    """Asks user input to display raw data"""
    index = 0
    while True:
        lines = input("would you like to see raw data? Answer with yes or no \n")
        if lines == 'yes':
            index += 5
            print(filtered_data.head(index))
            print(index)
        else:
            break

show_raw_data(filtered_data)

def main():
    """Asks user if they would like to restart"""
    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart == 'yes':
        filtered_data = load_data(filter_city,filter_month,filter_day)
        time_stats(filtered_data)
        station_stats(filtered_data)
        trip_duration_stats(filtered_data)
        user_stats(filtered_data)
        show_raw_data(filtered_data)
        main()
    else:
        print("thank you for playing")



if __name__ == "__main__":
	main()
