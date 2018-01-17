# Author: Mohammad Usman Sohail
# Create Date: 1-16-17
# description: This is a high level file that forms the architecture of the system.



### INPUT SYMBOLS
    # input type: list of symbols in order.
    # output type: list of symbol objects

### DETERMINE IF ANY BLISS WORDS ARE FORMED.
    # input type: list of symbols objects in order.
    # output type: list of block objects

### DETERMINE MORPHOLOGICAL RELATIONSHIPS.
    # input  type: list of block objects
    # output type: list of word objects

### DETERMINE FINAL OUTPUT BASED ON N-GRAM INFO.
    # input type: list of word objects
    # output type: natural language string


# symbol object:
    # - bool: character
    # - bool: word
    # - string: definition / description

# character object:
    # * inherits from symbol
    # - enum: place (pre, post, root)
    # - string or enum: morphological relationship

# bliss-word object:
    # * inherits from symbol
    # - list of strings: possible words
    # - list of strings: characters the word is composed of
    # - list of strings: known natural english words that this word can be