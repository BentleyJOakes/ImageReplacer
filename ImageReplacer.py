import os
import imagehash
import collections

from PIL import Image

import configparser

class ImageCopier:

    def __init__(self, source_dirs, target_dirs):
        self.source_dirs = source_dirs
        self.target_dirs = target_dirs

        self.source_hashes = None
        self.target_hashes = None

    def compare_images(self):

        print("Compare images...")

        print("Source dirs: " + str(self.source_dirs))
        print("Target dirs: " + str(self.target_dirs))

        for source_dir in self.source_dirs:
            self.source_hashes = self.hash_dir(source_dir)

            for target_dir in self.target_dirs:
                self.target_hashes = self.hash_dir(target_dir)

                self.compare_hashes()


    def hash_dir(self, d):
        hash_dict = collections.defaultdict(list)

        print("Hashing directory: " + d)
        files = sorted(os.listdir(d))
        for index, f in enumerate(files):
            i_filename = os.path.join(d, f)
            i = Image.open(i_filename)
            h = imagehash.average_hash(i)
            #print(h)
            print(index/len(files))

            hash_dict[h].append(f)

        return hash_dict

    def compare_hashes(self):
        for k in self.source_hashes.keys():
            if k in self.target_hashes.keys():
                print("Found match")

                print(self.source_hashes[k])

                # for v in self.source_hashes[k]:
                #     print(v[0])
                # for v in self.target_hashes[k]:
                #     print(v[0])


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.cfg')

    s_dirs = config.get('ImageReplacer', 'source_dirs')
    t_dirs = config.get('ImageReplacer', 'target_dirs')

    s_dirs = [os.path.expanduser(v.strip()) for v in s_dirs.split()]
    t_dirs = [os.path.expanduser(v.strip()) for v in t_dirs.split()]

    ic = ImageCopier(s_dirs, t_dirs)
    ic.compare_images()