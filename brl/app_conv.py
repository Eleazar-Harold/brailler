
from . import brailleTotext, textTobraille


class BrCnvx:
    def __init__(self, val=None, filename=None):
        self.val = val
        self.filename = filename

    def user_braille(self):
        return brailleTotext.translate(self.val)

    def user_text(self):
        return textTobraille.translate(self.val)

    def open_braille(self):
        file = open(self.filename)
        content = file.read()
        return brailleTotext.translate(content)

    def open_text(self):
        file = open(self.filename)
        content = file.read()
        return textTobraille.translate(content)
