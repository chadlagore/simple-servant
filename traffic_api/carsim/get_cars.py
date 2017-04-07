import datetime
import random
import time


intervals = {
    'midnight': 0,
    'morning': 8,
    'afternoon': 12,
    'evening': 18,
    'late': 24
}

rates = {
    'midnight': 2,
    'morning': 8,
    'afternoon': 4,
    'evening': 7,
    'late': 2
}

sig = 1.5

def get_cars(hour_of_day):
    mu = get_params(hour_of_day)

    # Get rid of negative values.
    return max(random.gauss(mu, sig), 0)


def get_params(hour):
    '''
    Returns the parameters given hour of day.
    Uses formula m = (y2 - y1) / (x2 - x1)
    '''
    if hour < 8:
        # Fit first line.
        x1 = intervals['midnight']
        x2 = intervals['morning']
        y1 = rates['midnight']
        y2 = rates['morning']

    elif hour <= 12:
        x1 = intervals['morning']
        x2 = intervals['afternoon']
        y1 = rates['morning']
        y2 = rates['afternoon']

    elif hour <= 18:
        x1 = intervals['afternoon']
        x2 = intervals['evening']
        y1 = rates['afternoon']
        y2 = rates['evening']

    elif hour < 24:
        x1 = intervals['evening']
        x2 = intervals['late']
        y1 = rates['evening']
        y2 = rates['late']

    else:
        return 5

    m = (y2 - y1) / (x2 - x1)
    yint = y1 - m * x1
    return m * hour + yint


# Maping of granularity to step size.
gran = {
    'hourly': 60,
    'daily': 60*24*1,  # 1 day
    'weekly': 60*24*7,  # 7 days.
    'monthly': 60*24*30, # 30 days.
    'yearly': 60*24*365   # 365 days.
}


def mock_traffic(start_date, end_date, granularity, id):
    '''
    Strategy:
        0. Set seed == id.
        1. Start from start_date.
        2. Increment by granularity until past end_date.
        3. For each step i, calculate get_cars() for each hour in granularity.
        4. Sum results for each i, add result to response.
    '''

    # Weight the trendline.
    trend_wt = 0.0008

    # We seed with the id, nice hack to make intersections look the same.
    random.seed(id)
    aggregate = {}

    # Generate a trendline.
    start_dt = datetime.datetime.fromtimestamp(start_date)
    end_dt = datetime.datetime.fromtimestamp(end_date)

    # y values.
    g = gran[granularity]
    start_reading = get_cars(start_dt.hour) * g
    end_reading = get_cars(end_dt.hour) * g

    # Slope and trendline.
    slope = (start_reading - end_reading) / (start_date - end_date)
    intercept = start_reading - slope * start_date
    trendline = lambda x: slope * x + intercept + random.gauss(0, g)

    # Aggregate by granularity.
    for ts in range(start_date, end_date, g):
        aggregate[ts] = 0
        hour_of_day = datetime.datetime.fromtimestamp(ts).hour

        # Get positie reading.
        reading = get_cars(hour_of_day) * g
        while reading == 0:
            reading = get_cars(hour_of_day) * g

        # Adjust reading by weighted trendline
        adjusted = (g * trend_wt * trendline(ts) + (1 - trend_wt) * reading) / 2
        aggregate[ts] = aggregate[ts] + adjusted

    return aggregate
