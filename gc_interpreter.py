class Interpreter:
    def __init__(self, interactive: bool = True):
        self.interactive = interactive
        self.variables = {}
        self.inputs = []
        self.actions = {
            "SET": self.set_variable,
            "COPY": self.copy_variable,
            "YIELD": self.yield_variable,
            "INPUT": self.input_number,
            "ADD": self.add_variables,
            "SUB": self.subtract_variables,
            "MUL": self.multiply_variables,
            "DIV": self.divide_variables,
            "MOD": self.mod_variables,
            "POW": self.pow_variables,
            "IF": self.if_comp,
            "LOOP": self.loop,
            "MULTI": self.multi,
            "NOP": self.nop,
        }

    def run(self, code, inputs: list[int] = [], recurse: bool = False):
        lines = code.split("\n")

        self.inputs = inputs.copy()

        result = []

        for line in lines:
            if line.strip():
                main, commands = self.split_command(line.split())
                action, arguments = main[0], main[1:]

                if action in self.actions:
                    action_res = self.actions[action](
                        arguments,
                        commands,
                    )

                    if action_res is not None:
                        result.extend(action_res)

        if not recurse:
            self.variables = {}

        return result

    def split_command(self, command):
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

    def set_variable(self, args, commands):
        if len(args) != 2 or len(commands) != 0:
            return

        var_name, value = args

        self.variables[var_name] = int(value)

    def copy_variable(self, args, commands):
        if len(args) != 2 or len(commands) != 0:
            return

        to_var, from_var = args

        if to_var not in self.variables or from_var not in self.variables:
            return

        self.variables[to_var] = self.variables[from_var]

    def yield_variable(self, args, commands):
        if len(args) != 1 or len(commands) != 0:
            return

        (var_name,) = args

        if var_name in self.variables:
            if self.interactive:
                print(self.variables[var_name])
            else:
                return [self.variables[var_name]]

    def input_number(self, args, commands):
        if len(args) != 1 or len(commands) != 0:
            return

        (var_name,) = args

        if var_name in self.variables:
            if self.interactive:
                i = input()
                if i.isnumeric():
                    self.variables[var_name] = int(i)
            else:
                if len(self.inputs) > 0:
                    self.variables[var_name] = self.inputs.pop()

    def add_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] + self.variables[var2]
            self.variables[to] = result

    def subtract_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] - self.variables[var2]
            self.variables[to] = result

    def multiply_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] * self.variables[var2]
            self.variables[to] = result

    def divide_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] // self.variables[var2]
            self.variables[to] = result

    def mod_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] % self.variables[var2]
            self.variables[to] = result

    def pow_variables(self, args, commands):
        if (len(args) != 2 and len(args) != 3) or len(commands) != 0:
            return

        var1, var2, *rest = args

        to = var1

        if len(args) == 3:
            to = rest[0]

        if var1 in self.variables and var2 in self.variables and to in self.variables:
            result = self.variables[var1] ** self.variables[var2]
            self.variables[to] = result

    def if_comp(
        self,
        args,
        commands,
    ):
        if len(args) != 3 or (len(commands) != 2 and len(commands) != 1):
            return

        left_var, operator, right_var = args

        if_result = False

        if not left_var in self.variables or not right_var in self.variables:
            return

        left = self.variables[left_var]
        right = self.variables[right_var]

        if operator == ">" and left > right:
            if_result = True
        elif operator == ">=" and left >= right:
            if_result = True
        elif operator == "=" and left == right:
            if_result = True
        elif operator == "<=" and left <= right:
            if_result = True
        elif operator == "<" and left < right:
            if_result = True
        elif operator == "!=" and left != right:
            if_result = True

        if if_result:
            result = self.run(" ".join(commands[0]), self.inputs, True)

            if not self.interactive:
                return result
        elif len(commands) == 2:
            result = self.run(" ".join(commands[1]), self.inputs, True)

            if not self.interactive:
                return result

    def loop(self, args, commands):
        if len(args) != 2 or len(commands) != 1:
            return

        count_var, index_var = args

        results = []

        if count_var in self.variables and index_var in self.variables:
            index_before = self.variables[index_var]

            for i in range(self.variables[count_var]):
                self.variables[index_var] = i + 1
                results.extend(self.run(" ".join(commands[0]), self.inputs, True))

            self.variables[index_var] = index_before

        if not self.interactive:
            return results

    def multi(self, args, commands):
        if len(args) != 0 or len(commands) != 2:
            return

        results = []

        results.extend(self.run(" ".join(commands[0]), self.inputs, True))
        results.extend(self.run(" ".join(commands[1]), self.inputs, True))

        return results

    def nop(self, args, commands):
        pass


if __name__ == "__main__":
    import sys

    interpreter = Interpreter()

    with open(sys.argv[1], "r") as f:
        print(interpreter.run(f.read()))
