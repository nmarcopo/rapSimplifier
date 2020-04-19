from translate import RoundTrip

translator = RoundTrip()
for line in translator.back_translate_file('thebox.txt', target_language='de'):
    print(line)