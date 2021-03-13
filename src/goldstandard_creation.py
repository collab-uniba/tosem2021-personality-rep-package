"""
This module creates the gold standard for the benchmarking. It takes care of anonymizing the content and the senders
"""
import json

from utils.email import email_utils

if __name__ == '__main__':
    email_list, hashed_email_list = email_utils.hash_score_email_addresses()
    corpus_dict = email_utils.get_mail_corpus()

    hashed_corpus_dict = dict()
    i = 1
    for email in email_list:
        hashed_email = hashed_email_list[i-1]
        if email in corpus_dict.keys():
            hashed_corpus_dict[hashed_email] = list(corpus_dict[email])
        i += 1

    with open(file="dataset/goldstandard/mailcorpus-sha.json", mode="w") as f:
        f.write(json.dumps(hashed_corpus_dict, indent=4))
