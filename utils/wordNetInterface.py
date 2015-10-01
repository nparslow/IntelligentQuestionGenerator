__author__ = 'nparslow'

# goal is to be able to look up synonyms, hypernyms etc. of a given word (or lemma probably)
# can we use nltk with the french wordnet file? oh actually nltk has french wordnet!
# looks like no non-english lemmatiser in ntlk so use morfette to lemmatise

#WORDNET_FILE = "/home/nparslow/Documents/WOLF/wolf-1.0b4.xml"

from nltk.corpus import wordnet as wn

# todo : add POS wn.NOUN wn.VERB wn.ADJ
def getSynonyms( lemma ):
    # wn.synsets( lemma.decode('utf-8'), lang="fra" )
    print wn.synsets("fear")
    print wn.synsets( lemma, lang="fra" )
    for synset in wn.synsets( lemma, lang="fra"):
        print "--Synset--"
        #print synset # print synset gives a runtime error warning
        print synset.definition() # in english
        print synset.examples()  # in english
        print synset.hypernyms()
        print synset.lemma_names('fra') #, synset.hyponyms()
        print synset.lemmas('fra')

    #    for hyper in synset.hypernyms():
    #        print hyper.lemma_names('fra')
        pass


def test():
    lemma = u"peur"
    getSynonyms(lemma)

    pass

if __name__ == "__main__":
    test()
