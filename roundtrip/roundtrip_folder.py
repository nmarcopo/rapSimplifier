from translate import RoundTrip
from os import walk
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
from sys import stderr, exit

def send_output_to_file(file_name):
    global translator
    global lyrics_dir
    global lyrics_parent_dir
    global lyrics_backtranslated_dir
    # get translation
    result = translator.back_translate_file(file_name)

    # send the translated results to a new directory
    file_name = file_name.replace(lyrics_dir, lyrics_backtranslated_dir) + '.backtranslated'
    result = [r + '\n' for r in result]
    with open(file_name, 'w') as f:
        f.writelines(result)
    return f"written file {file_name}"

if __name__ == '__main__':
    global translator
    translator = RoundTrip()
    num_threads = 10
    global lyrics_dir
    lyrics_dir = 'english/'
    global lyrics_parent_dir
    lyrics_parent_dir = '../data/'
    global lyrics_backtranslated_dir
    lyrics_backtranslated_dir = 'lyrics_backtranslated/'
    try:
        (_, _, file_names) = next(walk(lyrics_parent_dir + lyrics_dir))
    except StopIteration:
        print(f"Error, make sure directory {lyrics_parent_dir + lyrics_dir} exists.", file=stderr)
        exit(1)

    # add the directory to file names if they haven't already been translated
    try:
        (_, _, backtranslated_file_names) = next(walk(lyrics_parent_dir + lyrics_backtranslated_dir))
    except StopIteration:
        print(f"Error, make sure directory {lyrics_parent_dir + lyrics_backtranslated_dir} exists.", file=stderr)
        exit(1)
    file_names = [lyrics_parent_dir + lyrics_dir + f for f in file_names if f + '.backtranslated' not in backtranslated_file_names]
    if len(file_names) == 0:
        print("No files to translate. Are all of your files already translated?", file=stderr)
        exit(1)
    tasks = []

    # multiprocessing for getting translations faster
    p = ThreadPool(num_threads)
    for response in tqdm(p.imap_unordered(send_output_to_file, file_names), total=len(file_names)):
        print(response)