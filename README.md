# Trie searching problem

### Goal 
Implement a Trie (see https://en.wikipedia.org/wiki/Trie) according to the following requirements. The idea is to build a data structure that makes it easy to find specific terms in some text.

Supposing I have a set of terms, I can put them in the data structure and run my text through the data structure to see which of those terms are in the text.

A term may be multiple words (sometimes called tokens). The Trie should be built using tokens (not characters - which is the most common explanation and is what is showing in wikipedia). The text will need to be "tokenized" at some point and probably clean off punctuation and so on.

#### Prerequisites
- Python 3.8 or later
- `unittest` and `timeit` libraries, if running unit tests

#### Contents
- **input_data/search_terms.txt** contains a list of line-separated terms to search for. 
- **input_data/sample_text.txt** contains sample paragraphs of text that will be processed for matches.
- **trie_search.py** The main algorithm. This searches a text file for a variety of terms, and prints the matches as output. The algorithm is implemented using a trie. 
- **regular_search.py** An alternate implementation of the same algorithm. Instead of a trie, this uses the list structure to do the same search, with the same output. 
- **tests.py** A series of unit tests. 

#### How to run the program
- Run **trie_search.py**. The main method can be manually updated to feed in a different data source or search term. Results are printed to the console. 
- Run **tests.py** to view unit tests. 
