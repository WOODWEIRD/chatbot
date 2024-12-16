from googletrans import Translator

translator = Translator()

def translate_input(user_input, target_language='en'):
    return translator.translate(user_input, dest=target_language).text

def translate_output(response, target_language='auto'):
    return translator.translate(response, dest=target_language).text
