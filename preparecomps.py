import datetime

FULLSIZE = 400
DAYSPLUS = 10
# INITIAL_DATE = datetime.date(2019, 9, 4)


def get_competitions_by_day(all_competitions, initial_date):
    ret = dict()
    day_current = datetime.date.fromisoformat(initial_date)
    # starting from the start and going until today
    while day_current != datetime.date.today():
        competitions_current = []

        for c in all_competitions:
            # valid competition only if it is announced and it is not yet cancelled/started
            start = datetime.date.fromisoformat(c['start'])
            end = datetime.date.fromisoformat(c['end'])
            stop = datetime.date.fromisoformat(c['stop']) if c['stop'] is not None else None

            check = convert_competition(start, end, stop, day_current)
            if check is None:
                continue

            competitions_current.append({'lat': c['lat'], 'lon': c['lon'],
                                         'size': check[0], 'color': check[1],
                                         })

        ret[day_current.isoformat()] = competitions_current
        day_current += datetime.timedelta(days=1)  # will loop through the days until today

    return ret


def convert_competition(start, end, stop, current):
    if stop is not None and stop < end:
        if stop <= current <= stop + datetime.timedelta(days=DAYSPLUS):
            return FULLSIZE, 'red'
        if start <= current < stop:
            return get_value(current - start, end - start), 'green'
        return None

    if end <= current <= end + datetime.timedelta(days=DAYSPLUS):
        return FULLSIZE, 'blue'
    if start <= current < end:
        return get_value(current - start, end - start), 'green'
    return None


def get_value(top, bottom):
    return top.days/bottom.days * FULLSIZE
