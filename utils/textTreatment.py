# coding=utf-8
import codecs
import re

__author__ = 'nparslow'

SPECIAL_TOKENS = {"_NUM_", "_NE_"}

'''
a (very) simple French tokeniser (normally you'd use a better one)
takes a string and returns a list of tokens
punctuation included
separation by space and by apostrophe with some exceptions
'''
def tokenise(text):
    # remove the spaces first (except \n), these are thrown away (unlike other separators)
    tokens = re.split(ur"[^\S\n]+", text, flags=re.UNICODE)
    # now the pronouns after (with a dash) - note two types of inverted comma
    # (todo not sure if l' or s' are possible in imperative?)
    pronounaffixes = ur"-(y|en|moi|toi|lui|nous|vous|leur|le|la|les|[mtsl]['’]|se)+"
    tokens = [newtoken for oldtoken in tokens for newtoken in re.split(pronounaffixes, oldtoken, flags=re.UNICODE)]

    #print tokens
    # I use a for loop as it's difficult to use the apostrophe as a delimiter and re-attach it
    # now for anything with a ' except aujourd'hui (there are other older exceptions
    #tokens = [newtoken for oldtoken in tokens for newtoken in re.split(ur"(?<!aujourd)(?<=')(?!hui)", oldtoken,
    #                                                                   flags=re.UNICODE)]
    newtokens = []
    apostrophes = ur"'’"
    for oldtoken in tokens:
        # can't have aujourd before or hui after, (') to retain the ' or ’ (but only the former type is kept)
        # also ignore if there is a space after
        apostrophesplit = re.split(ur"(?<!aujourd)["+apostrophes+ur"](?!(?:hui|\s))", oldtoken, flags=re.UNICODE)
        if len(apostrophesplit) > 1:
            apostrophesplit = [ apostrophesplit[i] + u"'" for i in range(len(apostrophesplit)-1)]\
                              + [apostrophesplit[-1]]
        newtokens.extend(apostrophesplit)
    tokens = newtokens

    print [ x for x in tokens if "\n" in x]
    # now for other punctuation
    tokens = [newtoken for oldtoken in tokens for newtoken in re.split(ur"([^"+apostrophes+ur"\w])", oldtoken,
                                                                       flags=re.UNICODE) if len(newtoken) > 0]
    # the () is to keep the separators
    # tokens = re.split(ur"([\W']+)", text, flags=re.UNICODE )
    # tokens = [x for x in tokens if not re.match(ur'\s+$', x, flags=re.UNICODE)]
    return tokens


'''
Take a list of tokens and group into sentences (roughly)
returns a list of lists, sentences -> tokens
normally you'd have something better but we'll just use '.' '?' '!' and newlines (except . for numbers)
tokens should include endlines, they will be removed but interpretted as sentence ends
'''
# TODO : fix for decimal places!!!
def sentenceSegmeter( tokens ):
    sentences = []
    currentsentence = []
    for token in tokens:
        if re.match(ur'[\.\?\!\n]+$', token, flags=re.UNICODE):
            is_endline = re.match(ur'\n', token, flags=re.UNICODE)
            # if it's the first character, probably it's multiple punctuation from the previous sentence:
            if len(sentences) > 0 and len(currentsentence) == 0:
                if not is_endline: sentences[-1].append(token)
            else:
                if not is_endline: currentsentence.append(token)
                sentences.append(currentsentence)
                currentsentence = []
        else:
            currentsentence.append(token)
    if len(currentsentence) > 0:
        sentences.append(currentsentence)
    return sentences

'''
takes in sentences (a list of lists) and (roughly) identifies named entities
here it is very primitive, we just look at capital letters which are not the first word in the sentence
TODO: easiest is perhaps to have a targetted vocab list (e.g. a very large dictionary), and everything not in that
 is treated as a named entity
named entities will be replaced by _NE_
numbers will be replaced by _NUM_
'''
def namedEntityRecognition( sentences ):

    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            token = sentences[i][j]
            if len(token) > 0 and \
                re.match(ur"\w", token, flags=re.UNICODE):
                if token[0].isupper():
                    # if there's more than one upper case letter or if it's not the first word:
                    if len([x for x in token if x.isupper()]) > 1 or j > 0:
                        sentences[i][j] = "_NE_"
                elif re.match(ur"^\d+$", token, flags=re.UNICODE):
                    sentences[i][j] = "_NUM_"

'''
read a file and extract the sentences from it
'''
def fileToSentences( filename , encode="utf-8"):
    sentences = []
    with codecs.open(filename, encoding=encode) as infile:
        sentences = sentenceSegmeter(tokenise(infile.read()))
        namedEntityRecognition(sentences)
    return sentences

'''
get the vocab used in the sentences (may want to add a frequency count too?)
(assumes named entities removed so lowers - but I guess this could be done at a different stage)
'''
def sentencesToVocab( sentences, debug=False ):
    vocab = set([])
    for sentence in sentences:
        # ignore named entities, punctuation
        vocab.update([token.lower() for token in sentence
                      if token not in SPECIAL_TOKENS and re.search(ur"[^\W_]", token, flags=re.UNICODE)])
        # check rejected wordforms:
        if debug:
            for token in [token for token in sentence
                          if token in SPECIAL_TOKENS or not re.search(ur"[^\W_]", token, flags=re.UNICODE)]:
                print "rejected wordform:", token
    return vocab

'''
Take a vocab and write it to a file one word per line
utf-8 encoding by default
will leave a blank line at end of file
'''
def writeVocabToFile( vocab, outfilename, encode="utf-8"):
    with codecs.open(outfilename, mode="w", encoding=encode) as outfile:
        for wordform in vocab:

            outfile.write(wordform + "\n")



def test():
    # (not real french but for testing)
    text = u"LE DÉCRYPTAGE ÉCO par Vincent Giret lundi 28 septembre 2015.\nsalut t'en fait-t'y bien aujourd'hui"
    tokens = tokenise(text)
    print tokens
    sentences = sentenceSegmeter(tokens)
    print sentences
    namedEntityRecognition(sentences)
    print sentences

    filename = "../resources/ExampleTextCatalogne.txt"
    print "reading from " + filename
    sentences = fileToSentences(filename)
    for sentence in sentences:
        print sentence
    vocab = sentencesToVocab(sentences)
    print "vocabulary size:", len(vocab)
    print vocab

    # we'll save the example text's vocab to a file (we'll remove some words in a moment)
    outfilename = "../resources/ExampleKnownVocab.txt"
    writeVocabToFile(vocab, outfilename)

if __name__ == "__main__":
    test()
