import requests
import json
from datetime import date, timedelta


def load_all_competitions(file_name):
    with open(file_name, 'r') as f:
        j = json.load(f)
    return j


def save_all_competitions(j):
    with open('competitions.json', 'w+') as f:
        json.dump(j, f, indent=2)
    return


def check_cancelled(d, c):
    # the cancelled_at field is fixed to 2020-07-03 in all competition before this date.
    # So we have to manually fix these competitions
    # https://www.worldcubeassociation.org/posts/cancellation-of-wca-asian-championship-2020
    # no competition was announced

    # https://www.worldcubeassociation.org/posts/cancellation-of-wca-european-championship-2020
    if d['short_name'] == "WCA Euro 2020":
        c['stop'] = '2020-04-03'
        return c

    # https://www.worldcubeassociation.org/posts/cancellation-of-wca-north-american-championship-2020
    elif d['short_name'] == 'WCA NA Championship 2020':
        c['stop'] = '2020-06-25'
        return c

    end = date.fromisoformat(c['end'])   # start of the competition

    # https://www.worldcubeassociation.org/posts/covid-19-situation-update-2020-03-19
    if date(2020, 3, 19) <= end <= date(2020, 4, 19):
        c['stop'] = '2020-03-19'

    # https://www.worldcubeassociation.org/posts/covid-19-situation-update-2020-03-30
    elif date(2020, 4, 20) <= end <= date(2020, 6, 1):
        c['stop'] = '2020-03-31'

    # for competitions who cancelled themselfs
    elif end <= date(2020, 7, 3):
        c['stop'] = end.isoformat()

    else:
        c['stop'] = c['stop'].split("T")[0]

    return c


def parse_data(d):
    c = dict()
    c['start'] = d['announced_at'].split("T")[0]
    c['end'] = d['start_date']

    c['stop'] = d['cancelled_at']
    if c['stop'] is not None:
        # c['stop'] = c['stop'].split("T")[0]
        c = check_cancelled(d, c)

    c['lat'] = d['latitude_degrees']
    c['lon'] = d['longitude_degrees']
    return c


def get_all_competitions(link, initial_date):
    all_competitions = []
    page = 1
    print("Getting WCA API")
    while True:
        print('\tpage: ', page)
        # https://www.worldcubeassociation.org/api/v0/competitions?sort=announced_at&start=2019-03-13
        url = "%s?sort=announced_at&start=%s&page=%s" % (link, initial_date, page)
        r = requests.get(url)
        if r.status_code >= 400:
            raise Exception("HTMLCode%s" % r.status_code)
        data = r.json()
        if len(data) == 0:
            break
        for d in data:
            all_competitions.append(parse_data(d))

        page += 1

    print("Found %d competitions" % len(all_competitions))
    return all_competitions


def update_competitions(initial_date):
    all_comps = get_all_competitions('https://www.worldcubeassociation.org/api/v0/competitions', initial_date)
    save_all_competitions(all_comps)
    return all_comps
