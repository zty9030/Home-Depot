# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 16:39:15 2016

@author: williamz
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
#import urllib2
import sqlite3
import re
import time
import nltk
from nltk.stem.porter import PorterStemmer
import sys

def text_process(s):
    s = s.lower()
    s = re.sub(r'[^a-z ]','',s)
    
    token_list = nltk.word_tokenize(s)
    STEMMER = PorterStemmer()
    print 'Stemming...'
    stemming = [STEMMER.stem(tok.decode('utf-8',errors='ignore')) for tok in token_list]
    content = [w for w in stemming]
    return ' '.join(content)

def goo_search(text):
    q = '+'.join(text.split())
    url = 'https://www.google.co.uk/search?q='+q
    r = requests.get(url)
    bs = BeautifulSoup(r.text,'lxml')
    spell = bs.find_all('a',class_ = 'spell')
    if len(spell)>0:
        return spell[0].getText()
    else:
        return text
    
search = raw_input('Enter search: ')
print '-'*30
print 'Checking with Google'
search = goo_search(search)

print 'Correction: %s' % search
search = text_process(search)

time.sleep(1)

conn = sqlite3.connect('product.db')
cur = conn.cursor()

search_term = search.split()

slec = 'select * from title '
for i in search_term:
    slec +="union select 'q' as prod_id ,'%s' as term, 1 as tfidf " % i

print 'Searching database...'

query = "select b.prod_id, sum(b.tfidf) as su from (%s) as a join title as b on a.term = b.term where a.prod_id = 'q' group by b.prod_id order by su desc" % slec
#print query
cur.execute(query)
result = cur.fetchall()[:10]

print 'Fetching result...'
prod = pd.read_csv('Dataset/product.csv')
print '-'*30
print 'Prod_id,Prod_title,Relevace'
print '-'*30
for j in result:
    print '|',j[0],'|',prod.product_title[prod.prod_id==j[0]].values[0],'|',round(j[1]*3,2)
    time.sleep(0.5)
print '-'*30
    
    
    
    
    
    
    
    

