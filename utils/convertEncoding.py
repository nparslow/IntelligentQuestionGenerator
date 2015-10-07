import codecs

__author__ = 'nparslow'

# doesn't work, can't save utf8 as ascii, need to fix the sorter to handle utf8 ...
'''
def convFile( infilename, outfilename ):
    with codecs.open( infilename, mode="rb", encoding="utf8") as infile:
        with codecs.open( outfilename, mode="wb", encoding="ascii") as outfile:
            for line in infile:
                line = line.encode("utf8")
                outfile.write(line)


def test():
    infilename = "/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4_try/" + "test.txt"
    outfilename = "/home/nparslow/PycharmProjects/IntelligentQuestionGenerator/CPL4_try" + "test.out"
    convFile(infilename, outfilename)
'''

# random generator with replacement
# re: https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch18s04.html
import random
def sample_wr(population, _choose=random.choice):
    while True: yield _choose(population)

def test():
    for i in sample_wr(xrange(10)):
        print i
        if i == 9:
            break
    pass


if __name__ == "__main__":
    test()