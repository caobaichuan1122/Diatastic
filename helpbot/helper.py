import numpy as np

from .constants import PREDEFINED_GREETINGS


def index_sort(lst):
    return np.argsort(-np.array(lst))

def is_greeting(text):
    return any(greeting in text.lower() for greeting in PREDEFINED_GREETINGS)
