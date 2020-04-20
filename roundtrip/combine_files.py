from shutil import copyfileobj
from glob import glob
from tqdm import tqdm

def combine(outfilename, parent_dir, lyrics_dir, suffix):
    with open(outfilename, 'wb') as outfile:
        for filename in tqdm(sorted(glob(parent_dir + lyrics_dir + '*' + suffix))):
            if filename == outfilename:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                copyfileobj(readfile, outfile)

if __name__ == "__main__":
    combine('combined_lyrics.txt', '../data/', 'english/', '.txt')
    combine('combined_backtranslated.txt', '../data/', 'lyrics_backtranslated/', '.backtranslated')