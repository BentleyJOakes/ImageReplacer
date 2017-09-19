from multiprocessing import Process


from ImageShower import ImageShower

import hashlib

class ImageShowerProcess(Process):

    def __init__(self, images_queue):
        super(ImageShowerProcess, self).__init__()
        self.images_queue = images_queue


    #
    # def __del__(self):
    #     print("Shutting down image shower worker...")

    def run(self):

        #print("Starting image shower worker...")

        while True:

            images = self.images_queue.get()

            if images is None:
                break

            source_images, target_images = images


            for v1 in source_images:
                for v2 in target_images:

                    hash1 = self.get_hash(v1)
                    hash2 = self.get_hash(v2)
                    if not hash1.hexdigest() == hash2.hexdigest():

                        img_shower = ImageShower(v1, v2)
                        img_shower.mainloop()


    def get_hash(self, image_file):
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()

        with open(image_file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break

                md5.update(data)

        return md5
