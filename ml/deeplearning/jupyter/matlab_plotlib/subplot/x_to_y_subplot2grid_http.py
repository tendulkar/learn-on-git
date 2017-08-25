import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.style as style
from matplotlib.finance import candlestick_ohlc
import urllib


style.use("bmh")
MA1 = 20
MA2 = 30


def moving_average(values, window):
    weights = np.repeat(1.0 / (window * 1.0), window)
    res = np.convolve(values, weights, "valid")
    return res


def bytesupdate2num(fmt, encoding="utf-8"):
    strconverter = mdates.strpdate2num(fmt)


    def bytesconverter(b):
        s = b.decode(encoding)
        res = strconverter(s)
        # print("fmt: {}, s; {}, res: {}".format(fmt, s, res))
        return res


    return bytesconverter


stock_url = "https://pythonprogramming.net/yahoo_finance_replacement"
stock_info = urllib.request.urlopen(stock_url).read().decode().split("\n")[1:101]

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
print("dt size: {}".format(len(stock_info)))

fig = plt.figure(facecolor="white")
ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=1, colspan=1)
plt.ylabel("H-L")
ax2 = plt.subplot2grid((6, 1), (1, 0), rowspan=4, colspan=1, sharex=ax1)
plt.ylabel("Price")
ax2v = ax2.twinx()
ax3 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax2)
plt.ylabel("MAvgs")

ma1 = moving_average(closep, MA1)
ma2 = moving_average(closep, MA2)
start = len(dt[max(MA1, MA2) - 1:])

print("len(ma1): {}, len(ma2): {}, len(dt): {}, start: {}".format(len(ma1), len(ma2), len(dt), start))
print("len(ma1[-start:]): {}, len(ma2[-start:]): {}, len(dt[-start:]): {}, -start: {}"
      .format(len(ma1[-start:]), len(ma2[-start:]), len(dt[-start:]), -start))

stock_data = [(dt[i], openp[i], highp[i], lowp[i], closep[i]) for i in range(len(dt))]
candlestick_ohlc(ax2, stock_data[-start:], colorup="cyan", colordown="red")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax2.xaxis.set_major_locator(mticker.MaxNLocator(10))

# plot volumes on ax2v
# ax2v is creating using twinx()
# twinx is nothing but use same 'x' axis and grid layout, but uses different 'y' axis on right side
ax2v.fill_between(dt[-start:], 0, volume[-start:], label="volume", facecolor="cyan", alpha=0.4)
ax2v.yaxis.set_ticklabels([])
ax2v.grid(False)
ax2v.set_ylim(0, 3 * volume.max())
ax2v.legend().get_frame().set_alpha(.2)


# plot moving averages
ax3.plot(dt[-start:], ma1[-start:], label="fast average", linewidth=1)
ax3.plot(dt[-start:], ma2[-start:], label="slow average", linewidth=1)
ax3.fill_between(dt[-start:], ma1[-start:], ma2[-start:], where=(ma1[-start:] > ma2[-start:]), facecolor="cyan", edgecolor="cyan")
ax3.fill_between(dt[-start:], ma1[-start:], ma2[-start:], where=(ma1[-start:] < ma2[-start:]), facecolor="red", edgecolor="red")
ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax3.legend(loc="lower right", ncol=2).get_frame().set_alpha(0.1)

# plot difference b/n highs and lows
ax1.plot_date(dt[-start:], highp[-start:] - lowp[-start:], fmt="-", label="variation")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax1.legend(loc="upper right").get_frame().set_alpha(0.4)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
for label in ax3.xaxis.get_ticklabels():
    label.set_rotation(45)
plt.show()
fig.savefig('stock_data', facecolor=fig.get_facecolor())

