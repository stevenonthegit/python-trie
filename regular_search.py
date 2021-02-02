#!/bin/python3
'''
An implementation of python-project.py that does not use a trie. 

This implementation uses the basic python string search to count matches in a large text block,
and was written to compare the efficiency of the two implementations against each other. 

This is way faster than the homemade trie search.
'''
import re
import timeit
from trie_search import read_word, add_frequency_map


def find_matches(terms_file: str, search_file: str):
    '''
    Uses the python string search function to search for given terms in a
    body of text. Returns results as a frequency map of matches. 
    
    This is to be used in conjunction with python-project.py's trie search, 
    to compare which one is faster. 

    :param terms_file: a text file containing a line separated list of search terms
    :type terms_file: str
    :param search_file: a text file containing a body of text to search within.
    :type search_file: str

    :return: a dict containing resulting matches mapped to the number of their occurrences.
    '''

    # place search terms into a basic list
    terms = [term.strip().lower() for term in open(terms_file, 'r').readlines()]

    results = {}

    # searches input text file for matches
    with open(search_file, 'r') as f:
        for line in read_word(f):
            # This is a brute force, simple, O(n^2) search. Despite that, it ends 
            # up being faster than the trie implementation in the other file.
            for term in terms:
                if (count:=line.count(term)) > 0:
                    add_frequency_map(results, term, count)

    return results


if __name__ == "__main__":
    
    count = 10000
    start = timeit.default_timer()
    for _ in range(count):
        out = find_matches('input_data/search_terms.txt', 'input_data/sample_text.txt')
    stop = timeit.default_timer()
    
    total_time = stop - start
    print('for', count, 'runs:', total_time) 
    print('final out:', out)
