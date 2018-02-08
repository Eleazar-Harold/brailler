from . import AlphaBrailleMapper


class Printer:
    def uppercase_alphabet_utf_codes(self):
        # Print capital alphabet based letters and their respective UTF codes.
        print("UTF Codes for Capital Letters:")
        for i in range(65, 91):
            print(chr(i), i, end='    ')
            if i % 8 == 0:
                print()
        print()

    def lowercase_alphabet_utf_codes(self):
        # Print alphabet based letters and their respective UTF codes.
        print("UTF Codes for Letters:")
        for i in range(97, 123):
            print("%c %3d" % (chr(i), i), end='   ')
            if i % 8 == 0:
                print()
        print()

    def braille_utf_codes(self):
        # Print all 64 braille combinations and their respective UTF codes.
        print("UTF Codes for Braille Symbols:")
        for i in range(10240, 10304):
            print(chr(i), i, end='  ')
            if (i + 1) % 8 == 0:
                print()

    def alphabet(self):
        # Print the English alphabet with their respective Braille representations.
        print("Letters:")
        for i in range(97, 123):
            print(chr(i), AlphaBrailleMapper.letters.get(chr(i)), end='   ')
            if i % 8 == 0:
                print()
        print()

    def contractions(self):
        # Print Braille symbols that represent whole words.
        print("Contraction:")
        count = 0
        word_list = []
        for word in AlphaBrailleMapper.contractions:
            word_list.append(word)
        word_list.sort()
        for word in word_list:
            formatted = '{:<10}'.format(word)
            print("%c %10s" % (AlphaBrailleMapper.contractions.get(word), formatted), end="")
            count += 1
            if count % 5 == 0:
                print()
        print()

    def numbers(self):
        # Print numbers in Braille and in standard notation.
        print("Numbers (must proceed after the ⠼ escape code):")
        count = 0
        num_list = []  # Punctuation list.
        for num in AlphaBrailleMapper.numbers:
            num_list.append(num)
        num_list.sort()
        for num in num_list:
            print(num, AlphaBrailleMapper.numbers.get(num), end="        ")
            count += 1
            if count % 5 == 0:
                print()

    def punctuation(self):
        # Print Braille symbols for punctuation.
        print("Punctuation:")
        count = 0
        pun_list = []  # Punctuation list.
        for pun in AlphaBrailleMapper.punctuation:
            pun_list.append(pun)
        pun_list.sort()
        for pun in pun_list:
            print(pun, AlphaBrailleMapper.punctuation.get(pun), end="        ")
            count += 1
            if count % 5 == 0:
                print()
        print()

    def all_utf_codes(self):
        # Print the UTF codes for both lowercase and uppercase letters and for Braille symbols.
        self.lowercase_alphabet_utf_codes()
        print()
        self.uppercase_alphabet_utf_codes()
        print()
        self.braille_utf_codes()

    def all_braille(self):
        # Print all the Braille symbols and their standard alphabet based representations.
        self.alphabet()
        self.contractions()
        self.punctuation()
        self.numbers()


# Test all mapper methods
printer = Printer()
print(printer.all_braille())
