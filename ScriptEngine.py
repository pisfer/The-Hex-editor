from re import *
import textwrap

data_command = {
    "configure": r"-configure\.(?P<command>[^><]+)<(?P<dat>.+)>",
    "on_click": "-on_click\.(?P<command>[^><]+)<(?P<dat>.+)>",
    "do": "-do\.(?P<command>[wd]+)"
}

class Interpreter:
    def __init__(self, file, data):
        self.data = data
        self.file = file
        self.open_file = open(self.file, "r")

    def intr(self):
        for i in self.open_file.readlines():
            print(i)


if __name__ == '__main__':
    print(match('-configure\.(?P<command>[^><]+)<(?P<dat>.+)>', "-configure.menu!File!Open<h>"))
