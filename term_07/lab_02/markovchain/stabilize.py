from .config import TIME_DELTA


def derivative_p(matrix, probas):
    return [
        TIME_DELTA * sum(
            [
                probas[j] * matrix[j][i]
                if i != j else
                probas[j] * (-sum(matrix[i]) + matrix[i][i])
                for j in range(len(matrix))
            ]
        )
        for i in range(len(matrix))
    ]


def get_stabilization_times(matrix, start_probas, limit_probas):
    current_time = 0
    current_probas = start_probas.copy()

    lambda_sum = sum([sum(i) for i in matrix])
    criterion_eps = [p / (100 * lambda_sum) for p in limit_probas]

    stabilization_times = [0 for _ in range(len(matrix))]
    while not all(stabilization_times):
        current_dps = derivative_p(matrix, current_probas)
        for i in range(len(matrix)):
            if ((not stabilization_times[i]) and
                    (abs(current_probas[i] - limit_probas[i]) <= criterion_eps[i]) and
                    (current_dps[i] <= criterion_eps[i])):
                stabilization_times[i] = current_time
            current_probas[i] += current_dps[i]

        current_time += TIME_DELTA
    return stabilization_times


def get_proba_over_time(matrix, start_probas, end_time):
    current_time = 0
    current_probas = start_probas.copy()
    times = []
    probas_over_time = []

    while current_time < end_time:
        probas_over_time.append(current_probas.copy())
        current_dps = derivative_p(matrix, current_probas)
        for i in range(len(matrix)):
            current_probas[i] += current_dps[i]

        current_time += TIME_DELTA
        times.append(current_time)

    return (times, probas_over_time)