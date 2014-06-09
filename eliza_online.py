#!/usr/bin/env python

'''
Richard Turner
'''

import random
import string
import datetime
import re

## Talking to the computer
def interact(input, rules, default_responses):
    """Have a conversation with a user."""
    # Read a line, process it, and return the results.
    thistime = datetime.datetime(2000,1,1)
    # Remove the punctuation from the input and convert to upper-case
    # to simplify matching.
    input = remove_punct(input.upper())
    response = respond(rules, input, default_responses).upper()

    return response
    
# redo this with regexes
def respond(rules, input, default_responses):
    for rule in rules:
        m = rule.search(input)
        if m is None:
            continue
        response = m.expand(random.choice(rules[rule]))
        return switch_viewpoint(response)
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
    if string.endswith('?'):
        string = string[:-1]
    return (string.replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .replace('!', ''))
