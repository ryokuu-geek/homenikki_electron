import spacy
import ginza
import random
import os
import json
import re

apppath = os.path.dirname(os.path.dirname(__file__))
class Recognizer:
    def __init__(self) -> None:
        self.nlp = spacy.load('ja_ginza')
        self.modifier = (("に",'ni'),("で",'de'),("から",'kara'),("を",'wo'))
    def recognize(self, text):
        ret_value = {}
        doc = self.nlp(text)
        jutsugo = ginza.bunsetu_spans(doc)[-1]
        for i in [ginza.bunsetu_span(token) for token in jutsugo.lefts]:
            for j1, j2 in self.modifier:
                stri = str(i)
                if(stri[-1] == j1):
                    ret_value[j2] = stri 
            ret_value['jutsugo'] = str(jutsugo)
        return ret_value
    def fill_template(self, data={}):
        keys = set(data.keys())
        temp = ''
        tempkey = ''.join(sorted([i[0] for i in keys]))
        with open(os.path.join(apppath, 'home_template', 'template.json'), encoding='utf-8') as f:
            tempdic = json.load(f)
            templ = tempdic[tempkey]
            l = len(templ)
            temp = templ[random.randint(0, l-1)]
        for i in keys:
            temp = temp.replace(f'${{{i}}}', data[i])
        return temp
    """def add_template(self):
        with open(os.path.join('template','input.txt'), encoding='utf-8') as f:
            ip = f.readlines()
        with open(os.path.join('template', 'template.json'), encoding='utf-8') as f:
            new_json = json.load(f)
            for i in ip:
                key = ''.join(sorted([j.group()[2] for j in re.finditer(r'\$\{[^\}]+\}', i)]))
                try:
                    newl = set(new_json[key])
                except KeyError:
                    newl =  set()
                newl.add(i.strip())
                new_json[key] = sorted(newl)
        with open(os.path.join('template','newjson.json'), encoding='utf-8', mode='w') as f:
            json.dump(new_json, f, indent=4, ensure_ascii=False)"""


if __name__ == '__main__':
    r = Recognizer()
    l = r.fill_template(r.recognize(input('> ')))
    print(l)
    #print(r.fill_template(l))
    #r.add_template()