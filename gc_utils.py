import random
import re
from multiprocessing import Process, Queue
import queue

from gc_interpreter import Interpreter


def random_inverse_square():
    random_value = random.random()

    inverse_square_number = 1 / (random_value**0.5)

    return inverse_square_number


def get_variables(program):
    return set(re.findall("v[0-9]+", program))


def split_command(command: list[str]):
    nest_level = 0
    action_no = 0

    main = []

    commands = []

    for word in command:
        if word == ")":
            nest_level -= 1

            if nest_level == 0:
                continue

        if word == "(":
            nest_level += 1

            if nest_level == 1:
                if action_no != 0:
                    action_no += 1
                commands.append([])
                continue

        if word == ";" and nest_level == 1:
            action_no += 1
            commands.append([])
            continue

        if nest_level == 0:
            main.append(word)
        else:
            commands[action_no].append(word)

    return main, commands


def combine_command(main, commands):
    result = []

    result.extend(main)

    if len(commands) > 0:
        result.append("(")

        for i, command in enumerate(commands):
            result.extend(command)

            if i != len(commands) - 1:
                result.append(";")

        result.append(")")

    return result


class Runner:
    def __init__(self, interpreter: Interpreter) -> None:
        self.interpreter = interpreter
        self.worker = None
        self.task_queue = None
        self.output_queue = None

    def work(self) -> None:
        while True:
            code, inputs = self.task_queue.get(True)
            try:
                result = self.interpreter.run(code, inputs)
                self.output_queue.put(result)
            except:
                self.output_queue.put(None)

    def create_worker(self, replace=False) -> None:
        if not replace and self.worker:
            return

        if self.worker:
            self.worker.kill()

        self.task_queue, self.output_queue = Queue(), Queue()

        self.worker = Process(target=self.work, args=())

        self.worker.start()

    def run(self, code: str, inputs: list[int] = []) -> list[int]:
        self.create_worker()

        self.task_queue.put((code, inputs))

        try:
            return self.output_queue.get(True, 0.1)
        except queue.Empty:
            self.create_worker(True)
            return None
