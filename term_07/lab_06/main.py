from random import shuffle
import numpy.random


class RandomGenerator:
    def __init__(self, begin, delta=0):
        self.begin = begin
        self.d = delta

    def new_random(self):
        if (self.d == 0):
            return self.begin
        return numpy.random.uniform(self.begin - self.d, self.begin + self.d)


class GenerateRequest:
    def __init__(self, generator, name, count):
        self.random_generator = generator
        self.num_requests = count
        self.receivers = []
        self.next = 0
        self.name = name

    def generate_request(self):
        self.num_requests -= 1
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        return self.random_generator.new_random()


class ProcessRequest:
    def __init__(self, generator, name, kick_probability=0, max_queue_size=-1, end=False):
        self.random_generator = generator
        self.queue = 0
        self.received = 0
        self.max_queue = max_queue_size
        self.processed = 0
        self.next = 0
        self.receivers = []
        self.end = end
        self.name = name
        self.kick_probability = kick_probability

    def receive_request(self):
        if self.max_queue == -1 or self.max_queue > self.queue:
            self.queue += 1
            self.received += 1
            return True
        return False

    def process_request(self):
        if numpy.random.sample() < self.kick_probability:
            return "kick"
        if self.queue > 0:
            self.queue -= 1
            self.processed += 1
        shuffle(self.receivers)
        for receiver in self.receivers:
            if receiver.receive_request():
                return receiver
        return None

    def delay(self):
        return self.random_generator.new_random()


class Model:
    def __init__(self, clients, mask_check, temp_check, terminals, windows):
        self.clients = clients
        self.mask_check = mask_check
        self.temp_check = temp_check
        self.terminals = terminals
        self.windows = windows

    def event_mode(self):
        clients = self.clients
        mask = self.mask_check

        clients.receivers = self.mask_check.copy()
        self.mask_check[-1].receivers = self.temp_check.copy()
        self.temp_check[-1].receivers = self.terminals.copy()

        self.terminals[0].receivers = self.windows.copy()
        self.terminals[1].receivers = self.windows.copy()
        self.terminals[2].receivers = self.windows.copy()

        clients.next = clients.delay()

        blocks = []
        blocks += [clients]
        blocks += self.mask_check
        blocks += self.temp_check
        blocks += self.terminals
        blocks += self.windows

        refusals = {}

        for block in blocks:
            refusals[block.name] = 0
        refusals["query_window"] = 0

        while clients.num_requests >= 0:
            current_time = clients.next
            for block in blocks:
                if (0 < block.next) and (block.next < current_time):
                    current_time = block.next

            for block in blocks:
                if current_time == block.next:
                    if not isinstance(block, ProcessRequest):
                        next_clients = clients.generate_request()
                        if next_clients is not None:
                            next_clients.next = current_time + next_clients.delay()
                        else:
                            refusals[block.name] += 1
                        clients.next = current_time + clients.delay()
                    else:
                        next_process = block.process_request()
                        if block.queue == 0:
                            block.next = 0
                        else:
                            block.next = current_time + block.delay()

                        if next_process == "kick":
                            if block.name.find("terminal") != -1:
                                refusals["query_window"] += 1
                            else:
                                refusals[block.name] += 1
                            continue

                        if block.end:
                            continue

                        if next_process is not None:
                            next_process.next = current_time + next_process.delay()
                        else:
                            refusals[block.name] += 1

        return refusals


def main():
    # 5 2
    t_clients = int(input("Время прихода посетителей: "))
    dt_clients = int(input("Дельта прихода посетителей: "))

    # 1 0
    t_mask = int(input("Время проверки наличия маски: "))
    dt_mask = int(input("Дельта проверки наличия маски: "))

    # 3 1
    t_temp = int(input("Время проверки температуры: "))
    dt_temp = int(input("Дельта проверки температуры: "))

    # 4 1
    t_terminal = int(input("Время получения очереди в терминалах: "))
    dt_terminal = int(input("Дельта получения очереди в терминалах: "))

    # 15 5
    t_window1 = int(input("Время работы в окне 1: "))
    dt_window1 = int(input("Дельта работы в окне 1: "))

    # 10 2
    t_window2 = int(input("Время работы в окне 2: "))
    dt_window2 = int(input("Дельта работы в окне 2: "))

    # 20 5
    t_window3 = int(input("Время работы в окне 3: "))
    dt_window3 = int(input("Дельта работы в окне 3: "))

    # 800
    clients_number = int(input("Количество посетителей: "))

    min_res = None
    max_res = None
    min_sum = None
    max_sum = None

    for i in range(100):
        clients = GenerateRequest(RandomGenerator(t_clients, dt_clients), "entry", clients_number)

        mask_check = [
            ProcessRequest(
                RandomGenerator(t_mask, dt_mask),
                "mask_check",
                0.05,
                -1,
            )
        ]

        temp_check = [
            ProcessRequest(
                RandomGenerator(t_temp, dt_temp),
                "temp_check",
                0.02,
                -1,
            )
        ]

        terminals = [
            ProcessRequest(
                RandomGenerator(t_terminal, dt_terminal),
                "terminal1",
                0.05,
                max_queue_size=1,
            ),
            ProcessRequest(
                RandomGenerator(t_terminal, dt_terminal),
                "terminal2",
                0.05,
                max_queue_size=1,
            ),
            ProcessRequest(
                RandomGenerator(t_terminal, dt_terminal),
                "terminal3",
                0.05,
                max_queue_size=1,
            ),
        ]

        windows = [
            ProcessRequest(
                RandomGenerator(t_window1, dt_window1),
                "window1",
                0.0,
                max_queue_size=10,
                end=True
            ),
            ProcessRequest(
                RandomGenerator(t_window2, dt_window2),
                "window2",
                0.0,
                max_queue_size=10,
                end=True
            ),
            ProcessRequest(
                RandomGenerator(t_window3, dt_window3),
                "window3",
                0.0,
                max_queue_size=10,
                end=True
            ),
        ]

        model = Model(clients, mask_check, temp_check, terminals, windows)
        result = model.event_mode()
        summ = 0

        if min_res is None:
            min_res = result.copy()
            max_res = result.copy()
            min_sum = sum(result.values())
            max_sum = sum(result.values())
        else:
            for key in result.keys():
                summ += result[key]
                if result[key] < min_res[key]:
                    min_res[key] = result[key]
                if result[key] > max_res[key]:
                    max_res[key] = result[key]
            if summ < min_sum:
                min_sum = summ
            if summ > max_sum:
                max_sum = summ

    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓")
    print("┃ Наименование этапа               ┃      min      ┃      max      ┃")
    print("┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━┫")
    print("┃ Отказы при проверке маски        ┃{:^15d}┃{:^15d}┃".format(min_res["mask_check"], max_res["mask_check"]))
    print("┃ Отказы при проверке температуры  ┃{:^15d}┃{:^15d}┃".format(min_res["temp_check"], max_res["temp_check"]))
    print("┃ Отказы на терминале 1            ┃{:^15d}┃{:^15d}┃".format(min_res["terminal1"], max_res["terminal1"]))
    print("┃ Отказы на терминале 2            ┃{:^15d}┃{:^15d}┃".format(min_res["terminal2"], max_res["terminal2"]))
    print("┃ Отказы на терминале 3            ┃{:^15d}┃{:^15d}┃".format(min_res["terminal3"], max_res["terminal3"]))
    print(
        "┃ Отказы при распределении очереди ┃{:^15d}┃{:^15d}┃".format(min_res["query_window"], max_res["query_window"]))
    print("┃ Отказы на окне 1                 ┃{:^15d}┃{:^15d}┃".format(min_res["window1"], max_res["window1"]))
    print("┃ Отказы на окне 2                 ┃{:^15d}┃{:^15d}┃".format(min_res["window2"], max_res["window2"]))
    print("┃ Отказы на окне 3                 ┃{:^15d}┃{:^15d}┃".format(min_res["window3"], max_res["window3"]))
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━┛")

    print()
    print(
        "Всего отказов:\n"
        f"   минимум - {min_sum} ({round(min_sum / clients_number * 100, 2)}%)\n"
        f"   максимум - {max_sum} ({round(max_sum / clients_number * 100, 2)}%)\n"
    )
    print()


if __name__ == '__main__':
    main()