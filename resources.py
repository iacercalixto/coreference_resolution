from __future__ import print_function

class Document:
    """ A document represents the information parsed
        in every and each of the XML documents available
        in the NP4E project
    """
    
    # list of the paragraphs contained in the xml document
    # (objects of class Paragraph)
    __paragraphs = []
    
    
    def __init__(self):
        pass
    
    
    # Methods to deal with lists
    def addParagraph(self, p):
        self.__paragraphs.append(p)
    
    def _get__paragraphs(self):
        return self.__paragraphs
    
    paragraphs = property(_get__paragraphs)


class Paragraph:
    """ A paragraph parsed in an XML file in the NP4E project
    """
    
    __document = None
    
    # list of the sentences contained in this paragraph
    # (objects of class Sentence)
    __sentences = []
    
    
    def __init__(self):
        pass
    
    
    def output(self):
        print(self.__sentences, " ", ".")
    
    
    # Getters and setters
    def _get__id(self):
        return self.__id
    def _set__id(self, newId):
        self.__id = newId
    
    # the unique id of the paragraph
    idx = property(_get__id, _set__id)
    
    def _get__document(self):
        return self.__document
    def _set__document(self, d):
        self.__document = d
    
    # the document object which is the parent of this one
    document = property(_get__document, _set__document)
    
    # Methods to deal with lists
    def addSentence(self, s):
        self.__sentences.append(s)
    
    def _get__sentences(self):
        return self.__sentences
    
    sentences = property(_get__sentences)


class Sentence:
    """ A sentence parsed in an XML file in the NP4E project
    """
    
    __paragraph = None
    
    # the list of words this sentence contains
    # (objects of class Word)
    __words = []
    
    # the list of marked NPs in this sentence
    # (objects of class Markable)
    
    # the key of the markable in the list is its slice, in the form 'from:to'
    __markables = []
    
    
    def __init__(self):
        pass
    
    
    def output(self):
        print(self.__words, " ", ".")
        print(self.__markables, " ", ".")
    
    
    # Getters and setters
    def _get__id(self):
        return self.__id
    def _set__id(self, newId):
        self.__id = newId
    
    # the unique id of the sentence
    idx = property(_get__id, _set__id)
    
    def _get__paragraph(self):
        return self.__paragraph
    def _set__paragraph(self, p):
        self.__paragraph = p
    
    # the paragraph object that is the parent of this one
    paragraph = property(_get__paragraph, _set__paragraph)
    
    # Methods to deal with lists
    def addMarkable(self, m):
        self.__markables.append(m)
    
    def addWord(self, w):
        self.__words.append(w)
    
    def _get__words(self):
        return self.__words
    
    def _get__markables(self):
        return self.__markables
    
    # the getters to the words and markables in this sentence
    words = property(_get__words)
    markables = property(_get__markables)


class Word:
    """ A word parsed in an XML file in the NP4E project
    """
    
    __sentence = None
    
    def __init__(self):
        pass
    
    
    def __repr__(self):
        return "word #id=" + str(self.idx) + " - " + str(self.surfaceForm)
    
    
    # Getters and setters
    def _get__id(self):
        return self.__id
    def _set__id(self, newId):
        self.__id = newId
    
    # the unique id of the word
    idx = property(_get__id, _set__id)
    
    def _get__lemma(self):
        return self.__lemma
    def _set__lemma(self, lemma):
        self.__lemma = lemma
    
    # the lemma of the word
    lemma = property(_get__lemma, _set__lemma)
    
    def _get__func(self):
        return self.__func
    def _set__func(self, func):
        self.__func = func
    
    # the function of the word in the sentence
    func = property(_get__func, _set__func)
    
    def _get__postag(self):
        return self.__postag
    def _set__postag(self, postag):
        self.__postag = postag
    
    # the word's part-of-speech tag
    postag = property(_get__postag, _set__postag)
    
    def _get__dep(self):
        return self.__dep
    def _set__dep(self, dep):
        self.__dep = dep
    
    # the id of the word this word depends on
    dep = property(_get__dep, _set__dep)
    
    def _get__surfaceForm(self):
        return self.__surfaceForm
    def _set__surfaceForm(self, surfaceForm):
        self.__surfaceForm = surfaceForm
    
    # the word's surface form
    surfaceForm = property(_get__surfaceForm, _set__surfaceForm)
    
    def _get__sentence(self):
        return self.__sentence
    def _set__sentence(self, s):
        self.__sentence = s
    
    # the sentence object that is the parent of this one
    sentence = property(_get__sentence, _set__sentence)


class Markable:
    """ A markable (namely an NP) parsed in an XML file in the NP4E project
    """
    
    __sentence = None
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return "markable #id=" + str(self.idx) + " - " + str(self.slicex)
    
    
    # Getters and setters
    def _get__id(self):
        return self.__id
    def _set__id(self, newId):
        self.__id = newId
    
    # the unique id of the word
    idx = property(_get__id, _set__id)
    
    def _get__comment(self):
        return self.__comment
    def _set__comment(self, comment):
        self.__comment = comment
    
    # some comments made by the annotator about the markable
    comment = property(_get__comment, _set__comment)
    
    def _get__coref(self):
        return self.__coref
    def _set__coref(self, coref):
        self.__coref = coref
    
    # an object that described which Markable this markable is co-referential to
    coref = property(_get__coref, _set__coref)
    
    def _get__slice(self):
        return self.__slice
    def _set__slice(self, newSlice):
        self.__slice = newSlice
    
    # denotes the slice of the list of words this markable contains
    slicex = property(_get__slice, _set__slice)
    
    def _get__sentence(self):
        return self.__sentence
    def _set__sentence(self, s):
        self.__sentence = s
    
    # the sentence object that is the parent of this ones
    sentence = property(_get__sentence, _set__sentence)
    


class CoRef:
    """ A co-reference defined by an annotator parsed in an XML file in the NP4E project.
        The UCoRef tag is ignored, use this class property _certain in that case
    """
    
    _markable = None
    
    def __init__(self, m):
        self._markable = m
    
    
    # Getters and setters
    def _get_id(self):
        return self._id
    def _set_id(self, newId):
        self._id = newId
    
    # the unique id of the word
    _id = property(_get_id, _set_id)
    
    def _get_certain(self):
        return self._certain
    def _set_certain(self, certain):
        self._certain = certain
    
    # whether the annotator is 100% sure about the co-reference or not
    _certain = property(_get_certain, _set_certain)
    
    def _get_comment(self):
        return self._comment
    def _set_comment(self, comment):
        self._comment = comment
    
    # some comments about the co-reference annotation
    _comment = property(_get_comment, _set_comment)
    
    def _get_src(self):
        return self._src
    def _set_src(self, src):
        self._src = src
    
    # the id of the markable this object's owner is co-referential to
    _src = property(_get_src, _set_src)
    
    def _get_type_ref(self):
        return self._type_ref
    def _set_type_ref(self, type_ref):
        self._type_ref = type_ref
    
    # the type of this co-reference
    # might be: BLA, BLE, BLI or BLU
    _type_ref = property(_get_type_ref, _set_type_ref)
    
    def _get_type_rel(self):
        return self._type_rel
    def _set_type_rel(self, type_rel):
        self._type_rel = type_rel
    
    # the type of relation of this co-reference
    # might be: BLA, BLE or BLU.
    _type_rel = property(_get_type_rel, _set_type_rel)