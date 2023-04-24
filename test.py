from bikeshare_2 import MONTH_LIST, DAY_LIST, load_data, time_stats, station_stats, trip_duration_stats, user_stats

for city in ["chicago", "new york city", "washington"]:
    for month in [*MONTH_LIST, "all"]:
        for day in ["all", *DAY_LIST]:
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)