import hashlib
import json
import os
import warnings

import rpy2.robjects as robjects
from bs4 import BeautifulSoup as Bs
from cleantext import clean
from email_reply_parser import EmailReplyParser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from polyglot.detect import Detector
from polyglot.detect.base import logger as polyglot_logger

from utils.email import nlon, nlon_model, punc

warnings.filterwarnings(action="ignore", category=UserWarning, module='bs4')
warnings.filterwarnings(action="ignore", message="bad escape \\? at position *")
polyglot_logger.setLevel("ERROR")

contractions = {
    "ain't": "am not / are not",
    "aren't": "are not / am not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had / he would",
    "he'd've": "he would have",
    "he'll": "he shall / he will",
    "he'll've": "he shall have / he will have",
    "he's": "he has / he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has / how is",
    "i'd": "I had / I would",
    "i'd've": "I would have",
    "i'll": "I shall / I will",
    "i'll've": "I shall have / I will have",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it had / it would",
    "it'd've": "it would have",
    "it'll": "it shall / it will",
    "it'll've": "it shall have / it will have",
    "it's": "it has / it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had / she would",
    "she'd've": "she would have",
    "she'll": "she shall / she will",
    "she'll've": "she shall have / she will have",
    "she's": "she has / she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as / so is",
    "that'd": "that would / that had",
    "that'd've": "that would have",
    "that's": "that has / that is",
    "there'd": "there had / there would",
    "there'd've": "there would have",
    "there's": "there has / there is",
    "they'd": "they had / they would",
    "they'd've": "they would have",
    "they'll": "they shall / they will",
    "they'll've": "they shall have / they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had / we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what shall / what will",
    "what'll've": "what shall have / what will have",
    "what're": "what are",
    "what's": "what has / what is",
    "what've": "what have",
    "when's": "when has / when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has / where is",
    "where've": "where have",
    "who'll": "who shall / who will",
    "who'll've": "who shall have / who will have",
    "who's": "who has / who is",
    "who've": "who have",
    "why's": "why has / why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had / you would",
    "you'd've": "you would have",
    "you'll": "you shall / you will",
    "you'll've": "you shall have / you will have",
    "you're": "you are",
    "you've": "you have"
}


def _remove_stopwords_nonenglish_punctuation(text):
    """
    In order to perform stop words removal,we the function word_tokenize which
    splits the original text into tokens. Using list comprehension we check if
    the word is a stop word or not.
    """
    token = word_tokenize(text)
    new_words = []
    for word in token:
        new_word = word.lower()
        new_words.append(new_word)
    tokens_without_sw = [word for word in new_words if not word.lower() in stopwords.words()]

    """Remove only words classified as 'undefined' ('un')"""
    english_tokens_without_sw = [word for word in tokens_without_sw if not _is_word_lang_undefined(word)]

    """
    We remove every punctuation mark with the exception of: 
    1.   Dots, since personality tools use dots to determine the number of sentences;
    2.   Exclamation marks, since they might be meaningful giving more strength to some traits.
    """
    new_words = [word for word in english_tokens_without_sw if not word in punc]
    return " ".join(new_words)


def _is_word_lang_undefined(word):
    detector = Detector(word, quiet=True)
    return detector.language.code == 'un'


def _clean_body(text):
    clean_message_body = clean(text, lang="en", fix_unicode=True, to_ascii=True, lower=True, no_urls=True,
                               no_emails=True, no_phone_numbers=True, no_numbers=True, no_digits=True,
                               no_currency_symbols=True, replace_with_url="http://replaced.url",
                               replace_with_email="replaced@email.addr.es", replace_with_phone_number="555-555-555",
                               replace_with_number="0", replace_with_digit="0", replace_with_currency_symbol="$")
    return clean_message_body


def _remove_lines_of_code(text):
    try:
        soup = Bs(text, 'html.parser')
        clean_message_body = soup.text.strip()
    except Exception as e:
        print("Warning: {} ".format(type(e)))
        clean_message_body = text.strip()
    message_by_lines = clean_message_body.splitlines()
    list_length = len(message_by_lines)
    index = 0
    for count in range(0, list_length):
        text_line = robjects.StrVector([message_by_lines[index]])
        if nlon.NLoNPredict(nlon_model, text_line)[0] == 'Not':
            del message_by_lines[index]
        else:
            index += 1
    clean_message_body = '\n'.join(message_by_lines)
    return clean_message_body.strip()


def hash_score_email_addresses():
    # plain text
    sha_addresses = list()
    path = os.path.join("dataset", "goldstandard", "address_list.txt")
    with open(file=path, mode='r') as f:
        addresses = [a.strip() for a in f.readlines()]
        for addr in addresses:
            sha_addr = hashlib.sha256(addr.strip().encode()).hexdigest()
            sha_addresses.append(sha_addr)

    path = os.path.join("dataset", "goldstandard", "address_list_sha.txt")
    with open(file=path, mode='w') as f:
        f.writelines("\n".join(sha_addresses))

    # json
    path = os.path.join("dataset", "goldstandard", "ipip-scores.json")
    with open(file=path, mode='r') as f:
        data = json.load(f)
        for d in data:
            sha_addr = hashlib.sha256(d['email'].strip().encode()).hexdigest()
            d['email'] = sha_addr
    path = os.path.join("dataset", "goldstandard", "ipip-scores-sha.json")
    with open(file=path, mode='w') as f:
        f.write(json.dumps(data, indent=4))

    return addresses, sha_addresses


def _remove_contractions(text):
    res = text
    for word in text.split():
        if word.lower() in contractions:
            res = res.replace(word, contractions[word.lower()])
    return res


def get_mail_corpus():
    # Path to mail corpus
    corpus_file = 'dataset/goldstandard/mailcorpus.json'
    with open(corpus_file) as data_file:
        corpus = json.load(data_file)

    print('Reading and cleaning emails corpus. Number of emails: ' + str(len(corpus)))
    _dict = {}
    n = 0
    # Text cleaning
    for d in corpus:
        try:
            res = EmailReplyParser.read(d['message_body'].replace('\\n', '\n'))
            message_body = EmailReplyParser.parse_reply(res.text)
            n += 1

            clean_message_body = _remove_contractions(message_body)
            clean_message_body = _remove_lines_of_code(clean_message_body)
            clean_message_body = _remove_stopwords_nonenglish_punctuation(clean_message_body)
            clean_message_body = _clean_body(clean_message_body)

            if not clean_message_body == '':
                if d['email_address'] in _dict:
                    _dict[d['email_address']].add(clean_message_body)
                else:
                    _dict[d['email_address']] = {clean_message_body}
            print(str(n) + '/' + str(len(corpus)) + '\n' if n % 50 == 0 else '', end='')
        except Exception as e:
            print(e)
            continue

    print('Mails retrieved: ' + str(n))
    print('Email addresses: ' + str(len(_dict)))
    return _dict
