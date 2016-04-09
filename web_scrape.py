# https://automatetheboringstuff.com/chapter11/

# http://docs.python-guide.org/en/latest/scenarios/scrape/

from lxml import html
import requests

page = requests.get('http://www.spine-health.com/forum/discussion/90448/pain/lower-back-pain/running-out-options')
tree = html.fromstring(page.content)
vanilla = tree.xpath('//*[@id="Discussion_90448"]/div/div[2]/div/div[1]/text()[2]')
print vanilla

page2 = requests.get('http://www.spine-health.com/forum/discussion/90489/pain/lower-back-pain/chronic-lower-back-pain-after-pregnancy')
tree2 = html.fromstring(page2.content)
preg = tree2.xpath('//*[@id="Discussion_90489"]/div/div[2]/div/div[1]/text()')
print preg

page3 = requests.get('http://www.spine-health.com/forum/discussion/44887/pain/lower-back-pain/back-pain-worse-and-different-after-cortisone-injection')
tree3 = html.fromstring(page3.content)
surg = tree3.xpath('//*[@id="Discussion_44887"]/div/div[2]/div/div[1]/text()[2]')
print surg

page4 = requests.get('http://www.spine-health.com/forum/discussion/90441/pain/lower-back-pain/when-do-you-consider-surgery')
tree4 = html.fromstring(page4.content)
cons = tree4.xpath('//*[@id="Discussion_90441"]/div/div[2]/div/div[1]/text()[1]')
print cons
cons2 = tree4.xpath('//*[@id="Discussion_90441"]/div/div[2]/div/div[1]/text()[2]')
print cons2

num = range(1,7)

corpus = []
for i in num:
    text = 'cons' + str(i)
    corpus.append(text)

print corpus

forrest = []
for i in num:
    wood = 'tree' + str(i)
    forrest.append(wood)

print forest

element = []
for i in num:
    atom = """//*[@id="Discussion_90441"]/div/div[2]/div/div[1]/text()[""" + str(i) + ']'
    element.append(atom)

print element

dict = {}
for i,j in zip(corpus,element):
    dict[i] = tree4.xpath(j)