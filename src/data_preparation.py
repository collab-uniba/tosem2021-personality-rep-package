"""
This module transforms the corpus into the format require by each benchmarked tool
"""

import json

CORPUS_PATH = 'dataset/goldstandard/mailcorpus-sha.json'


def liwc(senders, data):
    ds = dict()
    for hashed_addr in senders:
        try:
            emails = '. '.join(data[hashed_addr])
            ds[hashed_addr] = emails
        except KeyError:
            continue
    with open(file="dataset/LIWC/dataset.csv", mode='w') as csv_file:
        for key in ds:
            csv_file.write("\"\"\"{}\"\"\",\"\"\"{}\"\"\"\n".format(key, ds[key]))


def personality_recognizer(senders, data):
    for hashed_addr in senders:
        try:
            emails = '. '.join(data[hashed_addr])
            with open("dataset/PersonalityRecognizer/data/{}.txt".format(hashed_addr), 'w') as f:
                f.write("%s\n" % emails)
        except KeyError:
            continue


if __name__ == '__main__':
    """
    The file mailcorpus-sha.json contains the emails written by the developers.
    """
    with open(CORPUS_PATH, encoding="utf-8") as f:
        email_corpus = json.load(f)

    """
    Here we retrieve the list of developers to perform the emails merging. 
    """
    with open(file="dataset/goldstandard/address_list_sha.txt", mode="r") as f:
        hashed_senders = [line.strip() for line in f.readlines()]

    liwc(hashed_senders, email_corpus)
    personality_recognizer(hashed_senders, email_corpus)
