import spacy
import re
from clickbait4 import clickbait
from subjectivemodel2 import subjective
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from gingerit.gingerit import GingerIt
from isnewstitle6 import checkNewsTitle


class checkTitle:

    def __init__(self, title):
        self.headline = title
        self.corrected = title
        self.own_corrections = {'iam': "i'm", 'im': "i'm"}

    # preprocess the text -> grammatical mistakes
    def lower_case(self):
        pattern = re.compile("<.*?>")
        head = self.headline
        head = pattern.sub(r'', head)
        pattern = re.compile(r'https?://\S+|www\.\S+')
        head = pattern.sub(r'', head)
        exclude = "[!\#\$%\&\(\)\*\+,\.\"/:;<=>\?@\[\\\\]\^_`\{\|\}\~0123456789]"
        return head.translate(str.maketrans('', '', exclude))

    # check for spelling mistakes, returns the percentage of incorrect spelled words
    def spelling_mistakes(self):
        head = self.lower_case()

        nlp = spacy.load('en_core_web_lg')
        doc = nlp(head)
        misspelled_words = []
        parser = GingerIt()  # using gingerit library for indian spell chceking enchant can also be used fto it
        words = []

        named_entities = []
        [named_entities.extend(x) for x in [ent.text.lower().split(" ") for ent in doc.ents if ent.label_ == 'PERSON']]

        for token in doc:
            if token.is_alpha and token.text.lower() in self.own_corrections:
                words.append(self.own_corrections[token.text.lower()])
                misspelled_words.append(token.text)
            elif token.is_alpha and not token.text.lower() == parser.parse(token.text.lower())['result'].lower() and \
                    token.text.lower() not in named_entities:
                misspelled_words.append(token.text)
                words.append(parser.parse(token.text.lower())['result'])
            else:
                words.append(token.text.lower())

        print(misspelled_words)
        if len(misspelled_words) == 0:
            return 0
        self.corrected = ' '.join(words)
        return len(set(misspelled_words)) / len(self.headline.split(" "))

    # check weather the title is a clickbait
    def classify_clickbait(self):
        click = clickbait(self.corrected)
        return click.run()

    # check weather the title is subjective, usually news headlines are objective
    def subjective_test(self):
        subjective_obj = subjective()
        answer = subjective_obj.send_request(self.corrected)
        return answer

    # checks weather the given title is a proper news title
    def is_newstitle(self):
        stop_words = set(stopwords.words('english'))

        if len(self.headline) > 70:
            return False

        if not re.search(r'[A-Z][a-z]+', self.headline):
            return False

        verb = False
        adjective = False
        noun = False

        tokenized = sent_tokenize(self.headline)
        for i in tokenized:
            wordslist = nltk.word_tokenize(i)
            wordslist = [w for w in wordslist if w not in stop_words]
            tagged = nltk.pos_tag(wordslist)

            for j in tagged:
                if j[1].find("VB") != -1:
                    verb = True
                if j[1].find("JJ") != -1:
                    adjective = True
                if j[1].find("NN") != -1:
                    noun = True

            if not verb or (not adjective and not noun):
                return False

        is_news = checkNewsTitle(self.headline)
        if is_news == 0:
            return False
        return True

    def run(self):
        print(self.spelling_mistakes())

