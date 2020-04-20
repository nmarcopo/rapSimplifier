from shutil import copyfileobj
from glob import glob

def combine(outfilename):
    with open(outfilename, 'wb') as outfile:
        for filename in glob('lyrics_backtranslated/*.backtranslated'):
            if filename == outfilename:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                copyfileobj(readfile, outfile)

if __name__ == "__main__":
    combine('combined_backtranslated.txt')