from google.cloud import translate
import os
import hashlib

class Translator:
    def __init__(self, location = "global", project_id = "valid-amplifier-406115") :
        self.client = translate.TranslationServiceClient()
        self.location = "global"
        self.project_id = "valid-amplifier-406115"
        self.parent = f"projects/{project_id}/locations/{location}"
        try:
            os.mkdir("./cache")
        except:
            pass


    def translate(self, text, target = "ko"):
        result = ""
        hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        cachePath = f'./cache/{hash}.txt'
        if os.path.isfile(cachePath) :
            print("cache available")
            cache = open(cachePath, 'r')
            result = cache.read()
            cache.close()
        else :
            result = self.client.translate_text(
                request={
                    "parent": self.parent,
                    "contents": [text],
                    "mime_type": "text/plain",
                    "source_language_code": "en-US",
                    "target_language_code": target,
                }
            ).translations[0].translated_text

            cache = open(cachePath, 'w')
            cache.write(result)
            cache.close()
        #print(result)
        return result
