#  Copyright (c) 2023 Robert Bosch GmbH
#  SPDX-License-Identifier: AGPL-3.0
import hydra
import nltk
from nltk import word_tokenize
import json
import argparse
import pandas
from ast import literal_eval
import re

from omegaconf import DictConfig, OmegaConf

import config.root_path as rp

nltk.download('punkt')

def extract_all_text(fileLocation):

    fulltext = ""
    with open(fileLocation, 'r', encoding='utf-8') as json_file:
        for line in json_file:
            result = json.loads(line)
            fulltext += result['contents'] + ' '
    return fulltext


def construct_vocabulary(text):

    text = text.lower()

    whitelist = set("abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'")
    text = ''.join(filter(whitelist.__contains__, text))

    text = re.sub(r'\.(?!(?<=\d\.)\d) ?', '. ', text)

    text_tokenized = word_tokenize(text)
    unique_tokens = list(set(text_tokenized))

    #some tokens added manually
    unique_tokens.append('50:50')
    unique_tokens.append('109')
    unique_tokens.append('se')
    unique_tokens.append('91360')
    unique_tokens.append('locator')
    unique_tokens.append('utilizing')
    unique_tokens.append('computer')
    unique_tokens.append('qr')
    unique_tokens.append('4/4c/4c')
    unique_tokens.append('editing')
    unique_tokens.append('elect')
    unique_tokens.append('e-mail')
    unique_tokens.append('notify')
    unique_tokens.append('customize')
    unique_tokens.append('4c')
    unique_tokens.append('wi-fi')
    unique_tokens.append('hotspot')
    unique_tokens.append('connects')
    unique_tokens.append('alexa')
    unique_tokens.append('enjoy')
    unique_tokens.append('skill')
    unique_tokens.append('credentials')
    unique_tokens.append('authorize')
    unique_tokens.append('virtually')
    unique_tokens.append('ca/en')
    unique_tokens.append('com/en-us')
    unique_tokens.append('edit/edit')
    unique_tokens.append('michigan')
    unique_tokens.append('presented')
    unique_tokens.append('non-connected')
    unique_tokens.append('involves')
    unique_tokens.append('tech')
    unique_tokens.append('1-800-890-4038')
    unique_tokens.append('family')
    unique_tokens.append('loved')
    unique_tokens.append('ones')
    unique_tokens.append('boundary')
    unique_tokens.append('pinpoint')
    unique_tokens.append('curfew')
    unique_tokens.append('valet')
    unique_tokens.append('quarter-mile')
    unique_tokens.append('radius')
    unique_tokens.append('sunvisor')
    unique_tokens.append('radio-frequency')
    unique_tokens.append('smartwatch')
    unique_tokens.append('integration')
    unique_tokens.append('stats')
    unique_tokens.append('videos')
    unique_tokens.append('familiarize')
    unique_tokens.append('convenient')
    unique_tokens.append('in/register')
    unique_tokens.append('guardian-equipped')
    unique_tokens.append('four-digit')
    unique_tokens.append('cybersecuritywarning')
    unique_tokens.append('nob')
    unique_tokens.append('trunk/liftgate')
    unique_tokens.append('tower')
    unique_tokens.append('alarming')


    unique_tokens = sorted(unique_tokens)

    #print(len(unique_tokens))

    word_to_id = {}
    id_to_word = {}

    for i in range(len(unique_tokens)):
        word_to_id[unique_tokens[i]] = i
        id_to_word[i] = unique_tokens[i]

    return word_to_id, id_to_word




def convert_text_to_textual(text_numeric, id_to_word):
	text = [id_to_word[word] for word in text_numeric]
	return ' '.join(text)

config_path = rp.getRootPath() / "config"
@hydra.main(version_base=None, config_path= str(config_path), config_name="config_convert")
def main(cfg: DictConfig):
    print('-' * 20)
    print(OmegaConf.to_yaml(cfg))
    print('-' * 20)

    assert hasattr(cfg, 'base')
    assert hasattr(cfg, 'full_text_location')

    base = cfg.base
    fullTextLocation = cfg.full_text_location


    text = extract_all_text(fullTextLocation)

    word_to_id, id_to_word = construct_vocabulary(text)

    with open(base+'word_to_id.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(word_to_id))


    with open(base+'id_to_word.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(id_to_word))


    train = pandas.read_csv(base+'train.csv', encoding='utf-8')
    test = pandas.read_csv(base+'test.csv', encoding='utf-8')
    dev = pandas.read_csv(base+'dev.csv', encoding='utf-8')
    unanswerable = pandas.read_csv(base+'unanswerable.csv', encoding='utf-8')


    train['Context'] = train['Context'].apply(literal_eval)
    test['Context'] = test['Context'].apply(literal_eval)
    dev['Context'] = dev['Context'].apply(literal_eval)
    unanswerable['Context'] = unanswerable['Context'].apply(literal_eval)


    train['Context'] = train['Context'].apply(convert_text_to_textual, id_to_word=id_to_word)
    test['Context'] = test['Context'].apply(convert_text_to_textual, id_to_word=id_to_word)
    dev['Context'] = dev['Context'].apply(convert_text_to_textual, id_to_word=id_to_word)
    unanswerable['Context'] = unanswerable['Context'].apply(convert_text_to_textual, id_to_word=id_to_word)


    train.to_csv(base+'train.csv', encoding='utf-8')
    test.to_csv(base+'test.csv', encoding='utf-8')
    dev.to_csv(base+'dev.csv', encoding='utf-8')
    unanswerable.to_csv(base+'unanswerable.csv', encoding='utf-8')

    return

if __name__ == '__main__':
    main()
