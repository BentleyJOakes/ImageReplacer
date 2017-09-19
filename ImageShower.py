import tkinter as tk
from PIL import ImageTk, Image
import os
from shutil import copyfile

class ImageShower(tk.Frame):
    def __init__(self, source_file, target_file):
        tk.Frame.__init__(self, tk.Tk())
        self.source_file = source_file
        self.target_file = target_file

        self.left_panel = None
        self.right_panel = None
        self.accept_button = None
        self.quit_button = None

        self.pack()
        self.createWidgets()

    def createWidgets(self):

        print("Comparing: " + self.source_file + " vs " + self.target_file)

        self.left_panel = self.make_image_panel(self.source_file)
        self.left_panel.pack(side = "left", fill = "both", expand = "yes")

        self.right_panel = self.make_image_panel(self.target_file)
        self.right_panel.pack(side = "right", fill = "both", expand = "yes")

        left_size = self.get_image_size(self.source_file)
        right_size = self.get_image_size(self.target_file)

        file_sizes = tk.Label(self.master, text = left_size + " vs " + right_size)
        file_sizes.pack(side="top")

        self.accept_button = tk.Button(self)
        self.accept_button["text"] = "Accept"
        self.accept_button["command"] = self.accept
        self.accept_button.pack(side="left")

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="right")

    def make_image_panel(self, image_file):
        image = Image.open(image_file)
        image = image.resize((300, 250), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)

        panel = tk.Label(self.master, image = photo_image, height = 400, width = 350)
        panel.image = photo_image
        return panel

    def get_image_size(self, image_file):
        s = os.path.getsize(image_file)
        s //= 1000
        return str(s) + " KB"


    def accept(self):
        print(self.target_file + " replaces " + self.source_file)
        os.rename(self.target_file, self.target_file + ".backup")
        copyfile(self.source_file, self.target_file)

        self.master.destroy()

