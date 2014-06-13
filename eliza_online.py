#!/usr/bin/env python

'''
Richard Turner
'''

import random
import string
import datetime
import re
from nltk import word_tokenize, pos_tag
import logging
logging.basicConfig( filename=r'C:\Users\Desktop\Besso\besso_online\elizalog.log', filemode='a' )

def interact(input, rules, default_responses):
    """Have a conversation with a user."""
    # Read a line, process it, and return the results.
    thistime = datetime.datetime(2000,1,1)
    # Remove the punctuation from the input and convert to upper-case
    # to simplify matching.
    input = remove_punct(input.upper())
    response = respond(rules, input, default_responses)

    return response
    
def respond(rules, input, default_responses):
    stripped_input = strip_adverbs(decontract(input))
    logging.debug(stripped_input)
    for rule in rules:
        m = rule.search(stripped_input)
        if m is None:
            continue
        mgroups = [switch_viewpoint(mg) for mg in m.groups()] # extract and transform free segments
        response = random.choice(rules[rule]).format(*mgroups) # choose and populate response template
        logging.debug(response)
        return parse_subobj(response.upper())
    return random.choice(default_responses)

## Translating user input

def replace(word, replacements):
    """Replace word with rep if (word, rep) occurs in replacements."""
    for old, new in replacements:
        if word == old:
            return new
    return word


def switch_viewpoint(input):
    """Swap some common pronouns for interacting with a robot."""
    replacements = [('I', 'YOU'),
                    ('YOU', 'I'),
                    ('ME', 'YOU'),
                    ('MY', 'YOUR'),
                    ('AM', 'ARE'),
                    ('ARE', 'AM'),
                    ('YOUR','MY'),
                    ('WE', 'YOU'),
                    ('OUR', 'YOUR'),
                    ('US', 'YOU'),
                    ('ID', 'YOU WOULD')
                    ]
    return ' '.join([replace(word, replacements) for word in input.split()])

def decontract(input):
    """Remove contractions"""
    contractions = [("AIN'T","IS NOT"),
                    ("AREN'T","ARE NOT"),
                    ("CAN'T","CANNOT"),
                    ("COULD'VE","COULD HAVE"),
                    ("COULDN'T","COULD NOT"),
                    ("COULDN'T'VE","COULD NOT HAVE"),
                    ("DIDN'T","DID NOT"),
                    ("DOESN'T","DOES NOT"),
                    ("DON'T","DO NOT"),
                    ("HADN'T","HAD NOT"),
                    ("HASN'T","HAS NOT"),
                    ("HAVEN'T","HAVE NOT"),
                    ("HE'D","HE HAD"),
                    ("HE'D'VE","HE WOULD HAVE"),
                    ("HE'LL","HE WILL"),
                    ("HE'S","HE IS"),
                    ("HOW'D","HOW DID"),
                    ("HOW'LL","HOW WILL"),
                    ("HOW'S","HOW IS"),
                    ("I'D","I WOULD"),
                    ("I'D'VE","I WOULD HAVE"),
                    ("I'LL","I WILL"),
                    ("I'M","I AM"),
                    ("I'VE","I HAVE"),
                    ("ISN'T","IS NOT"),
                    ("IT'D","IT HAD"),
                    ("IT'D'VE","IT WOULD HAVE"),
                    ("IT'LL","IT WILL"),
                    ("IT'S","IT IS"),
                    ("LET'S","LET US"),
                    ("MA'AM","MADAM"),
                    ("MIGHT'VE","MIGHT HAVE"),
                    ("MUST'VE","MUST HAVE"),
                    ("NEEDN'T","NEED NOT"),
                    ("O'CLOCK","OF THE CLOCK"),
                    ("SHAN'T","SHALL NOT"),
                    ("SHE'D","SHE WOULD"),
                    ("SHE'D'VE","SHE WOULD HAVE"),
                    ("SHE'LL","SHE WILL"),
                    ("SHE'S","SHE IS"),
                    ("SHOULD'VE","SHOULD HAVE"),
                    ("SHOULDN'T","SHOULD NOT"),
                    ("THAT'S","THAT IS"),
                    ("THERE'D","THERE WOULD"),
                    ("THERE'D'VE","THERE WOULD HAVE"),
                    ("THERE'S","THERE IS"),
                    ("THEY'D","THEY WOULD"),
                    ("THEY'D'VE","THEY WOULD HAVE"),
                    ("THEY'LL","THEY WILL"),
                    ("THEY'RE","THEY ARE"),
                    ("THEY'VE","THEY HAVE"),
                    ("WASN'T","WAS NOT"),
                    ("WE'D","WE WOULD"),
                    ("WE'D'VE","WE WOULD HAVE"),
                    ("WE'LL","WE WILL"),
                    ("WE'RE","WE ARE"),
                    ("WE'VE","WE HAVE"),
                    ("WEREN'T","WERE NOT"),
                    ("WHAT'LL","WHAT WILL"),
                    ("WHAT'RE","WHAT ARE"),
                    ("WHAT'S","WHAT IS"),
                    ("WHEN'S","WHEN IS"),
                    ("WHERE'D","WHERE DID"),
                    ("WHERE'S","WHERE IS"),
                    ("WHERE'VE","WHERE HAVE"),
                    ("WHO'LL","WHO WILL"),
                    ("WHO'S","WHO IS"),
                    ("WHY'S","WHY IS"),
                    ("WON'T","WILL NOT"),
                    ("WOULD'VE","WOULD HAVE"),
                    ("WOULDN'T","WOULD NOT"), 
                    ("YOU'D","YOU WOULD"),
                    ("YOU'D'VE","YOU WOULD HAVE"),
                    ("YOU'LL","YOU WILL"),
                    ("YOU'RE","YOU ARE"),
                    ("YOU'VE","YOU HAVE")]
    return ' '.join([replace(word, contractions) for word in input.split()])
    
def remove_punct(string):
    """Remove common punctuation marks."""

    return (string.replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .replace('!', ''))
            
def parse_subobj(input):
    """Correct uses of 'I' that should be 'ME'"""
    verbtags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    text = word_tokenize(input)
    tagset = pos_tag(text)
    logging.debug(tagset)
    output_words = [tagset[0][0]]
    for i in range(1, len(tagset)):
        if tagset[i][0] == "I" and tagset[i-1][1] in verbtags:
            output_words.append("ME")
        else:
            output_words.append(tagset[i][0])
    return ' '.join(output_words)

def strip_adverbs(input):
    """Remove all adverbs and interjections before parsing"""
    adverb_tags = ["RB", "RBR", "RBS", "UH", "WRB"]
    good_adverbs = ["NOT"]
    tagset = pos_tag(word_tokenize(input))
    logging.debug(tagset)
    output_words = []
    for i in range(0, len(tagset)):
        if tagset[i][1] in adverb_tags and tagset[i][0] not in good_adverbs:
            continue
        else:
            output_words.append(tagset[i][0])
    return ' '.join(output_words)