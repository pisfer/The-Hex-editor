import os, sys
from project.FileEngine import FileEngine
from tkinter import Tk, Text, Menu, StringVar, IntVar, TclError
from tkinter.constants import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
from tkinter.messagebox import showinfo, showerror
import json as js
import base64 as bs

# global wars
mmm = []
ENCODINGS = ("ASCII", "CP037", "CP850", "CP1140", "CP1252",
             "Latin1", "ISO8859_15", "Mac_Roman", "UTF-8",
             "UTF-8-sig", "UTF-16", "UTF-32")
savefilename = None
openfile = None


class rgb:
    def __new__(cls, *args, **kwargs):
        cls.args = args

        return "#{:02X}{:02X}{:02X}".format(args[0], args[1], args[2])


class Main(Tk):
    """
    Just edit Main()
    """
    open_file: object

    def __init__(self):
        super().__init__()
        self.fish = ()
        self.base_memory = [1024, "+"]
        self._create_window()

    def _create_window(self):
        # Root configure
        self.wm_resizable(False, False)
        self.wm_geometry("780x800")
        self.configure(bg="#3C3F41")

        # Frame
        self.top_control = Frame(self)
        self.left_hand_frame = Frame(self)
        self.right_hand_frame = Frame(self)

        self.top_control.pack(side=TOP)
        self.left_hand_frame.pack(side=LEFT)
        self.right_hand_frame.pack(side=RIGHT)

        # Scrollbar
        self.scrollbar = Scrollbar(self.left_hand_frame, orient=VERTICAL, command=self.on_scrollbar)
        self.scrollbar_d = Scrollbar(self.right_hand_frame, orient=VERTICAL, command=self.on_scrollbar)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar_d.pack(side=RIGHT, fill=Y)

        # Menu
        self.menu = Menu(self)
        self.configure(menu=self.menu)

        self.file_menu = Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.menu_open)
        self.file_menu.add_command(label="Save", command=self.menu_save, state=DISABLED)
        self.file_menu.add_command(label="Save as")

        self.menu.add_cascade(label="File", menu=self.file_menu)

        # Text lines
        self.text = Text(self.left_hand_frame, bg="#2B2B2B", width=47, fg="white", height=32, relief="flat",
                         yscrollcommand=self.scroll_func)
        self.text.insert(END,
                        "12 34 56 78 90 as df gh jk ls 12 gh 5t e4 gt ui"+"\n")
        self.text.insert(END,"as df gh jk lpn1 v2 h4 6j o9 u7 ff 34 "
                         "9s 99")
        self.text_hex = Text(self.right_hand_frame, bg="#2B2B2B", fg="white", width=16, height=32, relief="flat",
                             yscrollcommand=self.scroll_func)
        self.text_hex.insert(END, "12345\n12345\n12345\n12345")

        self.text.pack(side=LEFT)
        self.text_hex.pack(side=RIGHT)

        # Control panel
        self.svar = StringVar()
        self.ivar = IntVar()
        self.ivar.set(1024)
        self.fr = Radiobutton(self.top_control, text="512", variable=self.ivar,
                              value=512, command=self.change_increment)
        self.fr2 = Radiobutton(self.top_control, text="1024", variable=self.ivar,
                               value=1024, command=self.change_increment)

        self.fr.pack(side=RIGHT)
        self.fr2.pack(side=RIGHT, padx=5)

        self.spin = Spinbox(self.top_control, from_=0, textvariable=self.svar, increment=1024, to=10000,
                            wrap=True, command=self.draw, state=DISABLED)  # readonly
        self.spin.set(1024)
        self.spin_encoding = Spinbox(self.top_control, value=ENCODINGS, command=self.set_encoding)
        self.spin_encoding.set("utf-8")
        self.spin_encoding.pack()
        self.spin.pack()

        # Func
        self.bind_all("q", lambda event=None: print(self.text.get(0.0, END)))
        self._copy()
        self._opposite_copy()

    def set_encoding(self):
        self.file.encoding = self.spin_encoding.get()

    def menu_open(self):
        """we should use repr, not decode"""
        self.text.delete(0.0, END)
        self.text_hex.delete(0.0, END)

        self.open_file = askopenfilename(filetypes=(("eHex File", "*.eHex"),
                                                    ("All files", "*.*")))
        if self.open_file == '':
            pass
        else:
            self.spin.configure(state="readonly")
            self.file_menu.entryconfigure("Save", state=NORMAL)
            openfile = self.open_file
            print(os.path.getsize(self.open_file) if os.path.getsize(self.open_file) > 1024 else 1024)
            self.spin["to"] = os.path.getsize(self.open_file) if os.path.getsize(self.open_file) > 1024 else 1024

            self.file = FileEngine(self.open_file, "rb", encoding=self.spin_encoding.get())
            try:
                insert = self.file.read_sth("+", 1024)
            except AttributeError:
                insert = self.file.read_as_new("+", 1024)
            print("-start", insert)
            for i in insert[0]:
                print(type(i),i, " ".join(i)+"!", bs.b16decode("".join(i).encode()))
                self.text.insert(END, " ".join(i)+"\n")
            for i in insert[1]:
                print(type(i), i)
                self.text_hex.insert(END,i+"\n")
            print("hi")

    def menu_save(self):
        if savefilename is None:
            self.save_file = asksaveasfile(filetypes=(("eHex File", "*.eHex"),
                                                      ("All files", "*.*")))

            self.ob_file = FileEngine(self.save_file, "rb", openfile, encoding=self.spin_encoding.get())
            self.ob_file.write_sth()
            self.ob_file.close()

    def change_increment(self):
        self.spin["increment"] = self.ivar.get()

    def draw(self):
        self.text.delete(0.0, END)
        self.text_hex.delete(0.0, END)
        var = 0

        if int(self.spin.get()) < self.base_memory[0]:
            self.base_memory[0] = int(self.spin.get())
            self.base_memory[1] = "-"
            var = 0
            try:
                self.pre_draw = self.file.read_sth("-", int(self.spin.get()))
            except AttributeError:
                self.pre_draw = self.file.read_as_new("-", int(self.spin.get()))

            for i in self.pre_draw[0]:
                self.text.insert(END, i+'\n')
                var += 1
            var = 0
            for i in self.pre_draw[1]:
                self.text_hex.insert(END, i+'\n')
                var += 1

        elif int(self.spin.get()) > self.base_memory[0]:
            self.base_memory[0] = int(self.spin.get())
            self.base_memory[1] = "+"
            var = 0
            try:
                self.pre_draw = self.file.read_sth("+", int(self.spin.get()))
            except AttributeError:
                self.pre_draw = self.file.read_as_new("+", int(self.spin.get()))

            for i in self.pre_draw[0]:
                self.text.insert(END, " ".join(i)+'\n')
                var += 1
            var = 0
            for i in self.pre_draw[1]:
                self.text_hex.insert(END, i+'\n')
                var += 1

        print(self.base_memory, self.pre_draw)

    def scroll_func(self, *args):
        self.scrollbar.set(*args)
        self.scrollbar_d.set(*args)
        self.on_scrollbar('moveto', args[0])

    def on_scrollbar(self, *args):
        """Scrolls both text widgets when the scrollbar is moved"""
        self.text.yview(*args)
        self.text_hex.yview(*args)

    def _copy(self):
        self.after(20, self._copy)
        try:
            try:
                self.text_hex.tag_configure("selle", background="white", foreground="black")
                self.text_hex.tag_delete("selle")
            except TclError:
                pass
            self.first = self.text.index(SEL_FIRST).split(".")
            self.second = self.text.index(SEL_LAST).split(".")
            # print(self.first, self.second)

            self.first = (self.first[0],
                          str(self._pround(
                              (int(
                                  self.first[1]) + (
                                   1 if (int(self.first[1]) + 1) % 3 == 0 else 0)
                               ) / 3)))
            self.second = (self.second[0],
                           str(self._pround(
                               (int(
                                   self.second[1]) - (
                                    1 if (int(self.second[1]) - 1) % 3 == 0 else 0)
                                ) / 3)))

            # print("after", self.first, self.second)
            self.marks = (".".join(self.first), ".".join(self.second))
            # print(self.marks)
            self.text_hex.tag_add("selle", self.marks[0], self.marks[1])
            self.text_hex.tag_configure("selle", background=rgb(162, 8, 229), foreground="#ffffff")
            self.update_idletasks()
        except TclError:
            pass

    @staticmethod
    def _pround(r):
        if r > int(r):
            # print(r, int(r+1))
            return int(r) + 1
        else:
            # print(r, int(r), "else")
            return int(r)

    def _opposite_copy(self):
        self.after(20, self._opposite_copy)
        try:
            try:
                self.text.tag_configure("selle-hex", background="white", foreground="black")
                self.text.tag_delete("selle-hex")
            except TclError:
                pass
            self.hex_first, self.hex_second = self.text_hex.index(SEL_FIRST).split(".")[0] + "." + \
                                              str(int(self.text_hex.index(SEL_FIRST).split(".")[1]) * 3), \
                                              self.text_hex.index(SEL_LAST).split(".")[0] + "." + \
                                              str(int(self.text_hex.index(SEL_LAST).split(".")[1]) * 3 - 1)

            self.text.tag_add("selle-hex", self.hex_first, self.hex_second)
            self.text.tag_configure("selle-hex", background=rgb(229, 139, 8), foreground="#ffffff")
            self.update_idletasks()

        except TclError:
            pass


class Interface:
    def __init__(self, master):
        pass


if __name__ == '__main__':
    print(Main.__doc__)
    print('!.!')
    Main().mainloop()
