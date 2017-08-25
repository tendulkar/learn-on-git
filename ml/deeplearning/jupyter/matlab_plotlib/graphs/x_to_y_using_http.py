"""
It's more focused on getting the data from http using numpy and urllib, rather than any matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import urllib
import matplotlib.dates as mdates


def rotate_labels(angle=90):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(angle)
    ax1.grid(True)
    return ax1


def bytesupdate2num(fmt, encoding="utf-8"):
    strconverter = mdates.strpdate2num(fmt)


    def bytesconverter(b):
        s = b.decode(encoding)
        res = strconverter(s)
        # print("fmt: {}, s; {}, res: {}".format(fmt, s, res))
        return res


    return bytesconverter


stock_url = "https://pythonprogramming.net/yahoo_finance_replacement"
stock_info = urllib.request.urlopen(stock_url).read().decode().split("\n")[1:]

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
print("stock_data size: {}".format(len(stock_info)))

ax1 = rotate_labels(45)
ax1.plot_date(dt, openp, "-", label="open price", color="blue")
# plt.plot_date(dt, adjclose, "-", label="close price", color="red")
# plt.plot_date(dt, lowp, "-", label="low price", color="magenta")
# plt.plot_date(dt, highp, "-", label="high price", color="black")
plt.legend(loc="upper left")
plt.subplots_adjust(left=0.09, bottom=0.2, right=0.94, top=0.9, wspace=0.2, hspace=0)
plt.show()
