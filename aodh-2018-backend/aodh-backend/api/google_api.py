#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, six, os
import os.path as path
# Imports the Google Cloud client library
from google.cloud import translate, language
from google.cloud.language import enums, types
import googlemaps

from utils.db_utils import load_db, update_db
from utils.baseutils import get_filepath
import os.path as path

# analyzed entities cache
try:
    db_dir = "db"
    sentiment_db_filename = "sentiment-cache.json"
    sentiment_db_filepath = get_filepath(path.join(db_dir, sentiment_db_filename))
except:
    db_dir = "aodh-backend/db"
    sentiment_db_filename = "sentiment-cache.json"
    sentiment_db_filepath = get_filepath(path.join(db_dir, sentiment_db_filename))

sentiment_db = load_db(database_path=sentiment_db_filepath, debug=False)

from hidden.hidden import GoogleAPI
API_KEY = GoogleAPI().api_key

def translate_text_api(text='', target='ja', debug=False):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    if debug:
        try:
            print(u'Text: {}'.format(result['input']))
            print(u'Translation: {}'.format(result['translatedText']))
            print(u'Detected source language: {}'.format(
                result['detectedSourceLanguage']))
        except:
            pass

    return result


def translate_text(text='', target='ja', debug=False):
    from utils.baseutils import get_filepath
    from utils.db_utils import load_db, update_db
    db_dir = "/db"

    if target == 'ja':
        db_filename = "translation-to-ja-cache.json"
    elif target == 'en':
        db_filename = "translation-to-en-cache.json"
    else:
        raise SystemError('no translation cache defined. define one before proceeding.')

    db_filepath = get_filepath(path.join(db_dir, db_filename))

    db_keyword_pair = load_db(database_path=db_filepath, debug=debug)
    try:
        output = db_keyword_pair[text]
        if debug: print('local keyword pair found!')
        return output
    except KeyError:
        if debug: print('calling google translate to translate (will only happen once per word)')
        response = translate_text_api(text=text, target=target, debug=debug)
        output = response['translatedText']
        db_keyword_pair[text] = output
        update_db(db_keyword_pair, database_path=db_filepath)
        return output


def detect_language_api(text, debug=False):
    """Detects the text's language.
    :returns ISO compatible language
    """
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    if debug:
        print('Text: {}'.format(text))
        print('Confidence: {}'.format(result['confidence']))
        print('Language: {}'.format(result['language']))
    return result


def detect_language_code(text):
    return detect_language_api(text)['language']


def analyze_entities_api(text='', verbose=False):
    """
    ref: https://cloud.google.com/natural-language/docs/reference/rpc/google.cloud.language.v1#google.cloud.language.v1.AnalyzeEntitiesResponse
    name:
          The representative name for the entity.
    type:
          The entity type.
    metadata:
          Metadata associated with the entity.  Currently, Wikipedia
          URLs and Knowledge Graph MIDs are provided, if available. The
          associated keys are "wikipedia\_url" and "mid", respectively.
    salience:
          The salience score associated with the entity in the [0, 1.0]
          range.  The salience score for an entity provides information
          about the importance or centrality of that entity to the
          entire document text. Scores closer to 0 are less salient,
          while scores closer to 1.0 are highly salient.
    mentions:
          The mentions of this entity in the input document. The API
          currently supports proper noun mentions.
    sentiment:
          For calls to [AnalyzeEntitySentiment][] or if [AnnotateTextReq
          uest.Features.extract\_entity\_sentiment][google.cloud.languag
          e.v1.AnnotateTextRequest.Features.extract\_entity\_sentiment]
          is set to true, this field will contain the aggregate
          sentiment expressed for this entity in the provided document.

    :param document:
    :param verbose:
    :return: (entity.name, entity.type)
    """
    """Detects entities in the text."""
    text = text.lower()  #apparently entity search fails if there are capitals

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    # TODO: specify only entities that we are interested in finding?
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    # is it a full name, or a common noun?
    entity_mention_type = ('TYPE_UNKNOWN', 'PROPER', 'COMMON')

    list_of_entities = []
    # todo: key entry by relevance or by entity name!?
    for entity in entities:
        list_of_entities.append({
            entity.name: {
                "entity salience": entity.salience,
                "entity type": entity_type[entity.type]
            }
        })
        #list_of_entities.append((entity.name, entity_type[entity.type], '{:.2f}'.format(entity.salience)))

    return list_of_entities


# sentiment of entire content
def analyze_sentiment_api(text=''):
    """
    Detects the sentiment of the text
    https://cloud.google.com/natural-language/docs/analyzing-sentiment

    Detects sentiment in the document. You can also analyze HTML with:
    document.type == enums.Document.Type.HTML

    outpus score and magnitude
    The score of a document's sentiment indicates the overall emotion of a document.
    The magnitude of a document's sentiment indicates how much emotional content is present within the document,
    and this value is often proportional to the length of the document.

    TLDR:
    deifne your own threshold of what's strong emotion, then measure from there
    score = (- bad, + good, 0.0 either low emotion or mixed emotions)
    magnitude = (emotion / length of content) (how strong is the emotion in the content?)
    to find low emotions:
    if score = low, magnitude = low, emotion = low
    if score = low, magnitude = hight, emotion = mixed
    when comparing content of different length, use magnitude to normalize scores
    :param text:
    :param explicit_credentials:
    :return:
    """

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text,
        language='ja',
        type=enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document=document).document_sentiment

    """
    It is important to note that the Natural Language API indicates differences between 
    positive and negative emotion in a document, but does not identify specific positive and negative emotions. 
    For example, "angry" and "sad" are both considered negative emotions. However, when the Natural Language API 
    analyzes text that is considered "angry", or text that is considered "sad", the response only indicates that 
    the sentiment in the text is negative, not "sad" or "angry".

    A document with a neutral score (around 0.0) may indicate a low-emotion document, or may indicate mixed emotions, 
    with both high positive and negative values which cancel each out. Generally, you can use magnitude values to 
    disambiguate these cases, as truly neutral documents will have a low magnitude value, while mixed documents 
    will have higher magnitude values.

    When comparing documents to each other (especially documents of different length), make sure to use the 
    magnitude values to calibrate your scores, as they can help you gauge the relevant amount of emotional content.
    """

    return sentiment


def analyze_sentiment(text='', debug=True):
    global sentiment_db

    db_entities_cache = sentiment_db
    db_filepath = sentiment_db_filepath

    try:
        output = db_entities_cache[text]
        if debug: print('entity previously analysed. returning cache')
        return output
    except KeyError:
        if debug: print('calling google API to analyze entities')
        response = analyze_sentiment_api(text=text)
        output = response.score
        print('sentiment {} -> {}'.format(text, output))
        db_entities_cache[text] = output
        update_db(db_entities_cache, database_path=db_filepath)

        # reload the variable 'entities_db' if updated
        sentiment_db = load_db(database_path=sentiment_db_filepath, debug=False)
        return output


def parse_entities(text='', debug=False):
    """
    entity level parsing
    :param text:
    :param debug:
    :return:
    """
    from utils.baseutils import get_filepath
    from utils.db_utils import load_db, update_db
    db_dir = "/db"
    db_filename = "entity-cache.json"

    db_filepath = get_filepath(path.join(db_dir, db_filename))

    db_keyword_pair = load_db(database_path=db_filepath, debug=debug)
    try:
        output = db_keyword_pair[text]
        if debug: print('local keyword pair found!')
        return output
    except KeyError:
        if debug: print('calling google translate to translate (will only happen once per word)')
        response = analyze_entities_api(text)
        print(response)
        raise
        response = translate_text_api(text=text, target=target, verbose=debug)
        output = response['translatedText']
        db_keyword_pair[text] = output
        update_db(db_keyword_pair, database_path=db_filepath)
        return output


def get_places(query="Osaka"):
    # 2 fallbacks
    # if places returns nothing, try parsing entities
    gmaps = googlemaps.Client(key=API_KEY)

    response = gmaps.find_place(query, input_type='textquery')
    candidates = response['candidates']

    candidate_output = []
    for c in candidates:
        place = gmaps.place(place_id=c['place_id'])
        candidate_output.append(place)
    return candidate_output


def get_coordinates_from_places(query='Osaka'):
    places_list = get_places(query=query)

    candidate_coords = []
    for x in places_list:
        try:
            coords = x['result']['geometry']['location']
            candidate_coords.append(coords)
        except:
            return {}

    if len(candidate_coords) == 1:
        return candidate_coords[0]
    elif len(candidate_coords) < 1:
        return {}
    else:
        print('found multiple places for {}'.format(query))
        [print(x) for x in candidate_coords]
        raise SystemError('to be implemented: average? over coords')


def get_geocode(query='Osaka', with_bounds=False):
    gmaps = googlemaps.Client(key=API_KEY)

    response = gmaps.geocode(query)
    if len(response) > 1:
        [print(x) for x in response]
        raise
    location = response[0]['geometry']


    output = {}
    if with_bounds:
        try:
            output['bounds'] = location['bounds']
        except:
            print('no bounds found. coord might be a shop.')
    output['location'] = location['location']

    return output


def get_coordinates_from_geocode(query='Osaka'):
    response = get_geocode(query=query)
    return response['location']


if __name__ == '__main__':
    # translate_text("fathers day", debug=True)
    # translate_text("japan", debug=True)
    # detect_language_api('弟')
    # parse_entities("wakeupamerica")
    # parse_entities("america makes us strong like teeth")

    print(json.dumps(get_coordinates_from_geocode('東京 holiday'), indent=4, ensure_ascii=False))
    print(json.dumps(get_coordinates_from_geocode('兵庫県尼崎市'), indent=4, ensure_ascii=False))


