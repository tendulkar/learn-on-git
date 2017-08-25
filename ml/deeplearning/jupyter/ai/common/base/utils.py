import math


HISTOGRAM_SIZE = 7


def prob_distribution(data):
    data.sort()
    n = data.size // HISTOGRAM_SIZE
    m = data.size % HISTOGRAM_SIZE
    em = HISTOGRAM_SIZE - 1 - m + (m != 0)
    buckets = [data[0]] + [0 for i in range(HISTOGRAM_SIZE - 1)] + [data[-1]]
    bucket_indices = [n * (i + 1) for i in range(em)]
    last_ind = bucket_indices[-1]

    while last_ind + n + 1 < data.size:
        last_ind += n + 1
        bucket_indices.append(last_ind)

    cnt = 0
    for i in bucket_indices:
        cnt += 1
        buckets[cnt] = (data[i - 1] + data[i]) / 2

    return buckets


def display_time_histogram(ax, x, y, color):
    del ax.collections[:]

    lm = HISTOGRAM_SIZE // 2
    rm = HISTOGRAM_SIZE // 2
    for i in range(int(math.ceil(rm))):
        ax.fill_between(x, y[:, lm - i], y[:, rm + 1 + i], facecolor=color, alpha=1.6 / HISTOGRAM_SIZE)
        if i == 0 and HISTOGRAM_SIZE % 2 == 0:
            ax.fill_between(x, y[:, lm - 1], y[:, rm], facecolor=color, alpha=1.6 / HISTOGRAM_SIZE)
            lm = lm - 1
