from google.cloud import translate

class RoundTrip:
    def __init__(self, project_id='moonlit-haven-256102'):
        self.client = translate.TranslationServiceClient()
        self.parent = self.client.location_path(project_id, "global")

    def back_translate_string(self, text: str, source_language='en-US', target_language='es'):
        """
        Source language is the language that the original text is in,
        Target language is the intermediate language before it's translated back to source
        """
        translation = self.client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type='text/plain',
            target_language_code=target_language,
            source_language_code=source_language,
        )
        text = translation.translations[0].translated_text
        back = self.client.translate_text(
            parent=self.parent,
            contents=[text],
            mime_type='text/plain',
            target_language_code=source_language,
            source_language_code=target_language,
        )
        return back.translations[0].translated_text

    def back_translate_batch(self, text_list: list(), source_language='en-US', target_language='es'):
        """
        Source language is the language that the original text is in,
        Target language is the intermediate language before it's translated back to source
        """
        # remove all empty strings from the text_list
        list(filter(lambda a: a != '', text_list))
        translation = self.client.translate_text(
            parent=self.parent,
            contents=text_list,
            mime_type='text/plain',
            target_language_code=target_language,
            source_language_code=source_language,
        )
        text_list = [t.translated_text for t in translation.translations]
        back = self.client.translate_text(
            parent=self.parent,
            contents=text_list,
            mime_type='text/plain',
            target_language_code=source_language,
            source_language_code=target_language,
        )
        return [t.translated_text for t in back.translations]

    def back_translate_file(self, file_path, source_language='en-US', target_language='es'):
        with open(file_path) as f:
            file_text = [line.strip() for line in f.readlines()]
        return self.back_translate_batch(file_text, source_language, target_language)

if __name__ == '__main__':
    from sys import stdin
    translator = RoundTrip()
    for line in stdin:
        print(translator.back_translate_string(line.strip()))