import pickle
import os
import re
import json
from fono.parser import Parser
import pymongo


def main():
    database = None
    with open(os.path.join(os.getcwd(), 'fono', 'data', 'dasar.pickle'), mode='rb') as f:
        database = pickle.load(f)
    parser = Parser()
    parser.load()
    vocab = re.compile('(ai|au|ei|oi|[aiueo])')
    results = []
    for word in database:
        tokens = parser.parse(word)
        result = {
            'word': word,
            'tokens': []
        }
        for token in tokens:
            m = vocab.search(token)
            if m is None:
                # print(f'word = {word}')
                # print(f"tokens = {tokens}")
                # input()
                continue
            
            nucleus_idx = m.start()
            nucleus = token[nucleus_idx]
            onset = token[:nucleus_idx]
            coda = token[nucleus_idx + 1:]
            result['tokens'].append({
              'token': token,
              'nucleus': nucleus,
              'onset': onset,
              'coda': coda
            })
        results.append(result)
    return results

def split_char(s: str):
    gab_kons = re.compile('^(kh|ng|ny|sy|[bcdfghjklmnpqrstvwxyz])')
    v_pattern = re.compile('^[aiueo]')
    patterns = [
        (gab_kons, 'konsonan'), 
        (v_pattern, 'vocal')
    ]

    word = s
    result= []
    while word != '':
        for (pattern, tag)  in patterns:
            is_match = pattern.match(word)
            if is_match:
                _, end = is_match.span()
                match_w = is_match.group()
                word = word[end:]
                result.append((match_w, tag))
    return result

if __name__ == '__main__':
    results = main()
    counters = {}
    for data in results:
        w = data['word']
        for (char, tag) in split_char(w):
            key = (char, tag)
            if key not in counters:
                counters[key] = 0
            counters[key] += 1
    vocal_counters = [ {'char': c, 'count': count, 'tag': tag } for ((c, tag), count) in counters.items() if tag == 'vocal']
    kons_counters = [ {'char': c, 'count': count, 'tag': tag} for ((c, tag), count) in counters.items() if tag == 'konsonan']
    data_counters = vocal_counters + kons_counters
    # with open(os.path.join(os.getcwd(), 'fono', 'data', 'results.json'), mode='w') as f:
    #     json.dump(results, f)
    client = pymongo.MongoClient()
    db = client.fono
    db.counter.insert_many(data_counters)
