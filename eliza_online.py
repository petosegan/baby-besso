#!/usr/bin/env python

'''
Richard Turner
'''

import random
import string
import datetime
import re

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
    for rule in rules:
        m = rule.search(input)
        if m is None:
            continue
        mgroups = [switch_viewpoint(mg) for mg in m.groups()] # extract and transform free segments
        response = random.choice(rules[rule]).format(*mgroups) # choose and populate response template
        return response.upper()
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


def remove_punct(string):
    """Remove common punctuation marks."""

    return (string.replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .replace('!', ''))