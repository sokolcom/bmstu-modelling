from random import randint


def add_event(new_event, events):
    i = 0
    while (i < len(events)) and (events[i]["value"] < new_event["value"]):
        i += 1
    if (0 < i) and (i < len(events)):
        events.insert(i - 1, new_event)
    else:
        events.insert(i, new_event)


def event_model(generator, handler, total_tasks=0, repeat=0):
    handled_tasks = 0
    current_queue_length = 0
    max_queue_length = 0
    events = [{ "value": generator.yield_value(), "type": "generator" }]
    free, handle_flag = True, False

    while handled_tasks < total_tasks:
        event = events.pop(0)

        # Generator
        if event["type"] == "generator":
            current_queue_length += 1
            if current_queue_length > max_queue_length:
                max_queue_length = current_queue_length
            add_event({ "value": event["value"] + generator.yield_value(), "type": "generator"}, events)
            if free:
                handle_flag = True
        # Handler
        elif event["type"] == "handler":
            handled_tasks += 1
            if randint(1, 100) <= repeat:
                current_queue_length += 1
            handle_flag = True

        if handle_flag:
            if current_queue_length > 0:
                current_queue_length -= 1
                add_event({ "value": event["value"] + handler.yield_value(), "type": "handler" }, events)
                free = False
            else:
                free = True
            handle_flag = False

    return max_queue_length
