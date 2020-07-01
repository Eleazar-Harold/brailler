from brl import brailleTotext, textTobraille


class BrCnvx:
    def __init__(self, val=None, filename=None):
        self.val = val
        self.filename = filename

    @classmethod
    def user_braille(cls):
        return brailleTotext.translate(cls.val)

    @classmethod
    def user_text(cls):
        return textTobraille.translate(cls.val)

    @classmethod
    def open_braille(cls):
        file = open(cls.filename)
        content = file.read()
        return brailleTotext.translate(content)

    @classmethod
    def open_text(cls):
        file = open(cls.filename)
        content = file.read()
        return textTobraille.translate(content)
