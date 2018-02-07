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
    # - bool: is_character
    # - bool: is_word
    # - list of string: words
    # - list of string: composition

# character object:
    # * inherits from symbol
    # - enum: place (pre, post, root)
    # - string or enum: morphological relationship

# bliss-word object:
    # * inherits from symbol








"""
1-31-18:
not sure if characters that are made up of other characters should be considered words or characters

"""