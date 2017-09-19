from multiprocessing import Process
import tkinter as tk

class ImageShowerProcess(Process):

    def __init__(self, images_queue):
        super(ImageShowerProcess, self).__init__()
        self.images_queue = images_queue

        self.root = tk.Tk()

    def run(self):

        print("Starting image shower worker...")

        while True:

            images = self.images_queue.get()

            if images is None:
                break

            source_image, target_image = images
            print("Worker: " + str(source_image))

    def build_comparison(self, source_file, target_file):

        img_shower = ImageShower(source_file, target_file, master = self.root)
        img_shower.mainloop()

        raise Exception()