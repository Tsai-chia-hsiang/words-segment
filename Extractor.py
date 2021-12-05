#!/usr/bin/python3
import requests
import jieba.analyse as jAnalyse
import nltk
import pathlib
import os
import time
from bs4 import BeautifulSoup as bs
import random
import requests
from requests_toolbelt.adapters import source


class Extractor():
    def __init__(self) -> None:
       
        self.packege_path = pathlib.Path(__file__).parent.absolute()
        self.chi_noise = []
        self.eng_noise = []
        self.__read_noise()
        #self.proxies = self.__proxy()

    def __read_noise(self):
        with open(os.path.join(self.packege_path, "chi_noise.txt"), "r") as cn:
            for line in cn.readlines():
                self.chi_noise.append(line.strip())

        with open(os.path.join(self.packege_path, "eng_noise.txt"),"r") as en:
            for line in en.readlines():
                self.eng_noise.append(line.strip())
    
    def clean(self, keypattern:list):

        final_result = []
        for oword in keypattern:

            word = oword.strip()
            if len(word) == 0:
                continue

            ok = True
            for noise in self.chi_noise:
                if noise in word:
                    ok = False
                    break
            if ok:
                final_result.append(oword)

        return final_result
        
    def chi_extraction(self,para,engine,topk = 5):

        keypattern = []
        stat_code = 200

        if engine == "gais":
            keypattern, stat_code = self.gais_extraction(para)

        if engine == "jieba":
            keypattern = self.jextraction(para)

        result = self.clean(keypattern)
        final_result = []
        idx = 0
        for keyword in result:
            final_result.append(keyword)
            idx += 1
            if idx == topk:
                break

        return final_result, stat_code

    def gais_extraction(self, paragraph: str):

        gais_url = "http://gais.org.tw:5721/api/segment"
        gais_request = requests.session()
        format_data = {"content": paragraph.encode('utf-8')}
        result = gais_request.post(gais_url, data=format_data)

        if not result.status_code == 200:
            return [], result.status_code

        k = eval(result.text)
        key_pattern = k['Keyterms'].split(",")

        value = []
        for pattern in key_pattern:
            value.append(pattern)

        return value,result.status_code
    
    def jextraction(self, paragraph:str):
        tag = jAnalyse.extract_tags(paragraph, allowPOS=['n','ns','nr','nz'],topK=20)
        value = []
        for t in tag:
            value.append(t)
        return value 


if __name__ == "__main__":
    extr = Extractor()
   