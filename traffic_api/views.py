import datetime
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from traffic_api.models import *
from .carsim.get_cars import get_cars

granularities = [
    'hourly',
    'daily',
    'weekly',
    'monthly',
    'yearly'
]

time_integer_failure_msg = 'Time paramters must be integer POSIX timestamps.'
time_missing_failure_msg = 'Time paramters must specified.'
bad_granularity_msg = 'Granularity must be: ' + ', '.join(granularities)
id_not_integer_msg = 'Intersection id must be an integer.'
unimplemented_msg = 'Unimplemented feature: '

num_mock_intersections = 6


@csrf_exempt
def receive_data(request):
    if request.method == 'GET':
        return render(request, 'index.html', {'data': TrafficData.objects.all()})
    else:
        dataPackage = TrafficData()

        dataPackage.dataString = request.body
        pairs = request.body.decode().split('&')

        dataPackage.carCount = pairs[0].split('=')[1]
        dataPackage.latitude = pairs[1].split('=')[1]
        dataPackage.longitude = pairs[3].split('=')[1]
        timeStr = pairs[2].split('=')[1]

        hours = int(timeStr[0:2])
        minutes = int(timeStr[2:4])
        seconds = int(timeStr[4:6])

        time = datetime.time(hour=hours, minute=minutes, second=seconds)
        date = datetime.date.today()

        dataPackage.timestamp = datetime.datetime.combine(date, time)

        dataPackage.save()

        return HttpResponse(status=200)

@csrf_exempt
def all_intersection_activity(request):

    lat_lte = request.GET.get('lat_lte', '')
    lat_gte = request.GET.get('lat_gte', '')
    lon_gte = request.GET.get('lon_gte', '')
    lon_lte = request.GET.get('lon_lte', '')

    intersection_id = request.GET.get('id', '')

    # Check if we have coordinates.
    if lat_lte and lat_gte and lon_gte and lon_lte:
        filtered = IntersectionData.objects.filter(
            latitude__gte=lat_gte,
            latitude__lte=lat_lte,
            longitude__gte=lon_gte,
            longitude__lte=lon_lte)
    elif intersection_id:
        filtered = IntersectionData.objects.filter(
            id=intersection_id
        )
    else:
        filtered = IntersectionData.objects.all()

    # Convert all objects to dict.
    results = [ob.as_json() for ob in filtered]

    # Append car observations.
    hour = int(time.strftime("%H"))

    for result in results:
        result['cars'] = get_cars(hour)

    return JsonResponse(results, safe=False)


@csrf_exempt
def historical_request(request):
    '''
    Responds to a request for historical data.

    '''

    intersection_id = request.GET.get('id', None)
    granularity = request.GET.get('granularity', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    if granularity == 'weekly':
        return HttpResponseBadRequest(unimplemented_msg + 'weekly')

    # Times stamps must exist and be integers.
    try:
        start_date_ts = int(start_date)
        end_date_ts = int(end_date)

    except ValueError:
        return HttpResponseBadRequest(time_stamp_failure_msg)

    except TypeError:
        return HttpResponseBadRequest(time_missing_failure_msg)

    # Granularity must be one of the granularities.
    if granularity not in granularities:
        return HttpResponseBadRequest(bad_granularity_msg)

    # Id must be an integer.
    try:
        mock_id = int(intersection_id) % num_mock_intersections

    except TypeError:
        return HttpResponseBadRequest(id_not_integer_msg)

    except ValueError:
        return HttpResponseBadRequest(id_not_integer_msg)

    # Now we can filter.
    filtered = HistoricalData.objects.filter(
        intersection=intersection_id,
        timestamp__gte=start_date_ts,
        timestamp__lte=end_date_ts,
    )

    # Get filtered results from database and add mocked intersection id.
    results = [ob.as_json(intersection_id) for ob in filtered]

    response = {
        'meta': {
            'id': intersection_id,
            'granularity': granularity,
            'start_date': start_date,
            'end_date': end_date,
            'results': len(results)
        }, 'data': {}
    }

    # Truncate (floor) the date, and aggregate the response.
    for result in results:
        result['cars'] = result['cars'] * 60 # This is a dirty hack for now.
        result['timestamp'] = floor_date(result['timestamp'], granularity)

        # Add a new record at this timetamp.
        response['data'][result['timestamp']] = 0

    # Aggregate results into the response dict (simple sum).
    for result in results:
        stored = response['data'][result['timestamp']]
        response['data'][result['timestamp']] = stored + result['cars']

    # Only need to aggregate over timestamps if not hourly request.
    return JsonResponse(response, safe=False)


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

    return time.mktime(dt_floor.timetuple()) + 8*3600
