from flask import Flask, render_template, abort
from converter.converterv2 import Converter 
import os
import requests

doTranslate = os.environ['DO_TRANSLATE'] == '1'

app = Flask(__name__)
converter = Converter(doTranslate=doTranslate, languages=["ko"])

def getRFC(id) :
    response = requests.get(f'https://www.ietf.org/rfc/rfc{id}.txt')
    if response.ok :
        rfcFile = open(f'./rfcs/rfc{id}.txt','wb')
        rfcFile.write(response.content)
        rfcFile.close()
        converter.convert(id)
        return True
    else :
        return False


@app.route("/")
def root_page ():
    return render_template('index.html')

@app.route("/rfc<id>")
def rfc_page (id=None):
    try:
        id=int(id)
    except :
        abort(404)
    content = f'# rfc {id} file not found ... '
    if os.path.isfile(f'./mds/ko/rfc{id}.md'):
        rfcMdFile = open(f'./mds/ko/rfc{id}.md','r')
        content = rfcMdFile.read()
        rfcMdFile.close()
    elif os.path.isfile(f'./mds/ko/rfc{id}.txt.md'): # reuse legacy files
        rfcMdFile = open(f'./mds/ko/rfc{id}.txt.md','r')
        content = rfcMdFile.read()
        rfcMdFile.close()
    else :
        # make page
        getRFC(id)
        rfcMdFile = open(f'./mds/ko/rfc{id}.md','r')
        content = rfcMdFile.read()
        rfcMdFile.close()
        pass


    return render_template('rfc.html', id=id, content=content)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

