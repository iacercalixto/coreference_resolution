import os, sys
from xml.dom.minidom import parse, parseString
from resources import Word, Markable, Paragraph, Sentence, Document
import time
from multiprocessing import Process

class CorefParser:
    main_dir_name = 'data'
    
    def __init__(self):
        pass
    
    def __handleMarkable(self, xmlMarkable, xmlMarkableParent, s, nextWordIndex, appendString="...."):
        
        # The first element in the slice of this markable
        initialWordIndex = nextWordIndex
        
        # For all the possible child nodes inside a markable,
        # parse them
        if xmlMarkable.hasChildNodes():
            for xmlNode in xmlMarkable.childNodes:
                
                # If we've found a word inside this markable, parse it
                # an increase the word count only
                if xmlNode.nodeName == 'W':
                    nextWordIndex += 1
                    w = Word()
                    self.__handleWord(xmlNode, w)
                    s.addWord(w)
                    w.sentence = s
                    
                    #print '....added word id=' + str(xmlNode.attributes['ID'].nodeValue)
                
                # If we found a nested markable inside this markable
                if xmlNode.nodeName == 'MARKABLE':
                    # Update the nextWordIndex according to the index updated by the
                    # call of self.__handleMarkable recursively
                    nextWordIndex = self.__handleMarkable(xmlNode, xmlMarkable, s, nextWordIndex, appendString+"....")
                    #numWords = finalWordIndex
                
        else:
            raise Exception("There should be at least one word inside the markable id="+
                            xmlMarkable.attributes['ID'].nodeValue)
        
        # Create the markable
        m = Markable()
        m.idx = xmlMarkable.attributes['ID'].nodeValue
        m.comment = xmlMarkable.attributes['COMMENT'].nodeValue
        # Create the slice using the words' indexes in the sentence
        m.slice = str(initialWordIndex) + ":" + str(nextWordIndex-1)
        m.sentence = s
        # Every markable, no matter how deeply nested inside another markables,
        # will always be added to a sentence. They'll be accessible and identifiable
        # by their word slices.
        
        # Add the markable to the sentence
        s.addMarkable(m)
        
        # TO-DO: handle CoRef
        
        return nextWordIndex
    
    
    def __handleWord(self, xmlWord, word):
        #w = Word()
        w = word
        
        # All attributes exists (defaults behaviour)
        if (xmlWord.attributes.length==5):
            w.idx = xmlWord.attributes['ID'].nodeValue
            w.dep = xmlWord.attributes['DEP'].nodeValue
            w.func = xmlWord.attributes['FUNC'].nodeValue
            w.lemma = xmlWord.attributes['LEMMA'].nodeValue
            w.postag = xmlWord.attributes['POS'].nodeValue
        else:
            for i in range(xmlWord.attributes.length):
                attrName =  xmlWord.attributes.item(i).name
                if attrName == 'ID':
                    w.idx = xmlWord.attributes['ID'].nodeValue
                if attrName == 'DEP':
                    w.dep = xmlWord.attributes['DEP'].nodeValue
                if attrName == 'FUNC':
                    w.func = xmlWord.attributes['FUNC'].nodeValue
                if attrName == 'LEMMA':
                    w.lemma = xmlWord.attributes['LEMMA'].nodeValue
                if attrName == 'POS':
                    w.postag = xmlWord.attributes['POS'].nodeValue
        
        #print xmlWord.nodeName
        #print xmlWord.hasChildNodes()
        #print xmlWord.nodeValue
        
        w.surfaceForm = xmlWord.childNodes[0].data
        
        print w, w.surfaceForm
        
        return w
    
    
    def __handleSentence(self, xmlSentence, sentence):
        #s = Sentence()
        s = sentence
        s.idx = xmlSentence.attributes['ID'].nodeValue
        
        numWords = 0
        if xmlSentence.hasChildNodes():
            for xmlNode in xmlSentence.childNodes:
                print 'xmlNode.nodeName: '+xmlNode.nodeName
                if xmlNode.nodeName == 'MARKABLE':
                    finalWordIndex = self.__handleMarkable(xmlNode, s, s, numWords)
                    
                    # Add +1 to the finalWordIndex because it is decremented by
                    # one unit to make the slice range from index 0 to n-1
                    # (being n the number of words in the sentence)
                    numWords = finalWordIndex
                    
                if xmlNode.nodeName == 'W':
                    numWords += 1
                    w = Word()
                    self.__handleWord(xmlNode, w)
                    s.addWord(w)
                    w.sentence = s
        
        print s
        print 's.words: '+str(s.words)
        print 's.markables: '+str(s.markables)
        return s
    
    
    def __handleParagraph(self, xmlParagraph, paragraph):
        #p = Paragraph()
        p = paragraph
        p.idx = xmlParagraph.attributes['ID'].nodeValue
        
        if xmlParagraph.hasChildNodes():
            for xmlNode in xmlParagraph.childNodes:
                if xmlNode.nodeName == 'S':
                    s = Sentence()
                    print 'before handle_sentence'
                    self.__handleSentence( xmlNode, s )
                    print 'after handle_sentence'
                    p.addSentence(s)
                    s.paragraph = p
        
        print p, p.sentences
        #return p
    
    
    def __handleDocument(self, xmlDocument):
        d = Document()
        root = xmlDocument.firstChild
        
        maxNumParag = 2
        counter = 0
        if root.hasChildNodes():
            for xmlNode in root.childNodes:
                #print 'xmlNode.nodeName '+str(xmlNode.nodeName)
                if xmlNode.nodeName == 'DESC' or xmlNode.nodeName == 'TIME':
                    pass
                if xmlNode.nodeName == 'P':
                    counter += 1
                    
                    p = Paragraph()
                    print 'before hangle_paragraph'
                    self.__handleParagraph( xmlNode, p )
                    print 'after handle_paragraph'
                    d.addParagraph(p)
                    p.document = d
                    
                    
                    print p.idx
                    if counter >= maxNumParag:
                        break
                    
        print d, d.paragraphs
        """
        # After all the paragraphs, therefore sentences, therefore words
        # and markables have been parsed, the markables
        # will have its slices relative to the word indexes in the sentence,
        # being the first word index 0 and the last index numWords-1
        
        # Transform the indexes to absolute indexes, relative to the
        # word objects' ID attributes
        for paragraph in d._paragraphs:
            for sentence in paragraph._sentences:
                for markable in sentence._markables:
                    sliceIndex = markable._slice
                    fromIndex, toIndex = sliceIndex.split(":")[0], sliceIndex.split(":")[1]
                    
                    try:
                        fromId = sentence._words[int(fromIndex)]._id
                        toId = sentence._words[int(toIndex)]._id
                        #print fromId + " " + toId
                        markable._slice = fromId + ":" + toId
                    except ValueError:
                        # Value error here means that the key couldn't be converted to an int
                        # value, in that case it has already been converted by another
                        # markable and can be used "as is"
                        markable._slice = fromIndex + ":" + toIndex
        """
        return d
    
    
    def parse(self, filename='462176newsML-done.xml.xml'):
        """ Filename must be an XML 'file.xml'
        """
        time.clock()
        print 'Parsing file ' + str(filename)
        
        fullname = os.path.join(self.main_dir_name, filename)
        self.__dom1 = parse(fullname) # parse an XML file by name
        self.__parsedDocument = self.__handleDocument(self.__dom1)
        
        print 'Time elapsed: ' + str(time.clock())
    
    
    def parseString(self, string):
        """ String containing a valid XML
        """
        time.clock()
        self.__dom1 = parseString(string) # parse an XML file by name
        self.__parsedDocument = self.__handleDocument(self.__dom1)
        print 'Time elapsed: ' + str(time.clock())
        
    
    def getParsedDocument(self):
        return self.__parsedDocument
    
        

# The number of sentences before the sentence with an NP to be search for a coreference
WINDOW_SIZE = 10

if (__name__=='__main__'):
    string = """
    <D ID="D1">
        <P ID="P1">
            <S ID="S1">
                <W ID="W1">haha</W>
                <W ID="W2">hehe</W>
                <W ID="W3">hihi</W>
            </S>
        </P>
        <P ID="P2">
            <S ID="S2">
                <W ID="W4">hoho</W>
            </S>
            <S ID="S3">
                <W ID="W5">huhu</W>
                <W ID="W6">baba</W>
            </S>
            <S ID="S4">
                <W ID="W7">bebe</W>
            </S>
        </P>
    </D>
    """
    parser = CorefParser()
    parser.parseString(string)
    sentences = []
    
    for sentence in parser.getParsedDocument().paragraphs[0].sentences:
        print sentence.idx
    
    #for paragraph in parser.getParsedDocument()._paragraphs:
    #    print 'checking paragraph #'+paragraph._id
    #    for sentence in paragraph._sentences:
    #        print 'adding sentence #'+sentence._id
    #        sentences.append(sentence)
    """
    # Create a list of process with one parser for each
    plist = []
    for filename in os.listdir( os.path.join('data') ):
        parser = CorefParser()
        p = Process( target=parser.parse, args=(filename,) )
        plist.append(p)
    
    # Execute them! :)
    for p in plist:
        p.start()
        p.join()
    
    print 'Job done!'
    """