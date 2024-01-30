import re
from . import istranslatable
from . import element as ele

class Type :
    PAGEBREAK = "PageBreak"
    TOC = "TableOfContent"
    HEADER = "Header"
    TABLE = "Table"
    RAW = "RawContent"
    CONTENT = "Content"

class RFCParser:
    def __init__(self):

        self.parseRules = [
            {
                'type': Type.PAGEBREAK,
                'progs':[
                    re.compile(r'\[page \d*\]', re.IGNORECASE),
                    re.compile(r'\\f'),
                ],
            },
            {
                'type': Type.TOC,
                'progs':[
                    re.compile(r'((((?<=\n)|^)  +)?.+?\n?.+?( |\.)(\.| \.)+( +)?\d+((?=\n)|$))'),
                    re.compile(r' +1\. +(Introduction|Overview)'),
                ],
            },
            {
                'type': Type.HEADER,
                'progs':[
                    re.compile(r'^(\w|\d).*$'),
                ],
            },
            {
                'type': Type.TABLE,
                'progs':[
                    re.compile(r'(-+  )+-+(?=\n)'),
                ],
            },
            {
                'type': Type.RAW,
                'progs':[
                    re.compile(r'^ +[^ ]+\n +([^ ]|\n +)+$'), # space less content
                    re.compile(r'\w    +[\W\w](.|\n)*[^\.]$'), # have large empty space with no comma end, it can be diagram
                    re.compile(r'^(\d\w?| )+$'), # number only diagram
                    re.compile(r'(>|<|\||\+)--+(>|<|\||\+)?'), # include -------->
                    re.compile(r'(>|<|\||\+)?--+(>|<|\||\+)'), # include <--------
                    re.compile(r'---+'), # diagram content
                    re.compile(r'( [0123456789abcdefABCDEF]{2}){5,}$'), # hex values
                    re.compile(r'^(   )*(  | |# )(?=[\w#])[^(\- )(\d+\.)](.|\n)+[^(\.|:)]$'),
                    re.compile(r'^(   \[[\w\-]+\]( {2,}|\n))'), # referrence docs info
                    re.compile(r'^ +Figure \d+: '), # bottom content of figure
                    re.compile(r'\n {10,}'), # too deep
                ],
            },
        ]
        self.progBlock = re.compile(r'(((?<=\n\n).|.)((.|\n.)*))')

    def getContentType(self, text) :
        for rule in self.parseRules :
            for prog in rule['progs'] :
                if prog.search(text) != None :
                    return rule['type']
        return None


    def checkNoneConetentPatterns(self, text) : # will deprecate
        for prog in self.noneContentProgs :
            if prog.search(text) != None :
                return True
        return False

    def parseV2(self, rfcText):
        elements = []
        rfcText = rfcText.replace("\f\n", "\f")
        reResults = self.progBlock.findall(rfcText)

        for result in reResults :
            try:
                contentString = result[0]
            except:
                continue

            block = None
            element = ele.Element(contentString)

            if element.isCached == True :
                elements.append(element)
                continue

            contentType = self.getContentType(contentString)

            if contentType != None :
                pass
            elif istranslatable.isTranslatable(contentString) != 0 :
                contentType = Type.CONTENT
            else :
                contentType = Type.RAW

            element.data['type'] = contentType
            print(f'content type is {contentType}')

            element.save()
            elements.append(element)
        
        return elements

    def parse(self, rfcText):
        return self.parseV2(rfcText)