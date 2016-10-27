from fake_useragent import UserAgent
import requests
import getpass

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


if __name__ == '__main__':
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    s = requests.Session()

    if not do_auth(s):
        raise Exception('Login failed!')
    else:
        print 'Successful auth!'
    
    months = {'August': 8,
              'September': 9,
              'October': 10}
    total_dist_miles = 0
    total_time_mins = 0
    for month_name, month_num in months.iteritems():
        trips = get_trips_for_month(month_num, s)
        month_dist_miles = sum([trip['miles'] for trip in trips.itervalues()])
        month_time_mins = sum([trip['duration'] for trip in trips.itervalues()])
        print 'Total distance traveled in {month}: {dist} miles'.format(month=month_name,
                                                                        dist=month_dist_miles)
        print 'Total time traveled in {month}: {h} hours {m} minutes'.format(month=month_name,
                                                                             h=month_time_mins / 60,
                                                                             m=month_time_mins % 60)
        total_dist_miles += month_dist_miles
        total_time_mins += month_time_mins
    
    print 'Total distance traveled: {} miles'.format(total_dist_miles)
    print 'Total time traveled: {h} hours {m} minutes'.format(h=total_time_mins / 60, m=int(total_time_mins % 60))