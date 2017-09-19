import tkinter as tk
from PIL import ImageTk, Image

class ImageShower(tk.Frame):
    def __init__(self, source_file, target_file, master=None):
        tk.Frame.__init__(self, master)
        self.source_file = source_file
        self.target_file = target_file


        self.pack()
        self.createWidgets()

    def createWidgets(self):

        left_image =Image.open(self.source_file)
        left_image = left_image.resize((300, 250), Image.ANTIALIAS)
        left = ImageTk.PhotoImage(left_image)

        self.panel = tk.Label(self.master, image = left, height=400, width=350)
        self.panel.left = left
        self.panel.pack(side = "left", fill = "both", expand = "yes")


        right_image = Image.open(self.target_file)
        right_image = right_image.resize((300, 250), Image.ANTIALIAS)
        right = ImageTk.PhotoImage(right_image)

        self.panel = tk.Label(self.master, image = right, height = 400, width = 350)
        self.panel.right = right
        self.panel.pack(side = "right", fill = "both", expand = "yes")


        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.accept
        self.hi_there.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                                            command=self.master.destroy)
        self.QUIT.pack(side="bottom")



    def accept(self):
        print("hi there, everyone!")

