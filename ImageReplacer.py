import os
import imagehash
import collections

from PIL import Image

import configparser

class ImageCopier:

    def __init__(self, source_dirs, target_dirs):
        self.source_dirs = source_dirs
        self.target_dirs = target_dirs

        self.source_hashes = collections.defaultdict(list)
        self.target_hashes = collections.defaultdict(list)

    def hash_images(self):

        self.hash_dir(self.source_dirs, self.source_hashes)
        self.hash_dir(self.target_dirs, self.target_hashes)


    def hash_dir(self, dirs, file_dict):

        for d in dirs:
            files = sorted(os.listdir(d))
            for l, f in enumerate(files):
                i_filename = os.path.join(d, f)
                i = Image.open(i_filename)
                h = imagehash.average_hash(i)
                #print(h)
                print(l/len(files))

                file_dict[h].append([f, i])

    def compare_images(self):
        for k in self.source_hashes.keys():
            if k in self.target_hashes.keys():
                print("Found match")

                for v in self.source_hashes[k]:
                    print(v[0])
                for v in self.target_hashes[k]:
                    print(v[0])


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.cfg')

    source_dirs = config.get('ImageReplacer', 'source_dirs')
    target_dirs = config.get('ImageReplacer', 'target_dirs')

    source_dirs = [v.strip() for v in source_dirs.split()]
    target_dirs = [v.strip() for v in target_dirs.split()]

    ic = ImageCopier(source_dirs, target_dirs)
    ic.hash_images()

    ic.compare_images()