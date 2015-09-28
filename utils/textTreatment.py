# coding=utf-8
import re

__author__ = 'nparslow'

'''
a (very) simple French tokeniser (normally you'd use a better one)
takes a string and returns a list of tokens
punctuation included
separation by space and by apostrophe with some exceptions
'''


def tokenise(text):
    # remove the spaces first (except \n), these are thrown away (unlike other separators)
    tokens = re.split(ur"[^\S\n]+", text, flags=re.UNICODE)
    # now the pronouns after (with a dash)
    pronounaffixes = ur"-(y|en|moi|toi|lui|nous|vous|leur|le|la|les|m'|t'|se)+"
    tokens = [newtoken for oldtoken in tokens for newtoken in re.split(pronounaffixes, oldtoken, flags=re.UNICODE)]

    #print tokens
    # I use a for loop as it's difficult to use the apostrophe as a delimiter and re-attach it
    # now for anything with a ' except aujourd'hui (there are other older exceptions
    #tokens = [newtoken for oldtoken in tokens for newtoken in re.split(ur"(?<!aujourd)(?<=')(?!hui)", oldtoken,
    #                                                                   flags=re.UNICODE)]
    newtokens = []
    for oldtoken in tokens:
        # can't have aujourd before or hui after, (') to retain the '
        apostrophesplit = re.split(ur"(?<!aujourd)'(?!hui)", oldtoken, flags=re.UNICODE)
        if len(apostrophesplit) > 1:
            apostrophesplit = [ apostrophesplit[i] + u"'" for i in range(len(apostrophesplit)-1)]\
                              + [apostrophesplit[-1]]
        newtokens.extend(apostrophesplit)
    tokens = newtokens

    print [ x for x in tokens if "\n" in x]
    # now for other punctuation
    tokens = [newtoken for oldtoken in tokens for newtoken in re.split(ur"([^'\w])", oldtoken,
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






def test():
    # (not real french but for testing)
    text = u"LE DÉCRYPTAGE ÉCO par Vincent Giret lundi 28 septembre 2015.\nsalut t'en fait-t'y bien aujourd'hui"
    tokens = tokenise(text)
    print tokens
    sentences = sentenceSegmeter(tokens)
    print sentences
    namedEntityRecognition(sentences)
    print sentences

if __name__ == "__main__":
    test()
