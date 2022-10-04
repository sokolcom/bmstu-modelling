import random


def step_model(generator, handler, total_tasks=0, repeat=0, step=1e-3):
    t_current = step
    t_gen = generator.yield_value()
    t_gen_prev = t_proc = 0
    processed_tasks = 0
    current_queue_length = 0
    max_queue_length = 0
    free = True

    while processed_tasks < total_tasks:
         # Generator
        if t_current > t_gen:
            current_queue_length += 1
            if current_queue_length > max_queue_length:
                max_queue_len = current_queue_length
            t_gen_prev = t_gen
            t_gen += generator.yield_value()

        # Handler
        if t_current > t_proc:
            if current_queue_length > 0:
                was_free = free
                if free:
                    free = False
                else:
                    processed_tasks += 1
                    if random.randint(1, 100) <= repeat:
                        current_queue_length += 1
                current_queue_length -= 1
                if was_free:
                    t_proc = handler.yield_value() + t_gen_prev
                else:
                    t_proc += handler.yield_value()
            else:
                free = True

        t_current += step

    return max_queue_len
