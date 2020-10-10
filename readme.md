# Trie searching problem

### Goal 
*Note: in reality, i would just use pyhtrie for this problem, but it was a fun exercise. Challenge text follows:

Implement a Trie (see https://en.wikipedia.org/wiki/Trie) according to the following requirements. The idea is to build a data structure that makes it easy to find specific terms in some text.

Supposing I have a set of terms, I can put them in the data structure and run my text through the data structure to see which of those terms are in the text.

A term may be multiple words (sometimes called tokens). The Trie should be built using tokens (not characters - which is the most common explanation and is what is showing in wikipedia). The text will need to be "tokenized" at some point and probably clean off punctuation and so on.

### How to run this algorithm
- The file **input-terms.txt** contains a list of line-separated terms to put in the Trie.
- The file **input-text.txt** contains paragraphs of text that will be searched for matches. 
- Run the **python-project.py** file to use the application. The main method can be updated to feed in different source data. The resulting matches are written to the console as a frequency map (key: trie term; value: number of matches). 
*Note: It is recommended to run this using Python 3.8+, but version 3.6+ should be supported.
