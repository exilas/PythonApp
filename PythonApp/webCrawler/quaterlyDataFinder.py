#module de recherche des dernieres series de donnees trimestrielles pour les banques (CET1/T1/T2/RWA/NPL...)
import requests
import PyPDF2
from lxml import html
from bs4 import BeautifulSoup
import io
from urllib.request import Request, urlopen
from urllib.parse import urlsplit

#Q1/2/3/4 => first,second,third,fourth etc...
def quarter_in_letter(qter):
    if qter == '1':
        return "first"
    elif qter == '2':
        return "second"
    elif qter == '3':
        return "third"
    return "fourth"


#le fichier est il au bon trimestre
def isGoodQuaterlyDate(string, quarter, year):
    quarter1 = 'Q{0}'.format(quarter) #Q3
    quarter2 = '{0}Q'.format(quarter) #3Q
    quarterYear1 = 'Q{0}{1}'.format(quarter,year) #Q32016
    quarterYear2 = '{0}Q{1}'.format(quarter,year) #3Q2016
    quarterYear3 = 'Q{0}{1}'.format(quarter,year[-2:]) #Q316
    quarterYear4 = '{0}Q{1}'.format(quarter,year[-2:]) #3Q16
    quarterLetter = quarter_in_letter(quarter)

    isGoodDate = False
    if ((string.find(quarter1) >= 0 or string.find(quarter2) >= 0 or string.find(quarterLetter) >= 0) and string.find(year) >= 0) \
        or (string.find(quarterYear1) >= 0 or string.find(quarterYear2) >= 0 or string.find(quarterYear3) >= 0 or string.find(quarterYear4) >= 0):
        isGoodDate = True

    return isGoodDate

#le fichier est il le bon
def isGoodFileName(urlText, urlLink, urlFileName,urlTitle, tag):
    hasTag = urlText.find(tag) >= 0 or urlFileName.find(tag) >= 0 or urlTitle.find(tag) >= 0
    if urlFileName.find(".") >= 0 and urlFileName.find(".XLS") < 0  :
        return False
    return hasTag

#la chaine de caractere est il celui du bon trimestre ?
def isQuaterlyFile(urlText, urlLink, urlFileName, urlTitle, tag, quarter, year):
    urlText = urlText.upper()
    urlLink = urlLink.upper()
    urlFileName = urlFileName.upper()
    urlTitle = urlTitle.upper()
    tag = tag.upper()

    isGoodDateText = isGoodQuaterlyDate(urlText,quarter,year)
    isGoodDateTitle = isGoodQuaterlyDate(urlTitle,quarter,year)
    isGoodDateFileName = isGoodQuaterlyDate(urlFileName,quarter,year)
    isQuarterlyExcel = isGoodFileName(urlText, urlLink, urlFileName, urlTitle, tag)

    if (isGoodDateText or isGoodDateFileName or isGoodDateTitle) and isQuarterlyExcel:
        return True
    return False

#Determination du lien excel vers les resultats du trimestre par banque
def parseResultsPage(myurl, tag, quarter,year):
    page = requests.get(myurl).text
    soup = BeautifulSoup(page)
    allLinks = soup.find_all("a")
    for link in allLinks:
        urlLink = link.get("href")
        urlTitle = link.get("title")
        if urlLink == None:
            continue
        urlText = link.text
        urlTitleText = ""
        if urlTitle != None:
            urlTitleText = urlTitle        
        urlFileName = urlsplit(urlLink).path.split('/')[-1]
        if link != None and link != "" :
            if isQuaterlyFile(urlText,urlLink,urlFileName,urlTitleText, tag, quarter, year):
                return urlLink

