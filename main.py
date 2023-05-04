import math
import numpy as np
import matplotlib.pyplot as plt


def min_max():
    mini, maxi = data[0], data[0]
    for elem in data[1:]:
        if elem < mini:
            mini = elem
        if elem > maxi:
            maxi = elem
    return mini, maxi


def histogram(step_func, err=1):
    d = data.copy()
    d.sort()
    err10 = err * 10
    h = step_func(err)
    xi1 = minimum
    xi = round(math.floor(minimum * err10) / err10 + h, err)
    bar = list()
    xs = list()
    widths = list()
    i = 0
    while i < n:
        count = 0
        flag = True
        while xi1 <= d[i] < xi:
            flag = False
            count += 1
            i += 1
            if i >= n:
                xi = maximum
                break
        if flag:
            i += 1
            continue
        bar.append(count / n / (xi - xi1))
        xs.append((xi + xi1) / 2)
        widths.append(xi - xi1)
        xi1 = xi
        xi = round(xi + h, err)
    fig, ax = plt.subplots()
    ax.bar(xs, bar, edgecolor="black", linewidth=1, width=widths)
    ax.plot(xs, bar, color="red")
    ax.scatter(xs, bar, color="red")
    ax.grid(which='major', color='gray', linestyle=':')
    plt.xlim(minimum, maximum)
    plt.show()


def step(err):
    return round((maximum - minimum) / (1 + math.floor(math.log2(n))), err)


def step2(err):
    return round((maximum - minimum) / (1 + math.floor(3.322 * math.log(n))), err)


def empirical():
    def func(x):
        s = 0
        for elem in data:
            if elem < x:
                s += 1
        return s / n

    xs = np.arange(minimum, maximum, 0.01)
    y = list(map(func, xs))
    fig, ax = plt.subplots()
    ax.plot(xs, y)
    ax.grid(which='major', color='gray', linestyle=':')
    plt.xlim(minimum, maximum)
    plt.show()


if __name__ == "__main__":
    with open("2.txt", "r") as file:
        data = list(map(float, file.read().split()))
    n = len(data)
    minimum, maximum = min_max()
    histogram(step2, 3)
    empirical()
