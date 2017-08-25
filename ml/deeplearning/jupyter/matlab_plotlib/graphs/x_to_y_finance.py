import numpy as np
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import urllib


# bars are nothing but graphs with filling area
def bytesupdate2num(fmt, encoding="utf-8"):
    strconverter = mdates.strpdate2num(fmt)


    def bytesconverter(b):
        s = b.decode(encoding)
        res = strconverter(s)
        # print("fmt: {}, s; {}, res: {}".format(fmt, s, res))
        return res


    return bytesconverter


stock_url = "https://pythonprogramming.net/yahoo_finance_replacement"
stock_info = urllib.request.urlopen(stock_url).read().decode().split("\n")[1:11]

# check legibility of data by hand, to control too many values to unpack
# for x in stock_info:
#     if len(x.split(",")) != 7:
#         print("malformed data: {}".format(x))

dt, openp, highp, lowp, closep, adjclose, volume = np.loadtxt(stock_info,
                                                              delimiter=",",
                                                              unpack=True,
                                                              converters={
                                                                  0: bytesupdate2num("%Y-%m-%d")
                                                              })
stock_data = [(dt[i], openp[i], highp[i], lowp[i], closep[i]) for i in range(len(dt))]
ax1 = plt.subplot2grid((1, 1), (0, 0))
candlestick_ohlc(ax1, stock_data, colorup="cyan", colordown="red")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.scatter(dt, openp, 40, color="black")
ax1.scatter(dt, closep, 40, color="blue")

for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(90)
for s in stock_info:
    print("stock: {}".format(s))
print("stock_data size: {}".format(len(stock_info)))
plt.legend()

plt.show()
