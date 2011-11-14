import os
from Queue import Queue
from multiprocessing import Process
from parser import CorefParser

class RuleBased:
    
    # The number of sentences before and after
    # being considered for co-reference
    WINDOW_SIZE = 10
    
    def __init__(self):
        pass
    
    
    def loadXml(self, filename):
        """ Load the xml file in memory using
            the parser.
        """
        
        # Create a list of process with one parser for each
        #plist = []
        #for filename in os.listdir( os.path.join('data') ):
        #    parser = CorefParser()
        #    p = Process( target=parser.parse, args=(filename,) )
        #    
        #    plist.append(p)
        #
        # Execute them! :)
        #for p in plist:
        #    p.start()
        #    p.join()
        #
        #print 'Job done!'
        # The document that contains the parsed xml
        parser = CorefParser()
        parser.parse(filename)
        self.__doc = parser.getParsedDocument()
    
    
    def getSentenceQueue(self, s):
        sentenceQueue = Queue()
        
        for paragraph in self.__doc._paragraphs:
            #print 'iterating paragraph #'+paragraph._id
            for sentence in paragraph._sentences:
                sentenceQueue.put( sentence )
                if sentenceQueue.qsize() >= self.WINDOW_SIZE:
                    break
            if sentenceQueue.qsize() >= self.WINDOW_SIZE:
                break
        
        #print 'sentence queue size: '+ str(sentenceQueue.qsize())
        
        return sentenceQueue
        
    
    def extractHeadNoun(self, markable):
        """ Given a markable object, extracts
            the head noun of that markable
        """
        # Get the id of the last word in the markable
        headNounId = markable._slice.split(":")[1]
        headNoun = None
        for word in markable._sentence._words:
            if (word._id == headNounId):
                headNoun = word
        
        return headNoun
    
    
    def extractListOfWords(self, markable):
        """ Given a markable object, extracts
            the list of words that compose that markable
        """
        idW1, idW2 = markable._slice.split(":")[0], markable._slice.split(":")[1]
        wordList = []
        
        began = False
        for word in markable._sentence._words:
            # If the word is the first word in the markable
            if word._id == idW1:
                began = True
            if began:
                wordList.append(word)
            # If the word is the last word in the markable
            if word._id == idW2:
                break
        
        return wordList
    
    
    def checkHeadNounMatch(self, n1, n2):
        """ Given two nouns as Word objects,
            check if they match
        """
        return (n1._surfaceForm == n2._surfaceForm)
    
    
    def checkIdentityMatch(self, l1, l2):
        """ Given two lists of Word objects, check whether
            the two lists are an identity match or not
        """
        
        # TO-DO
        return True
    
    
    def run(self):
        matches = []
        sentences = []
        for paragraph in self.__doc._paragraphs:
            print 'checking paragraph #'+paragraph._id
            for sentence in paragraph._sentences:
                print 'adding sentence #'+sentence._id
                sentences.append(sentence)
        exit()
        
        
        for sentence in sentences:
            print '..checking sentence #'+sentence._id
            for markable in sentence._markables:
                headNoun = self.extractHeadNoun(markable)
                listOfWords = self.extractListOfWords(markable)
                sentencesQueue = self.getSentenceQueue(sentence)
                #print 'Testing markable ' + str( markable._id )
                
                # Iterate the sentences in the sentence queue to check
                # for potential matches in its markables
                finished = False
                while not finished:
                    s = sentencesQueue.get()
                    #print 'here... 2'
                    for m in s._markables:
                        headNoun2 = self.extractHeadNoun(m)
                        listOfWords2 = self.extractListOfWords(m)
                        
                        # Check if the head noun matches in both sentences
                        if ( self.checkHeadNounMatch(headNoun, headNoun2) ):
                            if self.checkIdentityMatch(listOfWords, listOfWords2):
                                matches.append( ('identity', markable, m) )
                            else:
                                matches.append( ('head-noun', markable, m) )
                    
                    #print '....Checked sentence #' + str(self.WINDOW_SIZE-sentencesQueue.qsize()) + ' in the queue.'
                    
                    if sentencesQueue.qsize()==0:
                        finished = True
        
        for match in matches:
            print match

if __name__ == '__main__':
    rb = RuleBased()
    rb.loadXml('462176newsML-done.xml.xml')
    rb.run()