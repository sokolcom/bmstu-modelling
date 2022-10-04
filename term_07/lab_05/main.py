from time import time
from random import random


time_unit = 0.01


class EvenDistribution:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def generate(self):
        return self.a + (self.b - self.a) * random()


class Request:
    cur_id = 0

    def __init__(self):
        self.id = Request.cur_id
        Request.cur_id += 1


class Generator:
    def __init__(self, distribution):
        self.work_time_distribution = distribution
        self.time_to_finish = 0

    def update_time(self, dt):
        self.time_to_finish -= dt

        if self.time_to_finish <= 1e-5:
            self.time_to_finish = self.work_time_distribution.generate()
            return Request()

        return None


class Operator:
    def __init__(self, send_to, distribution):
        self.work_time_distribution = distribution
        self.busy = False
        self.send_to = send_to
        self.current_req = None
        self.time_to_finish = 0

    def accept_request(self, request):
        self.busy = True
        self.current_req = request
        self.time_to_finish = self.work_time_distribution.generate()

    def finish_cur_request(self):
        self.send_to.append(self.current_req)
        self.busy = False
        self.current_req = None

    def update_time(self, dt):
        self.time_to_finish -= dt
        if self.busy and self.time_to_finish <= 1e-5:
            self.finish_cur_request()
            return 'request done'
        return 'pass'


class Processor:
    def __init__(self, requests_queue, distribution):
        self.work_time_distribution = distribution
        self.busy = False
        self.requests_queue = requests_queue
        self.current_req = None
        self.time_to_finish = 0

    def update_time(self, dt):
        self.time_to_finish -= dt

        if self.busy and self.time_to_finish <= 1e-5:
            self.busy = False
            self.current_req = None
            return 'request done'

        if not self.busy and len(self.requests_queue) != 0:
            self.current_req = self.requests_queue.pop(0)
            self.time_to_finish = self.work_time_distribution.generate()
            self.busy = True
            return 'request accepted'

        return 'pass'


def pick_operator(operators):
    for i in range(len(operators)):
        if not operators[i].busy:
            return i
    return -1


def one_step(generator, operators, processors, request_info, generate_new=True):
    if generate_new:
        request = generator.update_time(time_unit)
        if request:
            request_info['gen'] += 1
            i_operator = pick_operator(operators)
            if i_operator == -1:
                request_info['loss'] += 1
            else:
                operators[i_operator].accept_request(request)

    for cur_operator in operators:
        cur_operator.update_time(time_unit)

    for cur_processor in processors:
        res = cur_processor.update_time(time_unit)
        if res == 'request done':
            request_info['ok'] += 1


def modeling(generator, operators, processors, total_incoming_requests):
    request_info = { 'gen': 0, 'loss': 0, 'ok': 0 }

    while request_info['gen'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info)

    while request_info['loss'] + request_info['ok'] < total_incoming_requests:
        one_step(generator, operators, processors, request_info, False)

    return request_info


def main():
    client_generator = Generator(EvenDistribution(8, 12))

    first_queue = []
    second_queue = []

    operators = [
        Operator(first_queue, EvenDistribution(15, 25)),  # most powerful
        Operator(first_queue, EvenDistribution(30, 50)),
        Operator(second_queue, EvenDistribution(20, 60))  # least powerful
    ]

    processors = [
        Processor(first_queue, EvenDistribution(15, 15)),  # 15 minutes
        Processor(second_queue, EvenDistribution(30, 30))  # 30 minutes
    ]

    total_requests = 5000

    t_start = time()
    res = modeling(client_generator, operators, processors, total_requests)

    print('Total requests:', total_requests)
    print('Time (seconds):', time() - t_start)
    for key in res.keys():
        print(f"\t{key}\t---\t{res[key]}")

    print('Loss rate:', res['loss'] / total_requests)


if __name__ == '__main__':
    main()
