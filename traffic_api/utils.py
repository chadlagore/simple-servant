import datetime
import time

from scipy import stats


def floor_date(ts, granularity):
    '''
    Can pass in one of the granularities, floors the timestamp to the given
    granularity.

    '''

    dt = datetime.datetime.fromtimestamp(ts)

    if granularity == 'yearly':
        dt_floor = dt.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif granularity == 'monthly':
        dt_floor = dt.replace(day=1, hour=0, minute=0, second=0)
    elif granularity == 'daily':
        dt_floor = dt.replace(hour=0, minute=0, second=0)
    else:
        dt_floor = dt

    # Convert back to timestamp.
    return int(time.mktime(dt_floor.timetuple()))


def get_linreg(response):
    '''
    Fit a linear regression model. Put results into dictionary with the
    following keys:

    slope, intercept, r_squared, p_value, std_err, x1, y1, x2, y2

    '''

    # Collect x and y vectors.
    x = list(response.keys())
    y = list(response.values())

    # Fit data.
    fit = stats.linregress(x, y)

    # Results go in dictionary.
    result = {
        'slope': fit[0],
        'intercept': fit[1],
        'r_squared': fit[2]**2,
        'p_value': fit[3],
        'std_err': fit[4]
    }

    # Generate linear equations.
    f_x = lambda x: result['slope'] * x + result['intercept']
    f_y = lambda y: (result['slope'] - result['intercept']) / y

    # Calculate y1, y2, x1, x2.
    x1 = min(x)
    x2 = max(x)
    y1 = response[x1]
    y2 = response[x2]

    # Calculate endpoints of fitted line.
    result['y1'] = f_x(x1)
    result['y2'] = f_x(x2)
    result['x1'] = x1
    result['x2'] = x2

    return result
