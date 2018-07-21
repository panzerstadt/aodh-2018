from gensim.models import KeyedVectors
from utils.baseutils import get_filepath
import os


def load_word2vec_model_read_only(model_filepath):
    wv_model = KeyedVectors.load(model_filepath)
    return wv_model


try:
    read_only_model_path = 'aodh-backend/db/w2v/word2vec_readonly.model'
    read_only_model_path = os.path.join(os.getcwd(), read_only_model_path)
    model = load_word2vec_model_read_only(get_filepath(read_only_model_path))
except SystemError:
    read_only_model_path = '/db/w2v/word2vec_readonly.model'
    read_only_model_path = os.path.join(os.getcwd(), read_only_model_path)
    model = load_word2vec_model_read_only(get_filepath(read_only_model_path))
except:
    print('Windows system error')


def similarity(word1=u'女', word2=u'バナナ', debug=False):
    try:
        results = model.similarity(word1, word2)
    except KeyError:
        results = 9999
    if debug:
        print('(cosine) word similarity between {} and {}: '.format(word1, word2))
        print(results)
        print('')
    return results


def closer_than(word1=u'女', word2=u'母', debug=False):
    results = model.closer_than(word1, word2)
    if debug:
        print('words more similar to {} than {}'.format(word1, word2))
        if len(results) >= 10:
            [print(r) for r in results[:10]]
            print('...continued {}'.format(len(results)))
        else:
            [print(r) for r in results]
        print('')
    return results


def distance(word1=u'女', word2=u'母', debug=False):
    try:
        result = model.distance(word1, word2)
    except KeyError:
        result = 9999
    if debug:
        print('a "distance" measurement between words {} and {}:'.format(word1, word2))
        print(result)
        print('')
    return result


def distance_pair_with_entities(word_to_entities_list_tuple=(u'母', [u'王子', u'男', u'バナナ']), debug=False):
    """
    tuple unpacked inside function (so that map() can be used)
    :param word_to_entities_list_tuple:
    :return:
    """
    tweet_word = word_to_entities_list_tuple[0]
    entities_to_measure = word_to_entities_list_tuple[1]

    distance_list = [distance(tweet_word, x) for x in entities_to_measure]

    if debug:
        print('distance of entities to this word: {}'.format(tweet_word))
        [print('{} : {}'.format(entities_to_measure[i], distance_list[i])) for i, _ in enumerate(entities_to_measure)]

    return distance_list


def get_vector(word_input, debug=False):
    try:
        results = model.get_vector(word_input)
    except KeyError:
        results = 9999
    if debug:
        print('the "numerical" values representing the word {}'.format(word_input))
        print(results)
        print(len(results))
        print('')
    return results


def most_similar(list_of_words, how_many=10, debug=False):
    results = model.most_similar(list_of_words, topn=how_many)
    if debug:
        print('the most similar words from a list: {}'.format(list_of_words))
        [print(r) for r in results]
        print('')
    return results


def compare(positive=[u'王子', u'男'], negative=[u'男'], how_many=10, debug=False):
    results = model.most_similar(positive=positive, negative=negative, topn=how_many)
    if debug:
        print('the {} word that are like {} but not like {}: '.format(how_many, positive, negative))
        print(results)
        print('')


if __name__ == '__main__':
    compare(debug=True)

    distance_pair_with_entities(debug=True)