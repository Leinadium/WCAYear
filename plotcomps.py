import matplotlib.pyplot as plt
import cartopy.crs as ccrs


COLORS = {'red': '#ff2020', 'blue': '#2020ff', 'green': '#20ff20'}
TITLE = "World Map view of WCA Competitions"
SUBTITLE = "github.com/Leinadium/WCAYear"


def generate_maps(day_comps, ax=None):
    # plt.rcParams['figure.constrained_layout.use'] = True
    fig = plt.figure(figsize=(19.2, 10.8))
    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0, min_latitude=-65, max_latitude=70))
    plt.rcParams['font.family'] = 'monospace'

    i = 0
    for i, day in enumerate(day_comps):
        print("Creating map of day", day, end='')
        ax = generate_map(day, day_comps[day], ax)
        fig.tight_layout()
        fig.savefig('frames/frame%04d.png' % i, facecolor='white', dpi=fig.dpi)
        ax.clear()
        print(" = Done (%d)" % i)
        # input()

    print("Finished creating %d maps" % (i + 1))
    return


def generate_map(day, comps, ax=None):
    if ax is None:
        fig = plt.figure(figsize=(19.2, 10.8))
        ax = plt.axes(projection=ccrs.Mercator(central_longitude=0, min_latitude=-65, max_latitude=70))

    ax.coastlines()
    ax.set_extent([-180, 180, -70, 70], crs=ccrs.PlateCarree())

    lats = []
    lons = []
    sizes = []
    colors = []
    for a in comps:
        lats.append(a['lat'])
        lons.append(a['lon'])
        sizes.append(a['size'])
        colors.append(COLORS[a['color']])

    ax.scatter(lons, lats, s=sizes, c=colors, alpha=0.9, edgecolor='#000000',
               transform=ccrs.PlateCarree())

    ax = add_texts(day, len(comps), ax)

    # plt.show()
    # input()
    return ax


def add_texts(day, i, ax):
    # date
    ax.text(-175, -61,
            day, color='#000000',
            fontsize=15+5, transform=ccrs.PlateCarree(), alpha=0.9)

    # total competitions
    ax.text(-175, -64, 'competition count: %d' % i,
            color='#000000', fontsize=12+5, transform=ccrs.PlateCarree(), alpha=0.9)

    # signature
    # ax.text(-175, -59.5, SIGNATURE, color='#000000', fontsize=10,
    #         transform=ccrs.PlateCarree(), horizontalalignment='left', alpha=0.8)

    # subtitle
    ax.text(170, -64, SUBTITLE, color='#000000', fontsize=7+5,
            transform=ccrs.PlateCarree(), horizontalalignment='right', alpha=0.8)

    # title
    ax.text(170, -60, TITLE, color='#000000', fontsize=20+5,
            transform=ccrs.PlateCarree(), horizontalalignment='right', alpha=0.9)

    # description
    ax.text(-175, -10, 'competition announced', color=COLORS['green'], fontsize=12+5,
            transform=ccrs.PlateCarree(), horizontalalignment='left', alpha=0.8)
    ax.text(-175, -18, 'competition happening', color=COLORS['blue'], fontsize=12+5,
            transform=ccrs.PlateCarree(), horizontalalignment='left', alpha=0.8)
    ax.text(-175, -26, 'competition cancelled', color=COLORS['red'], fontsize=12+5,
            transform=ccrs.PlateCarree(), horizontalalignment='left', alpha=0.8)

    return ax
