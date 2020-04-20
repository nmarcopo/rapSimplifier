from os import walk
from sys import stderr
from mmap import mmap
import argparse
from tqdm import tqdm

def get_file_lines(file_path):
    with open(file_path, 'r+') as f:
        try:
            buf = mmap(f.fileno(), 0)
        except ValueError:
            return 0
        lines = 0
        readline = buf.readline
        # while True:
        #     x = readline()
        #     if len(x) == 0:
        #         break
        #     lines += 1
        #     print(x, lines)
        while readline():
            lines += 1
        return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    debug = parser.parse_args().debug

    lyrics_parent_dir = '../data/'
    lyrics_backtranslated_dir = 'lyrics_backtranslated/'
    lyrics_dir = 'english/'

    try:
        (_, _, file_names) = next(walk(lyrics_parent_dir + lyrics_backtranslated_dir))
    except StopIteration:
        print(f"Error, make sure directory {lyrics_parent_dir + lyrics_backtranslated_dir} exists.", file=stderr)
        exit(1)

    print("Getting line numbers for translated...")
    file_names_and_lines = {fname : get_file_lines(lyrics_parent_dir + lyrics_backtranslated_dir + fname) for fname in tqdm(file_names)}

    file_names = [fname.replace('.backtranslated', '') for fname in file_names]
    print("Comparing with line numbers in original...")
    for fname in tqdm(file_names):
        n_lines = get_file_lines(lyrics_parent_dir + lyrics_dir + fname)
        if file_names_and_lines[fname + '.backtranslated'] != n_lines:
            print(f"Error, {fname} + backtranslation have different line counts: {file_names_and_lines[fname + '.backtranslated']}, {n_lines}", file=stderr)
        else:
            if debug:
                print(f"No problems here, {file_names_and_lines[fname + '.backtranslated']}, {n_lines}")
