from rfcparser.rfcparser import RFCParser, Type
from translator.translator import Translator
from rfcparser import requirementlevel as rl
from rfcparser import rfcprefix as pf
from converter.tomarkdown import *

import sys

class Converter :
    def __init__(self, languages = ["ko"], doTranslate = True):
        self.parser = RFCParser()
        self.translator = Translator()
        self.languages = languages
        self.doTranslate = doTranslate


    def writeFile(self, id, language, elements) :
        with open(f'./mds/{language}/rfc{id}.md', 'w') as markdownFile :
            lastBlock = None
            for element in elements :
                block = toMakrdownBlock(element)

                if block == None :
                    continue

                if lastBlock == None :
                    markdownFile.write('\n\n')
                    markdownFile.write(block.getOpener())
                elif block.getId() != lastBlock.getId() :
                    markdownFile.write(lastBlock.getCloser())
                    markdownFile.write('\n\n')
                    markdownFile.write(block.getOpener())
                else :
                    markdownFile.write(block.getConnecter())

                lastBlock = block

                if block.getId() == Type.CONTENT :
                    text = ""
                    if element.data[language] == None :
                        text = element.data['fixed']
                    else :
                        text = element.data[language]

                    encodedText = text.replace('\*', '*').replace('\`', '`').replace('\_', '_')\
                                .replace('\~', '~').replace('\>', '>').replace('\[', '[')\
                                .replace('\]', ']').replace('\(', '(').replace('\)', ')')\
                                .replace('*', '\*').replace('`', '\`').replace('_', '\_')\
                                .replace('~', '\~').replace('>', '\>').replace('[', '\[')\
                                .replace(']', '\]').replace('(', '\(').replace(')', '\)')
                    
                    markdownFile.write(encodedText.lstrip())
                else :
                    markdownFile.write(element.data['original'])
                
            markdownFile.write(lastBlock.getCloser())
            markdownFile.flush()


    def convert(self, id) :
        elements = None
        with open(f'./rfcs/rfc{id}.txt', 'r') as rfcFile :
            elements = self.parser.parseV2(rfcFile.read())

        if elements == None : 
            return
        
        for element in elements :
            if element.data['type'] == Type.CONTENT :
                # prefix
                element.data['fixed'] = pf.prefix(element.data['original'])
                
                if self.doTranslate == False :
                    continue

                # translate
                for lang in self.languages :
                    if element.data[lang] == None :
                        text = element.data['fixed']
                        element.data[lang] = self.translator.translate(text, target=lang)
                        element.save()


        for lang in self.languages :
            self.writeFile(id, lang, elements)


        
