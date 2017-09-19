import os
import imagehash
import collections

from PIL import Image

import configparser

from multiprocessing import Manager

from progress import ProgressBar

from ImageShowerProcess import ImageShowerProcess

class ImageReplacer:

    def __init__(self, source_dirs, target_dirs):
        self.source_dirs = source_dirs
        self.target_dirs = target_dirs

        self.source_hashes = None
        self.target_hashes = None

        self.manager = Manager()
        self.images_queue = self.manager.Queue()

        self.image_shower_process = ImageShowerProcess(self.images_queue)
        self.image_shower_process.start()

        self.image_filetypes = [".jpg", ".jpeg", ".png"]

    def compare_images(self):

        print("Comparing images...")
        print("Source dirs: " + str(self.source_dirs))
        print("Target dirs: " + str(self.target_dirs))

        for source_dir in self.source_dirs:
            self.source_hashes = self.hash_dir(source_dir)

            for target_dir in self.target_dirs:
                self.target_hashes = self.hash_dir(target_dir)

                self.compare_hashes()

        self.images_queue.put(None)

        self.image_shower_process.join()


    def hash_dir(self, d):
        hash_dict = collections.defaultdict(list)

        print("Hashing directory: " + d)

        files = sorted(os.listdir(d))

        pb = ProgressBar(len(files))
        for index, f in enumerate(files):

            if any([f.lower().endswith(x) for x in self.image_filetypes]):
                i_filename = os.path.join(d, f)
                i = Image.open(i_filename)
                h = imagehash.average_hash(i)
                #print(h)
                pb.update_progress(index)

                hash_dict[h].append(i_filename)

        return hash_dict

    def compare_hashes(self):
        hash_diff = 1

        for s_k in self.source_hashes.keys():

            for t_k in self.target_hashes.keys():

                if s_k - t_k > hash_diff:
                    continue

                self.images_queue.put((self.source_hashes[s_k], self.target_hashes[t_k]))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.cfg')

    s_dirs = config.get('ImageReplacer', 'source_dirs')
    t_dirs = config.get('ImageReplacer', 'target_dirs')

    s_dirs = [os.path.expanduser(v.strip()) for v in s_dirs.split()]
    t_dirs = [os.path.expanduser(v.strip()) for v in t_dirs.split()]

    ic = ImageReplacer(s_dirs, t_dirs)
    ic.compare_images()