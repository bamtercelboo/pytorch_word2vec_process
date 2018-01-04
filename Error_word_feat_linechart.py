# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np


def line_chart(subword, subwordp, list_sample_k):
    print("line chart......")
    # plt.plot(list_sample_k, subword)
    plt.plot(list_sample_k, subword, label='subword line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=6)
    plt.plot(list_sample_k, subwordp, label='subwordp line', linewidth=3, color='b', marker='.',
             markerfacecolor='red', markersize=12)
    plt.xlabel("sample k")
    plt.ylabel("error_avg(e5)")
    plt.legend()
    plt.show()


def curve_graph(subword, subwordp, list_sample_k):
    print("line chart......")
    # plt.plot(list_sample_k, subword)
    plt.plot(list_sample_k, subword, label='subword line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=6)
    plt.plot(list_sample_k, subwordp, label='subwordp line', linewidth=3, color='b', marker='.',
             markerfacecolor='red', markersize=12)
    plt.xlabel("sample k")
    plt.ylabel("error_avg\t(e5)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    list_sample_k = [100, 500, 1000, 5000, 10000]
    subword = [1, 2, 3, 4, 5]
    result_subword = np.array([144190.621523, 716169.415991, 1434454.60236, 7161599.71824, 14326143.0018]) / 1e5
    result_subwordp = np.array([42247.319816, 211896.464883, 421972.310551, 2113090.17853, 4228295.00981]) / 1e5
    line_chart(result_subword, result_subwordp, list_sample_k)

