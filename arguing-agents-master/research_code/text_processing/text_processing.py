import re

def prepare_text(text):
    text = text.replace('\t', ' ').replace('\n', ' ')
    text = re.sub(r' +', ' ', text)
    text = text.strip(' ')

    return text

def split_into_sentences(text):
    sentences = []

    parts = re.split(r'([\.\?\!]) \s*(?![^()]*\))', text)

    for i in range(len(parts))[::2]:
        sentence = parts[i]

        if i + 1 < len(parts):
            sentence += parts[i + 1]

        sentence = sentence.strip()

        if sentence == '':
            continue

    return sentences

def get_words(text):
    text = prepare_text(text)
    return [word.strip(' ,.-!') for word in text.split(' ')]