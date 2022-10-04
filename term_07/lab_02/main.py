from markovchain.linalg import linalg_solve
from markovchain.stabilize import *
from markovchain.visualize import digraph, graph_proba_over_time
from auxiliary import *


def main():
    n = 5
    end_time = 10

    # intensity_matrix = generate_matrix(n)
    # n, intensity_matrix = create_matrix()
    intensity_matrix = get_predef_intensity(n)
    start_probas = get_start_probas(n, True)

    # Calculate limit probas
    limit_probas = linalg_solve(intensity_matrix)
    print_output('Предельные вероятности:', 'p', limit_probas)

    # Calculate stabilization times
    stabilization_times = get_stabilization_times(intensity_matrix, start_probas, limit_probas)
    times, probas_over_time = get_proba_over_time(intensity_matrix, start_probas, end_time)
    print_output('Время стабилизации:', 't', stabilization_times)

    # Calculate times per each state
    times_in_state = list(map(lambda x: x * end_time, limit_probas))
    print_output('Время процесса в состоянии:', 'tp', times_in_state)

    # Print graphs
    digraph(intensity_matrix)
    graph_proba_over_time(limit_probas, probas_over_time, times, stabilization_times)


if __name__ == "__main__":
    main()