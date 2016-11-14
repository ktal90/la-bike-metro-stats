from fake_useragent import UserAgent
import requests
import getpass
import datetime


START_DATE = datetime.date(2016, 8, 1)

AUTH_URL = 'https://bikeshare.metro.net/wp-content/themes/indego/api/authenticate/'
TRIP_HISTORY_URL = 'https://bikeshare.metro.net/wp-content/themes/indego/api/authenticate/history/'

def get_trips_for_month(month, session): 
    body = {'type':'trips',
            'month':month,
            'year':2016}
    r = session.post(TRIP_HISTORY_URL, json=body, headers=headers)
    return r.json()['data']

def do_auth(session):
    body = {'userlogin': raw_input('Username: '),
            'password': getpass.getpass()}
    r = session.post(AUTH_URL,
                     headers=headers,
                     data=body)
    return r.json()['result'] == 'Login Successful!'

def get_dates_since_start():
    today = datetime.date.today()
    months = []
    curr_date = today
    while curr_date >= START_DATE:
        months.append(curr_date)
        curr_date = curr_date - datetime.timedelta(days=365/12)
    return months


if __name__ == '__main__':
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    s = requests.Session()

    months = get_dates_since_start()
    if not do_auth(s):
        raise Exception('Login failed!')
    else:
        print 'Successful auth!'

    total_dist_miles = 0
    total_time_mins = 0
    for date in months:
        trips = get_trips_for_month(date.month, s)
        month_dist_miles = sum([trip['miles'] for trip in trips.itervalues()])
        month_time_mins = sum([trip['duration'] for trip in trips.itervalues()])
        print 'Total distance traveled in {month}/{year}: {dist} miles'.format(month=date.strftime('%B'),
                                                                               year=date.year,
                                                                               dist=month_dist_miles)
        print 'Total time traveled in {month}/{year}: {h} hours {m} minutes'.format(month=date.strftime('%B'),
                                                                                    year=date.year,
                                                                                    h=month_time_mins / 60,
                                                                                    m=month_time_mins % 60)
        total_dist_miles += month_dist_miles
        total_time_mins += month_time_mins

    print 'Total distance traveled: {} miles'.format(total_dist_miles)
    print 'Total time traveled: {h} hours {m} minutes'.format(h=total_time_mins / 60, m=int(total_time_mins % 60))