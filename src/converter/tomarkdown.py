import re
from rfcparser.rfcparser import Type

class Block: # will deprecate
    def getId(self) :
        return self.id

    def getOpener(self):
        return self.opener

    def getCloser(self):
        return self.closer

    def getConnecter(self):
        return self.connecter

class RawContent(Block):
    def __init__(self, text):
        self.id = Type.RAW
        self.opener = '```text\n'
        self.text = text
        self.closer = '\n```'
        self.connecter = '\n\n'

class TableOfContent(RawContent):
    def __init__(self, text):
        RawContent.__init__(self, text)
        self.id = Type.TOC
        self.connecter = '\n'

class Table(RawContent):
    def __init__(self, text):
        RawContent.__init__(self, text)
        self.id = Type.TABLE
        self.connecter = '\n```\n```text\n'

class Header(Block):
    def __init__(self, text):
        self.id = Type.HEADER
        self.opener = '----\n**'
        self.text = text
        self.closer = '**'
        self.connecter = '**\n\n----\n**'

    def getOpener(self):
        opener = '#'
        for i in range(self.text.split(' ')[0].count('.')) :
            opener = opener + '#'
        return '---\n' + opener + ' **'

    def getConnecter(self):
        return self.getCloser() + '\n' + self.getOpener();

class Content(Block):
    def __init__(self, text):
        self.id = Type.CONTENT
        self.opener = ''
        self.text = text
        self.closer = ''
        self.connecter = '\n\n'

def toMakrdownBlock(element):
    blocks = []

    type = element.data['type']
    text = element.data['original']
    block = None
    if type == Type.PAGEBREAK : # ignore page break
        pass
    elif type == Type.TOC :
        block = TableOfContent(text)
    elif type == Type.TABLE :
        block = Table(text)
    elif type == Type.HEADER :
        block = Header(text)
    elif type == Type.CONTENT :
        block = Content(text)
    elif type == Type.RAW :
        block = RawContent(text)

    return block