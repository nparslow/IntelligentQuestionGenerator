import codecs
import os.path
import random
import tempfile

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


def add2count( dic, key, countToAdd=1):
    if key not in dic:
        dic[key] = 0
    dic[key] += countToAdd


def writeVocabToFile( vocabdict, outputFilename, mincount ):
    '''
    takes a vocab->count dictionary and writes it as the outputfilename with word and count separated by a space
    :param vocabdict:
    :param outputFilename:
    :return:
    '''
    with codecs.open( outputFilename, mode="wb", encoding="utf-8" ) as outfile:
        for vocabelement in vocabdict:
            if vocabdict[vocabelement] > mincount:
                outfile.write(vocabelement + " " + str(vocabdict[vocabelement]) + "\n")

# random generator with replacement
# re: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch18s04.html
#import random
#def sample_wr(population, _choose=random.choice):
#    while True: yield _choose(population)


def readRSELfile( rselFilename, outputBaseDirectory, debug=False ):
    '''
    Note that after running, you'll still need to shuffle the training file (see 'shuf' command in linux)
    :param rselFilename:
    :param outputBaseDirectory:
    :param debug:
    :return:
    '''
    vocab2count = {}
    context2count = {}
    # takes up too much memory:
    #lem_rel_dep2count = {}

    if not os.path.isdir(outputBaseDirectory):
        # todo check it doesn't exist as a file already
        os.mkdir(outputBaseDirectory)
    outputTrainingFilename = os.path.join(outputBaseDirectory, "training_data")
    outputWordVocabFilename = os.path.join(outputBaseDirectory, "word_vocabulary")
    outputContextVocabFilename = os.path.join(outputBaseDirectory, "context_vocabulary")

    #with codecs.open(outputTrainingFilename, mode="wb", encoding="utf-8") as outtrainfile:
    linenum = 0
    depcount = 0
    # we will assume max count on first line
    maxcount = 0

    print "first loop over file"

    with codecs.open(rselFilename, mode="rb", encoding='latin-1') as rselfile:

        for line in rselfile:
            linenum += 1
            headlemma_pos, dep, deplemma_pos, occurances, weight, corpus_article_sentence_egs \
                = line.strip().split('\t')
            occurances = int(occurances)
            depcount += occurances

            if linenum == 1:
                maxcount = occurances

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
            add2count(vocab2count, headlemma_pos, occurances)
            add2count(context2count, contextelement, occurances)
            # same for the inverse relation:
            add2count(vocab2count, deplemma_pos, occurances)
            add2count(context2count, invcontextelement, occurances)

            #add2count(lem_rel_dep2count, (headlemma_pos, dep, deplemma_pos), occurances)


    # take vocab and context only when > 100 counts:
    #vocab2count = dict([ (key,val) for key,val in vocab2count.items() if val > 100] )
    #context2count = dict([ (key,val) for key,val in context2count.items() if val > 100] )

    # not sure if I should actually have maxcount + 1 or +2  files for gaps before/after
    print "making temp files"
    tempfiles = [tempfile.TemporaryFile(mode="w+") for i in xrange(maxcount)]


    MINIMUMCOUNT =100
    # todo - rewrite to take into account counts and contexts, prob can't run on my computer as data file will
    # todo - end up too large
    #with codecs.open(outputTrainingFilename, mode="wb", encoding="utf-8") as outtrainfile:

        # shuffling large files:
        # https://github.com/trufanov-nok/shuf-t/tree/master/binaries

    with codecs.open(rselFilename, mode="rb", encoding='latin-1') as rselfile:
        tmplinenum = 0
        for line in rselfile:
            tmplinenum += 1
            headlemma_pos, dep, deplemma_pos, occurances, weight, corpus_article_sentence_egs \
                = line.strip().split('\t')
            occurances = int(occurances)

            if tmplinenum % 10000 == 0:
                #break
                print "lines processed writing:", tmplinenum
                print headlemma_pos, dep, deplemma_pos #, somenumber, somenumber2, corpus_article_sentence

            # replace any spaces with "__" (not a single as that's already used)
            headlemma_pos = headlemma_pos.replace(" ", "__")
            dep = dep.replace(" ", "__")
            deplemma_pos = deplemma_pos.replace(" ", "__")

            # join the dep and deplemma_pos to make a context element: (3*_ to join)
            contextelement = dep + "___" + deplemma_pos
            invcontextelement = dep + "___INV_" + headlemma_pos

        #for headlemma_pos, dep, deplemma_pos in lem_rel_dep2count.iterkeys():
                #count = lem_rel_dep2count[(headlemma_pos, dep, deplemma_pos)]


            if vocab2count[headlemma_pos] > MINIMUMCOUNT and context2count[contextelement] > MINIMUMCOUNT:
                #outtrainfile.writelines( [headlemma_pos + " " + contextelement + "\n"]*occurances)
                for counter in xrange(occurances):
                    randnum = random.randint(0, maxcount-1)
                    #with codecs.open( outputTrainingFilename + "_" + str(randnum) ,
                    #                 mode="ab+", encoding="utf-8") as outtrainfile:
                    #    outtrainfile.write(headlemma_pos + " " + contextelement + "\n")
                    outstring = (headlemma_pos + u" " + contextelement + u"\n").encode("utf8")
                    tempfiles[randnum].write(outstring)

            if vocab2count[deplemma_pos] > MINIMUMCOUNT and context2count[invcontextelement] > MINIMUMCOUNT:
                #outtrainfile.writelines( [headlemma_pos + " " + invcontextelement + "\n"]*occurances)
                for counter in xrange(occurances):
                    randnum = random.randint(0, maxcount-1)
                    #with codecs.open( outputTrainingFilename + "_" + str(randnum) ,
                    #                 mode="ab+", encoding="utf-8") as outtrainfile:
                    #    outtrainfile.write(deplemma_pos  + " " + invcontextelement + "\n")
                    outstring = (deplemma_pos  + " " + invcontextelement + "\n").encode("utf8")
                    tempfiles[randnum].write(outstring)


                '''
                filenum = 0

                for occ in range(occurances):
                    randnum = random.randint(0, depcount-1)

                    # append if the file exists, otherwise create a new one
                    # note assumes no such files exist already
                    with codecs.open( outputTrainingFilename + "_" + str(randnum) ,
                                     mode="ab+", encoding="utf-8") as outtrainfile:
                        outtrainfile.write( headlemma_pos + " " + contextelement + "\n" )
                '''

    '''
    with codecs.open( outputTrainingFilename,
                                     mode="ab+", encoding="utf-8") as outtrainfile:
        for n in depcount:
            try:
                linefilename = outputTrainingFilename + "_" + str(n)
                with codecs.open( linefilename , mode="rb", encoding="utf-8") as infile:
                    outtrainfile.writelines(infile.readlines())
                os.remove(linefilename)
            except Exception:
                pass
    '''

    print "combining temp files"
    # reset the temp files to the first line
    for tfile in tempfiles:
        tfile.seek(0)
    with codecs.open( outputTrainingFilename,
                                     mode="wb", encoding="utf-8") as outtrainfile:
        filecount = 0
        for tfile in tempfiles:
            filecount += 1
            if filecount % 10000 == 0:
                print "temp files read:", filecount
            # on average 1k lines per file so random shuffle is ok
            #print type(tfile.readlines())

            #blah = tfile.readlines()
            #print type(blah)
            #print blah
            lines = [x.decode('utf8') for x in tfile.readlines()]
            random.shuffle(lines)
            outtrainfile.writelines(lines)
            #outtrainfile.writelines(random.shuffle(tfile.readlines()))
            tfile.close()
            #break


    # now write the vocab files:
    writeVocabToFile(vocab2count, outputWordVocabFilename, MINIMUMCOUNT)
    writeVocabToFile(context2count, outputContextVocabFilename, MINIMUMCOUNT)




def test():
    rselFilename = u"/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4.rsel"
    outDir = u"/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4_try"
    readRSELfile(rselFilename, outDir)



if __name__ == "__main__":
    test()

