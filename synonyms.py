from thesaurus import Word
from Queue import Queue


class Color:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    USED = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def flatten(lst):
    items = set()
    q = Queue()
    q.put(lst)
    while not q.empty():
        cur_lst = q.get()
        if type(cur_lst) != list:
            items.add(str(cur_lst))
            continue
        for item in cur_lst:
            q.put(item)
    return items


def main(include_file, exclude_file, relevance=[3], length=[1], parts_of_speech=[]):
    with open(include_file) as file:
        words = set(file.read().splitlines())
    with open(exclude_file) as file:
        exclude = set(file.read().splitlines())

    word_objects = map(lambda w: Word(w), list(words))

    syns = map(lambda w: w.synonyms(
        'all',
        relevance=relevance,
        length=length,
        partsOfSpeech=parts_of_speech
    ), word_objects)

    synonyms = flatten(syns)
    good = set(words)
    new = synonyms - good - exclude
    with open('new-words.txt', 'w') as file:
        for s in new:
            print(s)
        file.write('\n'.join(list(new)))

    print Color.USED + ' '.join(good) + Color.END


if __name__ == '__main__':
    main('good-words.txt', 'bad-words')
