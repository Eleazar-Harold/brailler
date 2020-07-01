# Translate braille to alphabet based text.
from . import AlphaBrailleMapper, BrailleAlphaMapper

CAPITAL = chr(10272)  # ⠠
NUMBER = chr(10300)  # ⠼
UNRECOGNIZED = "?"


def trim(word):
    # Remove punctuation around a word.
    while (
        len(word) is not 0
        and word[0] not in BrailleAlphaMapper.letters
        and word[0] not in BrailleAlphaMapper.contractions
    ):
        word = word[1:]
    while (
        len(word) is not 0
        and word[-1] not in BrailleAlphaMapper.letters
        and word[-1] not in BrailleAlphaMapper.contractions
    ):
        word = word[:-1]
    return word


def numbers_handler(word):
    # Translate braille numbers to standard number notation.
    if word == "":
        return word
    result = ""
    is_number = False
    for i in range(0, len(word)):
        if word[i] == NUMBER:
            is_number = True
            continue
        if is_number and word[i] in BrailleAlphaMapper.numbers:
            result += BrailleAlphaMapper.numbers.get(word[i])
        else:
            result += word[i]
    return result


def capital_letters_handler(word):
    # Capitalize letters after the capitalization escape code.
    if word == "":
        return word
    result = ""
    for i in range(0, len(word)):
        if (
            i - 1 >= 0
            and word[i - 1] == CAPITAL
            and word[i] in AlphaBrailleMapper.letters
        ):
            result += word[i].upper()
        elif word[i] != CAPITAL:
            result += word[i]
    return result


def word_to_alpha(word):
    # Convert a braille word to alphabet based text.
    if word in BrailleAlphaMapper.contractions:
        return BrailleAlphaMapper.contractions.get(word)
    else:
        result = ""
        for i in range(0, len(word)):
            if word[i] in BrailleAlphaMapper.letters:
                result += BrailleAlphaMapper.letters.get(word[i])
            elif word[i] in BrailleAlphaMapper.punctuation:
                result += BrailleAlphaMapper.punctuation.get(word[i])
        return result


def extract_words(string):
    # Split up a sentence based on whitespace (" ") and new line ("\n") chars.
    words = string.split(" ")
    result = []
    for word in words:
        temp = word.split("\n")
        for item in temp:
            result.append(item)
    return result


def fix_exceptions(string):
    # Fix exceptions where a braille symbol can have multiple meanings.
    result = ""
    # Decipher whether "⠦" should be "“" or "?".
    for i in range(0, len(string)):
        if (
            i - 1 >= 0
            and string[i] == "“"
            and string[i - 1] in AlphaBrailleMapper.letters
        ):
            result += "?"
        else:
            result += string[i]
    # Decipher whether "()" should be "(" or ")".
    open_bracket = False
    while result.find("()") != -1:
        if open_bracket:
            result = result.replace("()", ")", 1)
        else:
            result = result.replace("()", "(", 1)
        open_bracket = not open_bracket
    return result


def translate(string):
    # Convert braille to alphabet based text.
    alpha = ""
    words = extract_words(string)
    for word in words:
        word = numbers_handler(word)
        trimmed_word = trim(word)  # Remove punctuation.
        untrimmed_word = word
        index = untrimmed_word.find(trimmed_word)
        shavings = untrimmed_word.replace(trimmed_word, "")
        alpha = build_alpha_word(trimmed_word, shavings, index, alpha) + " "
    alpha = capital_letters_handler(alpha[:-1])
    return fix_exceptions(alpha)


def build_alpha_word(trimmed_word, shavings, index, alpha):
    # Translate a trimmed braille word to alphabet
    # based text then re-attach the shavings.
    if shavings == "":
        alpha += word_to_alpha(trimmed_word)
    else:
        for i in range(0, len(shavings)):
            if i == index and trimmed_word is not "":
                alpha += word_to_alpha(trimmed_word)
            if shavings[i] in BrailleAlphaMapper.punctuation:
                alpha += BrailleAlphaMapper.punctuation.get(shavings[i])
            else:
                alpha += shavings[i]
        if index == len(shavings):  # If the shavings are all at the beginning.
            alpha += word_to_alpha(trimmed_word)
    return alpha
