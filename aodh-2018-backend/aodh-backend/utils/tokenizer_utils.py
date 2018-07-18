from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
from many_stop_words import get_stop_words
import re

from utils.regex import regexEnJa
from api.google_api import detect_language_code

# en
from ekphrasis.classes.segmenter import Segmenter
seg_tw = Segmenter(corpus="twitter")

# ja
import JapaneseTokenizer
mecab_wrapper = JapaneseTokenizer.MecabWrapper(dictType='ipadic')


# tokenization for japanese
def mecab_tokenize(text):
    # with JapaneseTokenizer (https://pypi.org/project/JapaneseTokenizer/)
    global mecab_wrapper
    words = mecab_wrapper.tokenize(text).convert_list_object()
    return words


# tokenization for hashtags (twitter corpora)
# word segmentation fpr hashtags
def twitter_subtokenize(text):
    # with ekphrasis (https://github.com/cbaziotis/ekphrasis)
    global seg_tw
    words = seg_tw.segment(text)
    return words


def english_tokenize(text, subtokenize=True):
    words = word_tokenize(text.lower())
    output = []
    if subtokenize:
        for w in words:
            segments = twitter_subtokenize(w)
            subwords = word_tokenize(segments)
            output.extend(subwords)
    return output


def tokenize_and_normalize_sentences(sentence, language=None, clean_http=True, debug=False):
    stemmer = LancasterStemmer()

    regex_set = regexEnJa().regex_en_ja_characters_set(whitespace=True, tabs_newlines=False, url=True)

    matches = re.finditer(regex_set, sentence, re.MULTILINE | re.IGNORECASE | re.VERBOSE | re.UNICODE)
    matches = [match.group() for match in matches]

    if debug:
        print('all matches')
        print(matches)

    if clean_http:
        matches = [x for x in matches if 'http' not in x]

    s = ''.join(matches)

    if debug:
        print('from: ', '<start>' + sentence + '<end>')
        print('='*100)
        print('to:   ', '<start>' + s + '<end>')
        print('')

    if language:
        lang_code = language
    else:
        lang_code = detect_language_code(sentence)

    # set ignored words (overly common words)
    # tokenize words
    if lang_code == 'en':
        ignore_words = set(stopwords.words('english'))  # english
        # nltk's word_tokenize for english
        words = english_tokenize(s)
    elif lang_code == 'ja':
        ignore_words = get_stop_words(lang_code)  # has japanese
        words = mecab_tokenize(s)
        # clean blanks (japanese only)
        words = [w for w in words if w is not ' ']
    else:
        # todo: handle other languages properly
        # currently using english tokenizer as stand in
        ignore_words = set(stopwords.words('english'))  # english
        # nltk's word_tokenize for english
        words = english_tokenize(s)

    root_words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]

    return root_words


if __name__ == '__main__':
    def test():
        test_tweet_ja = u"""
        ＼浦ちゃんの家大ぼしゅう／

        浦ちゃんの家のデザイン･アイデア募集中！
        完成したらCMに登場するかも！？

        6/19(火)までに、 #浦ちゃんの家つくろう をつけて投稿しよう♪
        http://pnw-b.ctx.ly/r/607gu 
        """

        t = tokenize_and_normalize_sentences(test_tweet_ja, language='ja', debug=True)
        print(t)
        [print(x) for x in t]

        test_tweet_en = "📸 We are working hard on editing videos and we'll start publishing this week. Meanwhile, enjoy amazing pictures from the conference made by our great volunteers."
        test_tweet_en2 = "The #big COW’s JuMp!!!"

        t = tokenize_and_normalize_sentences(test_tweet_en, language='en', debug=True)
        print(t)
        [print(x) for x in t]

        test_tweet_en3 = "asachildithought"

        t = tokenize_and_normalize_sentences(test_tweet_en3, language='en', debug=True)
        print(t)
        [print(x) for x in t]


    test()


    def test2():
        test_tweet_en = "asachildithought"
        test_tweet_en2 = "AsAChildIThought"
        test_tweet_en3 = "WakeUpAmerica"

        print(twitter_subtokenize(test_tweet_en))
        print(twitter_subtokenize(test_tweet_en2))
        print(twitter_subtokenize(test_tweet_en3))

    def test3():
        test_tweet_en = "horribleday with crappyhair WakeUpAmerica"

        print(english_tokenize(test_tweet_en))

    #test3()