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

if __name__ == '__main__':
    results = main()
    with open(os.path.join(os.getcwd(), 'fono', 'data', 'results.json'), mode='w') as f:
        json.dump(results, f)
