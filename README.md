# Street Smart Backend [![Build Status](https://travis-ci.org/chadlagore/simple_servant.svg?branch=master)](https://travis-ci.org/chadlagore/simple_servant)

A backend and API for the Street**Smart** app.

`https://tranquil-shore-92989.herokuapp.com`

[![Build Status](https://travis-ci.org/chadlagore/simple_servant.svg?branch=master)](https://travis-ci.org/chadlagore/simple_servant)


## Getting Started

You will require access to the Heroku database to do development.
Get yourself added as a contributor on the Heroku app, collect the
`DATABASE_URL` from the database settings page. Then prior to running the app,
in your terminal:

```
export DATABASE_URL=<insert Heroku DB basic URL here>
```

To install the dependencies, create a virtual environment and activate it:

```bash
conda create --name street_smart python=3.5
source activate street_smart
```

Then,

```bash
pip install -r requirements.txt
python manage.py runserver
```

## Historical Data API

Endpoint: `traffic/historical`

#### Parameters

+ `id` intersection id.
+ `granularity` can be hourly, daily, weekly or monthly.
+ `start_date` unix timestamp.
+ `end_data` unix timestamp.

### Response Payload

For a request like:

`traffic/historical?id=1&granularity=daily&start_date=1490000000&end_date=1490831240`

```
{
    meta: {
        "id": 1,
        "granularity": "daily",
        "start_date": 1490810000,
        "end_data": 1490831240
    },
    data = {
        1490810000: 240,
        1490896400: 325,
        1490982800: 299,
        1491069200: 225,
        1491155600: 279,
        1491242000: 522,
        ...
    }
}
```

In this example, each entry in data represents a day. The unix timestamps
are evenly spaced 24hour intervals from 1490000000 to 1490831240.
