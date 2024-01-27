from utils.phonemizer.base import BasePhonemizer
from utils.phonemizer.espeak_wrapper import ESpeak

PHONEMIZERS = {ESpeak.name}


ESPEAK_LANGS = list(ESpeak.supported_languages().keys())



# Add ESpeak languages and override any existing ones
_ = [ESpeak.name()] * len(ESPEAK_LANGS)
_new_dict = dict(list(zip(list(ESPEAK_LANGS), _)))
#DEF_LANG_TO_PHONEMIZER.update(_new_dict)


# Force default for some languages
#DEF_LANG_TO_PHONEMIZER["en"] = DEF_LANG_TO_PHONEMIZER["en-us"]



def get_phonemizer_by_name(name: str, **kwargs) -> BasePhonemizer:
    """Initiate a phonemizer by name

    Args:
        name (str):
            Name of the phonemizer that should match `phonemizer.name()`.

        kwargs (dict):
            Extra keyword arguments that should be passed to the phonemizer.
    """
    if name == "espeak":
        return ESpeak(**kwargs)

    raise ValueError(f"Phonemizer {name} not found")


if __name__ == "__main__":
    print(DEF_LANG_TO_PHONEMIZER)
