import datetime
import time

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
