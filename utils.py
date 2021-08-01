import numpy as np
from matplotlib import pyplot as plt

def plot(x, y_list, labels, xlabel, ylabel, title):
    fig, ax = plt.subplots()
    assert len(y_list) == len(labels)
    for y, label in zip(y_list, labels):
        ax.plot(x, y, label=label)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    plt.show()

def plot_bar(x, y1, y2, label1, label2, xlabel, ylabel, title, width=0.35):
    x_pos = np.arange(len(x))
    fig, ax = plt.subplots()
    rects1 = ax.bar(x_pos + width / 2, y1, width, label=label1)
    rects2 = ax.bar(x_pos - width / 2, y2, width, label=label2)
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    plt.show()

