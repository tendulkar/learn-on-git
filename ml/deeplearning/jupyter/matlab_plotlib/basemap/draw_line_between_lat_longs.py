from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection="mill",
            llcrnrlat=6,
            llcrnrlon=68,
            urcrnrlat=36,
            urcrnrlon=90,
            resolution="l")

m.drawcoastlines()
m.drawcountries()

xs, ys = [], []
blrLat, blrLon = 12.91, 77.66
xpt, ypt = m(blrLon, blrLat)
xs.append(xpt)
ys.append(ypt)
m.plot(xpt, ypt, 'c^', markersize=16)

delLat, delLon = 28.55, 87.55
xpt, ypt = m(delLon, delLat)
xs.append(xpt)
ys.append(ypt)
m.plot(xpt, ypt, 'r*', markersize=16)

m.plot(xs, ys, color="blue", linewidth=3, label="6E-455")
m.drawgreatcircle(blrLon, blrLat, delLon, delLat, color="red", linewidth=3, label="draw arc")

plt.legend()
plt.show()