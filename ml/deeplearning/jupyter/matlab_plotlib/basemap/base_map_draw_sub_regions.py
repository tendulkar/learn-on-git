from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection="mill",
            llcrnrlat=6.0,
            llcrnrlon=68,
            urcrnrlat=36,
            urcrnrlon=100,
            resolution="l")

m.drawcoastlines()
m.drawcountries(linewidth=2)
m.drawstates()
# m.etopo()
# m.bluemarble()

plt.show()