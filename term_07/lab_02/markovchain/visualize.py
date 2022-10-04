from matplotlib import collections
import networkx as nx
import matplotlib.pyplot as plt

from .config import EPS


def matrix2nx(matrix):
    row_size, col_size = len(matrix), len(matrix[0])
    result = []
    for i_row in range(row_size):
        for i_col in range(col_size):
            weight = matrix[i_row][i_col]
            if weight > EPS:
                result.append((i_row, i_col, weight))
    return result


def digraph(matrix):
    dg = nx.DiGraph()
    dg.add_weighted_edges_from(matrix2nx(matrix))
    layout = nx.shell_layout(dg)

    nx.draw(dg, layout, with_labels=True)
    labels = nx.get_edge_attributes(dg, 'weight')
    nx.draw_networkx_edge_labels(dg, layout, edge_labels=labels, label_pos=0.2)
    plt.show()


def graph_proba_over_time(probas, probas_over_time, times, stabilization_times):
    for idx in range(len(probas_over_time[0])):
        plt.plot(times, [i[idx] for i in probas_over_time])
        plt.scatter(stabilization_times[idx], probas[idx])

    plt.legend([f"Состояние #{i}" for i in range(len(probas))], loc='upper right')
    plt.xlabel('Время')
    plt.ylabel('Вероятность')
    plt.show()
