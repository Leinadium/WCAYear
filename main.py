from getcomps import update_competitions, load_all_competitions
from preparecomps import get_competitions_by_day
from plotcomps import generate_maps

from time import time

FILENAME = 'competitions.json'
INITIAL_DATE = '2019-01-01'


def main():
    s = FILENAME if input("U to update, or anything to load: ").upper() != 'U' else ''
    i = time()

    if s == '':
        all_comps = update_competitions(INITIAL_DATE)
    else:
        all_comps = load_all_competitions(s)

    comps_by_day = get_competitions_by_day(all_comps, INITIAL_DATE)

    generate_maps(comps_by_day)

    i = int(time() - i)
    print("Total time: %0dm%2ds" % (i // 60, i % 60))
    return


if __name__ == '__main__':
    main()
