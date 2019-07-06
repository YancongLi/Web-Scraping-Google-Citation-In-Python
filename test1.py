from bs4 import BeautifulSoup
import requests
import csv

page_link = 'https://scholar.google.ca/citations?view_op=view_org&hl=en&org=13655899619131983200&after_author=sdM6AL_F__8J&astart=530'

page_response = requests.get(page_link, timeout=5)

page_content = BeautifulSoup(page_response.content, "html.parser")

subUrls = []

for i in range(3, 13):
    url = page_content.select('#gsc_sa_ccl > div:nth-child('+ str(i) +') > div > div > h3 > a')
    # print(url)
    soupUrlTag = url[0]
    actualUrl = 'https://scholar.google.ca' + soupUrlTag.attrs["href"]
    # print(actualUrl)
    subUrls.append(actualUrl)

profNo = 1

class Prof():
    def __init__(self):
        self.name = ""
        self.picLink = ""
        self.title = ""
        self.citationTotal = ""
        self.hIndex = ""
        self.i10Index = "" 

profList = []

for subUrl in subUrls:

    prof = Prof()

    print(str(profNo) + ": ")
    sub_page_response = requests.get(subUrl, timeout=5)
    sub_page_content = BeautifulSoup(sub_page_response.content, "html.parser")
    
    prof.name = sub_page_content.select('#gsc_prf_in')[0].text
    print('Prof Name: ' + prof.name)
    
    prof.picLink = 'https://scholar.google.ca'+ sub_page_content.select('#gsc_prf_pup-img')[0].attrs["src"]
    print('Picture Link: ' + prof.picLink)
    
    prof.title = sub_page_content.select('#gsc_prf_i > div:nth-child(2)')[0].text
    print('Title: ' + prof.title)

    prof.citationTotal = sub_page_content.select('#gsc_rsb_st > tbody > tr:nth-child(1) > td:nth-child(2)')[0].text
    print('Citation total: ' + prof.citationTotal)

    # Citation by year (I am not sure what this means)

    prof.hIndex = sub_page_content.select('#gsc_rsb_st > tbody > tr:nth-child(2) > td:nth-child(2)')[0].text
    print('h-index: ' + prof.hIndex)

    prof.i10Index = sub_page_content.select('#gsc_rsb_st > tbody > tr:nth-child(3) > td:nth-child(2)')[0].text
    print('i10-index: ' + prof.i10Index)

    print("--------------------------------------------------------")
    profNo += 1

    profList.append(prof)

with open('data.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Picture Link', 'Title', 'Citation Total', 'h Index', 'i-10Index'])
    for prof in profList:
        writer.writerow([prof.name, prof.picLink, prof.title, prof.citationTotal, prof.hIndex, prof.i10Index])