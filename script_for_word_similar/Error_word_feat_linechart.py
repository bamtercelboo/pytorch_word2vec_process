# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np


def line_chart(subword, subwordp, list_sample_k):
    print("line chart......")
    ax = plt.figure()
    # plt.plot(list_sample_k, subword)
    plt.plot(list_sample_k, subword, label='subword line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=6)
    plt.plot(list_sample_k, subwordp, label='subwordp line', linewidth=3, color='b', marker='.',
             markerfacecolor='red', markersize=12)

    # mark data
    datadotxy_subwordp = tuple(zip(list_sample_k, subwordp))
    for index, dotxy in enumerate(datadotxy_subwordp):
        if index >= 2:
            plt.annotate((int(dotxy[0]), int(dotxy[1])), xy=dotxy)

    datadotxy_subword = tuple(zip(list_sample_k, subword))
    for index, dotxy in enumerate(datadotxy_subword):
        if index >= 2:
            plt.annotate((int(dotxy[0]), int(dotxy[1])), xy=dotxy)

    plt.xlabel("sample k")
    plt.ylabel("error_avg  (e5)")
    plt.title("subword compare to subwordp")
    # plt.p
    plt.legend()
    plt.show()
    ax.savefig("./Error.jpg")


if __name__ == "__main__":
    list_sample_k = [100, 500, 1000, 5000, 10000]
    result_subword = np.array([144190.621523, 716169.415991, 1434454.60236, 7161599.71824, 14326143.0018]) / 1e5
    result_subwordp = np.array([42247.319816, 211896.464883, 421972.310551, 2113090.17853, 4228295.00981]) / 1e5
    # line_chart(result_subword, result_subwordp, list_sample_k)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    result_subword_1 = np.array([143319.390711, 716121.69137, 1434830.03841, 4295752.4993, 7158406.87341, 11451680.9352, 14313336.4919]) / 1e5
    result_subwordp_1 = np.array([42482.822056, 211515.23559, 422875.380547, 1267350.48972, 2113341.01494, 3380381.35501, 4224598.85861]) / 1e5
    line_chart(result_subword_1, result_subwordp_1, list_sample_k)

