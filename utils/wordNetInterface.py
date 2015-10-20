# coding=utf-8
__author__ = 'nparslow'

# goal is to be able to look up synonyms, hypernyms etc. of a given word (or lemma probably)
# can we use nltk with the french wordnet file? oh actually nltk has french wordnet!
# looks like no non-english lemmatiser in ntlk so use morfette to lemmatise

#WORDNET_FILE = "/home/nparslow/Documents/WOLF/wolf-1.0b4.xml"

from nltk.corpus import wordnet as wn
#import heapq

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

# get the 3 most similar words in the vocab:
def getMostSimilar( lemma, vocab, n=3 ):
    # todo : pos is a big factor it seems in e.g. peur -> a verb first, so need to assume we have a pos
    # todo : re: http://www.nltk.org/howto/wordnet.html
    # wn.synsets( lemma.decode('utf-8'), lang="fra" )
    lsynset = wn.synsets( lemma, lang="fra")

    #  tuples (distance, lemma)
    nearest_n = []

    # not all words are in wordnet
    #print "lemma is:", lsynset
    if len(lsynset) > 0:
        lsynset = lsynset[0] # first in the list
        l_pos = lsynset.pos()

        #print "lemma is:", lsynset

        for vlemma in vocab:
            vsynset = wn.synsets( vlemma, lang="fra")
            if len(vsynset) > 0:
                vsynset = vsynset[0] # first in the list
                #print vsynset

                # simple step count:
                dist = lsynset.path_similarity(vsynset)

                if vsynset.pos() == l_pos:
                    dist = lsynset.lch_similarity(vsynset) # Leacock-Chodorow Similiarity - needs same POS
                else:
                    continue

                print nearest_n, (dist, vsynset)

                i = len(nearest_n)
                if i == 0:
                    nearest_n = [(dist, vsynset)]
                else:
                    while i >= 0:
                        if i == 0:
                            nearest_n = [(dist, vsynset)] + nearest_n[0:min(len(nearest_n),n-1)]
                            break
                        elif dist < nearest_n[i-1][0]:
                            i -= 1
                            continue
                        else:
                            if i < len(nearest_n):
                                nearest_n = nearest_n[0:i] + [(dist, vsynset)] + nearest_n[i:min(len(nearest_n),n-1)]
                            break
    print nearest_n

    '''
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
    '''

def test():
    lemma = u"peur"
    #getSynonyms(lemma)
    vocab = [u"émotion", u"bêtise", u"chercher", u"être", u"pleine", u"homme", u"femme"]
    getMostSimilar( lemma, vocab)

    pass

if __name__ == "__main__":
    test()
