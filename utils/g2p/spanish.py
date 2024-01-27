""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''


# Regular expression matching whitespace:


import re
from unidecode import unidecode
import inflect
_inflect = inflect.engine()
_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_pounds_re = re.compile(r'£([0-9\,]*[0-9]+)')
_dollars_re = re.compile(r'\$([0-9\.\,]*[0-9]+)')
_ordinal_re = re.compile(r'[0-9]+(st|nd|rd|th)')
_number_re = re.compile(r'[0-9]+')


# List of (ipa, lazy ipa) pairs:
_lazy_ipa = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('r', 'ɹ'),
    ('æ', 'e'),
    ('ɑ', 'a'),
    ('ɔ', 'o'),
    ('ð', 'z'),
    ('θ', 's'),
    ('ɛ', 'e'),
    ('ɪ', 'i'),
    ('ʊ', 'u'),
    ('ʒ', 'ʥ'),
    ('ʤ', 'ʥ'),
    ('ˈ', '↓'),
]]

# List of (ipa, lazy ipa2) pairs:
_lazy_ipa2 = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('r', 'ɹ'),
    ('ð', 'z'),
    ('θ', 's'),
    ('ʒ', 'ʑ'),
    ('ʤ', 'dʑ'),
    ('ˈ', '↓'),
]]

# List of (ipa, ipa2) pairs
_ipa_to_ipa2 = [(re.compile('%s' % x[0]), x[1]) for x in [
    ('r', 'ɹ'),
    ('ʤ', 'dʒ'),
    ('ʧ', 'tʃ')
]]

def collapse_whitespace(text):
    return re.sub(r'\s+', ' ', text)

def mark_dark_l(text):
    return re.sub(r'l([^aeiouæɑɔəɛɪʊ ]*(?: |$))', lambda x: 'ɫ'+x.group(1), text)


def spanish_to_ipa(text):
    from utils.phonemizer.espeak_wrapper import ESpeak    
    e = ESpeak(language="es-419", keep_puncs=False)
    text = unidecode(text).lower()
    phonemes = e.phonemize(text)
    phonemes = collapse_whitespace(phonemes)
    return phonemes


def spanish_to_lazy_ipa(text):
    text = spanish_to_ipa(text)
    for regex, replacement in _lazy_ipa:
        text = re.sub(regex, replacement, text)
    return text


def spanish_to_ipa2(text):
    text = spanish_to_ipa(text)
    text = mark_dark_l(text)
    for regex, replacement in _ipa_to_ipa2:
        text = re.sub(regex, replacement, text)
    return text.replace('...', '…')


def spanish_to_lazy_ipa2(text):
    text = spanish_to_ipa(text)
    for regex, replacement in _lazy_ipa2:
        text = re.sub(regex, replacement, text)
    return text
