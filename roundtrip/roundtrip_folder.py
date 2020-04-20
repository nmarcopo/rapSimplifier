from translate import RoundTrip
from os import walk
from multiprocessing import Pool

def send_output_to_file(file_name):
    global translator
    global lyrics_dir
    # get translation
    result = translator.back_translate_file(file_name)

    # send the translated results to a new directory
    file_name = file_name.replace(lyrics_dir, 'lyrics_backtranslated/') + '.backtranslated'
    result = [r + '\n' for r in result]
    with open(file_name, 'w') as f:
        f.writelines(result)
    return f"written file {file_name}"

if __name__ == '__main__':
    global translator
    translator = RoundTrip()
    num_processes = 10
    global lyrics_dir
    lyrics_dir = 'lyrics_test/'
    (_, _, file_names) = next(walk(lyrics_dir))
    # add the directory to file names
    file_names = [lyrics_dir + f for f in file_names]
    tasks = []

    # multiprocessing for getting translations faster
    p = Pool(num_processes)
    for response in p.imap_unordered(send_output_to_file, file_names):
        print(response)