from inspect import getfullargspec
from ast import literal_eval
# import json
# from types import SimpleNamespace
# x = json.loads(data, object_hook=lambda _d: SimpleNamespace(**_d))


class Parameters:
    def __init__(self, data, prefix: str = "", lock: bool = False):
        self._prefix = prefix
        self._called = True
        self.command = data
        self.parameters = ""

        if not lock:
            self.revert()
        else:
            self.convert()

    def convert(self):
        check = False
        blank_prefix = False
        com = self.command

        if isinstance(self._prefix, str):
            check = str(self.command).startswith(self._prefix)
            blank_prefix = False if self._prefix else True

        elif isinstance(self._prefix, list):
            for pre in self._prefix:
                if str(self.command).startswith(pre):
                    check = True

                if check and pre == "":
                    blank_prefix = True

        if check and not blank_prefix:
            try:
                self.command = com.lower().split()[0][1:]
                self.parameters = " ".join(com.split()[1:])
            except Exception:
                self.command = com.lower()
                self.parameters = ""

        elif check and blank_prefix:
            self.command = com.lower().split()[0]
            self.parameters = " ".join(com.split()[1:])

        self._called = check

    def revert(self):
        done = False
        try:
            data = {"command": "", "parameters": ""}

            if isinstance(self.command, str) or isinstance(self.command, bytes):
                data = literal_eval(self.command)

            elif isinstance(self.command, list):
                if self.command:
                    data["command"] = self.command[0]

                if len(self.command) > 1:
                    data["parameters"] = self.command[1:]

            else:
                data = self.command

            self.command = data.get("command")
            self.parameters = data.get("parameters")

            done = True

            for key, value in data.items():
                if key not in ["command", "parameters"]:
                    setattr(self, key, value)

        except Exception:
            if not done:
                self.convert()

    def transform(self):
        return self.__dict__

    def clear(self):
        delattr(self, "command")
        delattr(self, "parameters")
        delattr(self, "_prefix")
        delattr(self, "_called")

    def build_str(self):
        res = ""
        for key, value in self.__dict__.items():
            res += f"{key} : {value}\n"

        return res

    def __str__(self):
        return self.build_str()

    def setattr(self, key, value):
        setattr(self, key, value)

    def delattr(self, key):
        delattr(self, key)


class Decorator:
    def __init__(self):
        self.events = {}
        self.command = self.event

    def command_exist(self, name: str):
        return self.events.get(name)

    def get_commands(self):
        return self.events.keys()

    def event(self, aliases=None, condition=None):
        if isinstance(aliases, str):
            aliases = [aliases]
        elif not aliases:
            aliases = []

        if not callable(condition):
            condition = None

        def add_command(command_funct):
            aliases.append(command_funct.__name__)
            for command in aliases:
                self.events[command.lower()] = {"command": command_funct, "condition": condition}
            return command_funct

        return add_command


class Commands(Parameters, Decorator):
    def __init__(self, prefix: str = "", lock: bool = False):
        Decorator.__init__(self)
        self.prefix = prefix
        self._lock = lock

    def build_arguments(self, function, arguments):
        values = getfullargspec(function)

        arg = values.args
        arg.pop(0)

        default = values.defaults
        ext_default = values.kwonlydefaults

        para = {}

        if default:
            default = list(default)
            for i in range(-1, -len(default)-1, -1):
                para[arg[i]] = default[i]

        ext = None

        if values.kwonlyargs:
            ext = values.kwonlyargs[0]
            arg.extend(values.kwonlyargs)

        s = len(arg)
        dico = {}

        if ext:
            if not (isinstance(arguments, list) or isinstance(arguments, dict)):
                arguments = arguments.split()

            sep = len(arguments) - s + 1

            if not sep:
                sep = 1

            for i in range(s):
                key = arg[i]

                if key != ext:
                    if isinstance(arguments, list):
                        try:
                            dico[key] = arguments.pop(0)
                        except IndexError:
                            if key in para.keys():
                                dico[key] = para[key]

                    elif isinstance(arguments, dict):
                        try:
                            dico[key] = arguments[key]
                        except KeyError:
                            if key in para.keys():
                                dico[key] = para[key]

                else:
                    li = []
                    if isinstance(arguments, list):
                        for _ in range(sep):
                            try:
                                li.append(arguments.pop(0))
                            except IndexError:
                                pass

                    elif isinstance(arguments, dict):
                        try:
                            li.append(arguments[key])
                        except KeyError:
                            pass

                    if not li and ext_default and ext_default.get(key):
                        li = [ext_default[key]]

                    dico[key] = li

        elif s:
            if isinstance(arguments, list):
                dico = {key: value for key, value in zip(arg, arguments[0:s])}

            elif isinstance(arguments, dict):
                for key in arg:
                    try:
                        dico[key] = arguments[key]
                    except KeyError:
                        if key in para.keys():
                            dico[key] = para[key]
            else:
                dico = {key: value for key, value in zip(arg, arguments.split()[0:s])}

        return dico

    def execute(self, data: Parameters):
        com = self.events[data.command].get("command")
        con = self.events[data.command].get("condition")

        dico = self.build_arguments(com, data.parameters)

        # data.parameters = dico
        for name in ["command", "parameters", "_called", "_prefix"]:
            delattr(data, name)

        if (con and con(data)) or not con:
            return com(data, **dico)

    def process_data(self, data, lock: bool = None):
        none = type(None)

        if isinstance(lock, none):
            lock = self._lock

        args = data

        # if not isinstance(data, Parameters):
        if not str(type(data)).endswith("<class 'easy_events.async_commands.Parameters'>"):
            args = Parameters(data, self.prefix, lock)

        # print("-"*15 + f"\n{args}\n" + "-"*15 + "\n")

        if isinstance(args.command, str) and self.command_exist(args.command) and args._called:
            try:
                val = self.execute(args)
            except Exception as e:
                raise e
                return f"{type(e)}: {e}"

            if isinstance(val, Parameters):
                return val.transform()

            return val

        if isinstance(data, bytes):
            return data.decode()

        return data
