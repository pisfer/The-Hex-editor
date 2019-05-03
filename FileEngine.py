
from typing import BinaryIO

from typing import *
import os

import base64 as bs


# gv


class File:
    def __init__(self, file, mode):
        self.mode = mode
        self.file = file
        self.ob = open(file, mode)

    def read(self, n: int = -1) -> AnyStr:
        return self.ob.read(n)

    def seek(self, offset: int, whence: int = 0):
        self.ob.seek(offset, whence)

    def write(self, s):
        self.ob.write(s)

    def writelines(self, lines: List[AnyStr]) -> None:
        self.ob.writelines(lines)

    def readline(self, limit: int = -1):
        return self.ob.readline(limit)

    def readlines(self, hint: int = -1):
        return self.ob.readlines(hint)

    def tell(self) -> int:
        return self.ob.tell()

    def close(self):
        self.ob.close()


class Wrap:
    def __init__(self, string, width):
        self.string = string
        self.width = width
        self.ret = []

    def start_wrap(self):
        for i in range(self.width, len(self.string)+self.width, self.width):
            self.ret.append(self.string[i-self.width:i])
        return self.ret


class FileEngine(File):
    copy_object: BinaryIO
    rad: object

    def __init__(self, file: object, mode: str, copy_file=None, encoding="utf-8"):
        """

        :rtype: object
        """
        self.g = bytes.maketrans("\u2028\u2029\t\n\r\v\f\uFFFD".encode(encoding=encoding), b"." * 14)
        #self.g_error = bytes.maketrans(bytearray(range(0x20, 0xFFFF)), b"?" * len(range(0x20, 0xFFFF)))
        self.frad = False
        self.copy_file = copy_file
        self.steps = 0
        self.pop = 0
        self.encoding = encoding
        super().__init__(file, mode)
        if mode == "rb":
            try:
                self.data = list(map(lambda n: int(n), Wrap(self.read(20).decode(self.encoding), 10).start_wrap()))
            except ValueError:
                self.frad = False
            # self.read_sth(step, encoding)
        elif mode == "wb":
            pass
        else:
            raise TypeError
        self.file = file

    def write_sth(self):
        self.size_copy = os.path.getsize(self.copy_file)
        self.write(str(self.size_copy * 2).rjust(10, "0").encode() + str(self.size_copy).rjust(10, "0").encode())
        self.copy_object = open(self.copy_file, "rb")
        self.pop = self.size_copy
        while self.pop >= 0:
            self.pop -= 1024
            self.write(bs.b16encode(self.copy_object.read(1024)))
        self.pop = self.size_copy
        self.copy_object.seek(0)
        while self.pop >= 0:
            self.pop -= 1024
            self.write(self.copy_object.read(1024))

    def read_as_new(self, mode, step=1024, encoding=None):
        encoding = self.encoding if encoding is None else encoding
        if self.steps >= os.path.getsize(self.file) or self.frad:
            self.steps = 0
        if mode == "+":
            self.steps += step
            self.seek(self.steps - step)
            self.new_rad = self.read(step)
            self.new2_rad = bs.b16encode(self.new_rad).decode(encoding)
            print(self.g, self.new_rad, "ashope-")
            self.new_rad = self.new_rad.translate(self.g)
            #self.new_rad = self.new_rad.translate(self.g_error)
        else:
            if self.steps - step <= 0:
                self.steps = step
            else:
                self.steps -= step
            self.steps -= step
            self.seek(self.steps - step)
            self.new_rad = self.read(step)
            self.new2_rad = bs.b16encode(self.new_rad).decode(encoding)
            self.new_rad = self.new_rad.translate(self.g)
            #self.new_rad = self.new_rad.translate(self.g_error)

        return list(map(lambda n: Wrap(n, 2).start_wrap(), Wrap(self.new2_rad, 32).start_wrap())), Wrap(
            self.new_rad.decode(encoding,  errors='ignore'), 16).start_wrap()

    def read_sth(self, mode, step=1024, encoding=None):
        self.frad = True
        encoding = self.encoding if encoding is None else encoding
        if self.steps >= os.path.getsize(self.file):
            self.steps = 0
        if mode == "+":
            self.steps += step
            self.seek(self.steps - step + 20)
            print(self.steps - step + 20)
            self.rad = self.read(step * 2 if step * 2 < self.data[0] else self.data[0])
            self.seek(self.steps - step + self.data[0] + 20)
            self.rad2 = self.read(step).decode(encoding)
            self.rad = self.rad.translate(self.g)
            #self.rad = self.rad.translate(self.g_error).decode(encoding)
        else:
            if self.steps - step < 20:
                self.steps = step
            else:
                self.steps -= step
            self.seek(self.steps - step + 20)
            print(self.steps - step + 20)
            self.rad = self.read(step * 2 if step * 2 < self.data[0] else self.data[0])
            self.seek(self.steps - step + self.data[0] + 20)
            self.rad2 = self.read(step).decode(encoding)
            self.rad = self.rad.translate(self.g)
            #self.rad = self.rad.translate(self.g_error).decode(encoding)

        return list(map(lambda n: Wrap(n, 2).start_wrap(), Wrap(self.rad, 32).start_wrap())), Wrap(self.rad2, 16).start_wrap()


if __name__ == '__main__':
    pass
