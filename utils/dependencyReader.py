import codecs
import os.path

__author__ = 'nparslow'

'''
word2vecf expects 3 files:
word_vocabulary:
   file mapping words (strings) to their counts
context_vocabulary:
   file mapping contexts (strings) to their counts
   used for constructing the sampling table for the negative training.
training_data:
   textual file of word-context pairs.
   each pair takes a seperate line.
   the format of a pair is "<word> <context>", i.e. space delimited, where <word> and <context> are strings.
   if we want to prefer some contexts over the others, we should construct the
   training data to contain the bias.
'''


def add2count( dic, key):
    if key not in dic:
        dic[key] = 0
    dic[key] += 1


def writeVocabToFile( vocabdict, outputFilename ):
    '''
    takes a vocab->count dictionary and writes it as the outputfilename with word and count separated by a space
    :param vocabdict:
    :param outputFilename:
    :return:
    '''
    with codecs.open( outputFilename, mode="wb", encoding="utf-8" ) as outfile:
        for vocabelement in vocabdict:
            outfile.write(vocabelement + " " + str(vocabdict[vocabelement]) + "\n")

def readRSELfile( rselFilename, outputBaseDirectory, debug=False ):

    vocab2count = {}
    context2count = {}

    if not os.path.isdir(outputBaseDirectory):
        # todo check it doesn't exist as a file already
        os.mkdir(outputBaseDirectory)
    outputTrainingFilename = os.path.join(outputBaseDirectory, "training_data")
    outputWordVocabFilename = os.path.join(outputBaseDirectory, "word_vocabulary")
    outputContextVocabFilename = os.path.join(outputBaseDirectory, "context_vocabulary")

    with codecs.open(outputTrainingFilename, mode="wb", encoding="utf-8") as outtrainfile:
        with codecs.open(rselFilename, mode="rb", encoding='latin-1') as rselfile:
            linenum = 0
            for line in rselfile:
                linenum += 1
                headlemma_pos, dep, deplemma_pos, occurances, weight, corpus_article_sentence_egs \
                    = line.strip().split('\t')

                if linenum % 10000 == 0:
                    #break
                    print "lines processed:", linenum
                    print headlemma_pos, dep, deplemma_pos #, somenumber, somenumber2, corpus_article_sentence
                    if debug:
                        if " " in headlemma_pos: print "WARNING HEAD"
                        if " " in dep : print "WARNING DEP"
                        if " " in deplemma_pos : print "WARNING DEPLEM"

                # replace any spaces with "__" (not a single as that's already used)
                headlemma_pos = headlemma_pos.replace(" ", "__")
                dep = dep.replace(" ", "__")
                deplemma_pos = deplemma_pos.replace(" ", "__")

                # join the dep and deplemma_pos to make a context element: (3*_ to join)
                contextelement = dep + "___" + deplemma_pos
                invcontextelement = dep + "___INV_" + headlemma_pos

                # always add the dependent (since all words are dependent on something but not vice-versa)
                # well ... hopefully ... is the main verb dependent on something??
                add2count(vocab2count, headlemma_pos)
                add2count(context2count, contextelement)
                # same for the inverse relation:
                add2count(vocab2count, deplemma_pos )
                add2count(context2count, invcontextelement)



    # todo - rewrite to take into account counts and contexts, prob can't run on my computer as data file will
    # todo - end up too large
    with codecs.open(outputTrainingFilename, mode="wb", encoding="utf-8") as outtrainfile:
            outtrainfile.write(headlemma_pos + " " + contextelement + "\n")
            outtrainfile.write(deplemma_pos  + " " + invcontextelement + "\n")
    # now write the vocab files:
    writeVocabToFile(vocab2count, outputWordVocabFilename)
    writeVocabToFile(context2count, outputContextVocabFilename)




def test():
    rselFilename = u"/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4.rsel"
    outDir = u"/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4_try"
    readRSELfile(rselFilename, outDir)



if __name__ == "__main__":
    test()

