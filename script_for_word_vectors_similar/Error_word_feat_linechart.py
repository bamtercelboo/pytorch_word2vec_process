# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np


def line_chart(subword, subwordp, list_sample_k):
    print("line chart......")
    ax = plt.figure()
    plt.plot(list_sample_k, subword, label='subword line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=6)
    plt.plot(list_sample_k, subwordp, label='parallel line', linewidth=3, color='b', marker='.',
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
    plt.ylabel("error_avg  (e3)")
    plt.title("subword compare to parallel")
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
    # line_chart(result_subword_1, result_subwordp_1, list_sample_k)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    result_suda_subword = np.array([32129.741336, 159902.812013, 320304.528431, 961862.493594, 1602531.804909, 2564679.817743, 3205338.644382]) / 1e5
    result_suda_parallel = np.array([19038.387846, 95299.619365, 190441.612338, 571882.432056, 953147.436573, 1523103.390247, 1904668.266237]) / 1e5
    # line_chart(result_suda_subword, result_suda_parallel, list_sample_k)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    result_suda_subword0113 = np.array([648.123963, 3260.556078, 6518.512892, 19543.624102, 32589.178882, 52126.385028, 65153.879922]) / 1e3
    result_suda_parallel0113 = np.array([407.091772, 2040.240418, 4073.736341, 12204.637238, 20337.042452, 32546.18937, 40694.549352]) / 1e3
    # line_chart(result_suda_subword0113, result_suda_parallel0113, list_sample_k)

    list_sample_k = [100, 500, 1000, 3000, 5000, 8000, 10000]
    result_suda_subword0113 = np.array(
        [29.27668, 144.987352, 290.223509, 868.914766, 1448.332134, 2323.863474, 2901.982173])
    result_suda_parallel0113 = np.array(
        [0.751965, 3.778848, 7.542349, 22.639896, 37.69508, 60.329705, 75.472882])
    line_chart(result_suda_subword0113, result_suda_parallel0113, list_sample_k)


