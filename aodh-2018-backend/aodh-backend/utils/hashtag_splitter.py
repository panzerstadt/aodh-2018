"""
from: https://github.com/matchado/HashTagSplitter
todo: checkout google's tokenizer: https://github.com/google/sentencepiece

NOT USED CURRENTLY, CURRENTLY USING EKPHRASIS (in tokenizer_utils, twitter_subtokenizer()
"""
debug = False

import nltk
from nltk.corpus import words, brown
import re

from api.google_api import identify_entities

if debug:
    w = words.words()
    [print(x) for x in w]

word_dictionary = list(set(words.words()))

if debug:
    print('\n\n\n')
    [print(x) for x in word_dictionary]


for alphabet in "bcdefghjklmnopqrstuvwxyz":
    word_dictionary.remove(alphabet)

if debug:
    print('\n\n\n')
    [print(x) for x in word_dictionary]


def check_upper(text):
    for a in text:
        if a.isupper():
            return True
    return False


def split_by_uppercase(text):
    """
    https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters
    :param text:
    :return:
    """
    return re.findall('[A-Z][^A-Z]*', text)


# lowercase only
def split_hashtag_to_words_all_possibilities(hashtag):
    all_possibilities = []

    split_possibility = [hashtag[:i] in word_dictionary for i in reversed(range(len(hashtag)+1))]
    possible_split_positions = [i for i, x in enumerate(split_possibility) if x == True]

    for split_pos in possible_split_positions:
        split_words = []
        word_1, word_2 = hashtag[:len(hashtag)-split_pos], hashtag[len(hashtag)-split_pos:]

        if word_2 in word_dictionary:
            split_words.append(word_1)
            split_words.append(word_2)
            all_possibilities.append(split_words)

            another_round = split_hashtag_to_words_all_possibilities(word_2)

            if len(another_round) > 0:
                all_possibilities = all_possibilities + [[a1] + a2 for a1, a2, in zip([word_1]*len(another_round), another_round)]
        else:
            another_round = split_hashtag_to_words_all_possibilities(word_2)

            if len(another_round) > 0:
                all_possibilities = all_possibilities + [[a1] + a2 for a1, a2, in zip([word_1]*len(another_round), another_round)]

    return all_possibilities


# todo: when ready, place this on algorithmia
# todo: and store data permanently. every subsequent call for tokenization will update the database
def tokenize_english_hashtags(hashtags):
    # 1. call google api (cached results) to identify entities and split
    ordered_segmentation_dict = identify_entities(hashtags)

    position = segmentation_dict['positions']

    non_entities =

    # 2a. split by uppercase
    if check_upper(hashtags):
        return split_by_uppercase(hashtags)
    # 2b. split by maximum matching algorithm
    else:
        return split_hashtag_to_words_all_possibilities(hashtags)


if __name__ == '__main__':
    def test(text='WakeUpAmerica'):
        t = text
        result = split_hashtag_to_words_all_possibilities(t)
        print("{} -> {}".format(t,result))

    def test2(text="WakeUpAmerica"):
        t = text
        result = tokenize_english_hashtags(t)
        print("{} -> {}".format(t, result))

    test2()
    test2("theedgeofentertainment")
    test("wakeupamerica")

    def test3(text="WakeUpAmerica"):
        from nltk.tokenize import word_tokenize
        words = word_tokenize(text.lower())
        print("{} -> {}".format(text, words))

    test3()
    test3("wakeupamerica")
    test3("wake up america")

