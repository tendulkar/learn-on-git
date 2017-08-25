
def scale_ticks(plt, font_size=16, alpha=.65):
    ax = plt.gca()
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(font_size)
        label.set_bbox(dict(facecolor="white", edgecolor="None", alpha=alpha))