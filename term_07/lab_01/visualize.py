import random
import matplotlib.pyplot as plt


COLORS = ["r", "g", "b", "y", "m", "c", "k"]


def create_graphs(x, f_res, cdf_res, label, **kwargs):
    random.shuffle(COLORS)

    fig, axes = plt.subplots(2, figsize=(6, 7))
    fig.suptitle(label)

    for i in range(0, len(f_res)):
        if label == "Нормальное распределение":
            g_label = f"mu={kwargs['mu'][i]}, sigma={kwargs['sigma'][i]}"
        else:
            g_label = f"a={kwargs['a'][i]}, b={kwargs['b'][i]}"

        axes[0].plot(x, f_res[i], color=COLORS[i], label=g_label)
    for i in range(0, len(cdf_res)):
        if label == "Нормальное распределение":
            g_label = f"mu={kwargs['mu'][i]}, sigma={kwargs['sigma'][i]}"
        else:
            g_label = f"a={kwargs['a'][i]}, b={kwargs['b'][i]}"
        axes[1].plot(x, cdf_res[i], color=COLORS[i], label=g_label)

    axes[0].set_xlabel('x')
    axes[1].set_xlabel('x')
    axes[0].set_ylabel('F(x)')
    axes[1].set_ylabel('f(x)')
    axes[0].grid(True)
    axes[1].grid(True)
    axes[0].legend(loc='upper right')
    axes[1].legend(loc='upper right')
    plt.show()