class WordsLoader:
    def __init__(self, file_name):

        info = {}

        with open(file_name) as file:
            line = file.readline()
            while line:
                # get first character
                first_character = line[:1]
                if first_character != '#':
                    (word, polarity) = self.process_line(line)
                    info[word] = polarity

                line = file.readline()

        self.polarized_words = info
        print('Finished loading polarized words')

    def process_line(self, line):
        words = line.split("\t")

        # get word and remove part of speach information
        word = words[0].rsplit('#', 1)[0]
        polarity = words[1].strip()
        return (word, polarity)
