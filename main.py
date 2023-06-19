import math
import numpy as np
import matplotlib.pyplot as plt

FILE_NAME = "2.txt"
ERR = 3


def normal_dist(x, mean, sd):
    return np.exp(-0.5*((x-mean)/sd)**2) / sd / math.sqrt(2 * math.pi)


def histogram():
    fig, ax = plt.subplots()
    ax.bar(xs_bar, bar, edgecolor="black", linewidth=1, width=widths_bar, label="Гистограмма")
    ax.plot(xs_bar, bar, color="red", label="Полигон")
    x = np.linspace(minimum, maximum, 1000)
    ys = list()
    for j in range(len(x)):
        ys.append(normal_dist(x[j], 0.985, 0.13))
    ax.plot(x, ys, color="green")
    ax.scatter(xs_bar, bar, color="red")
    ax.grid(which='major', color='gray', linestyle=':')
    plt.xlim(minimum, maximum)
    plt.title("Сгрупированный ряд", fontsize=14)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("f", fontsize=14)
    plt.legend()
    plt.savefig("histogram.png")
    plt.show()


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
    plt.title("Эмпирическая функция распределения", fontsize=14)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("F", fontsize=14)
    plt.savefig("empirical_function.png")
    plt.show()


def series_moments(e=9):
    summ = 0
    summ2 = 0
    summ3 = 0
    summ4 = 0
    print(f"Математическое ожидание: {m}")
    for ind in range(n):
        temp = data[ind] - m
        summ += temp
        summ2 += temp ** 2
        summ3 += temp ** 3
        summ4 += temp ** 4
    print(summ2)
    d = summ2 / n
    print(f"Центральный момент 1-го порядка: {round(summ / n, e)}")
    print(f"Центральный момент 2-го порядка: {round(d, e)}")
    print(f"Центральный момент 3-го порядка: {round(summ3 / n, e)}")
    print(f"Вторая оценка: {round(summ2 / (n - 1), e)}")
    return summ2 / (n - 1)


def pirson():
    xi_ni_sum = 0
    xi2_ni_sum = 0
    for j in range(len(xs_bar)):
        xi_ni_sum += xs_bar[j] * ws[j]
        xi2_ni_sum += xs_bar[j] ** 2 * ws[j]
    sum_w = np.sum(ws)
    mean = xi_ni_sum / sum_w
    dispersion = xi2_ni_sum / sum_w - mean ** 2
    standard_deviation = math.sqrt(dispersion)
    summ = 0
    for j in range(len(xs_bar)):
        z = (xs_bar[j] - mean) / standard_deviation
        f = normal_dist(z, 0, 1)
        freq = sum_w * f * h / standard_deviation
        summ += (ws[j] - freq) ** 2 / freq
    return summ


if __name__ == "__main__":
    with open(FILE_NAME, "r") as file:
        data = list(map(float, file.read().split()))
    n = len(data)
    data.sort()

    minimum, maximum = data[0], data[n - 1]
    m = np.sum(data) / n

    err10 = ERR * 10
    h = round((maximum - minimum) / (1 + math.floor(3.322 * math.log(n))), ERR)
    xi1 = minimum
    xi = round(math.floor(minimum * err10) / err10 + h, ERR)

    bar = list()
    xs_bar = list()
    widths_bar = list()
    ws = list()
    intervals = list()

    i = 0
    while i < n:
        count = 0
        flag = True
        while xi1 <= data[i] < xi:
            flag = False
            count += 1
            i += 1
            if i >= n:
                xi = maximum
                break
        if flag:
            i += 1
            continue

        width = xi - xi1
        bar.append(count / n / width)
        xs_bar.append((xi + xi1) / 2)
        widths_bar.append(width)
        ws.append(count)
        intervals.append(xi1)
        if i >= n:
            intervals.append(xi)

        xi1 = xi
        xi = round(xi + h, ERR)

    disp = series_moments()
    histogram()
    empirical()

    print(disp)
    print(pirson())
