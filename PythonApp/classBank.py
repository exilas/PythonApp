from urllib.parse import urlsplit
import datetime
import webCrawler.quaterlyDataFinder
import requests
import xlutils
from xlrd import open_workbook

#date du dernier jour trimestre précedent
def previous_quarter_date(ref):
    if ref.month < 4:
        return datetime.date(ref.year - 1, 12, 31)
    elif ref.month < 7:
        return datetime.date(ref.year, 3, 31)
    elif ref.month < 10:
        return datetime.date(ref.year, 6, 30)
    return datetime.date(ref.year, 9, 30)

#format Q1/Q2/Q3/Q4
def previous_quarter_number(ref):
    if ref.month < 4:
        return "4"
    elif ref.month < 7:
        return "1"
    elif ref.month < 10:
        return "2"
    return "3"


#année trim précèdent
def previous_quarter_year(ref):
    if ref.month < 4:
        return str(ref.year - 1)
    return str(ref.year)

class Bank(object):
    """Classe banque contenant le lien vers les résutlats, la racine du site etc..."""
    last_quarter_date = previous_quarter_date(datetime.date.today())
    last_quarter_number = 3 #previous_quarter_number(datetime.date.today())
    last_quarter_year = previous_quarter_year(datetime.date.today())
    last_quarter = 'Q{number} {year}'.format(number=last_quarter_number, year=last_quarter_year)
    path_temp_file = "C:\\Users\\alexisl-fdc\\Downloads\\"

    def __init__(self, bkname, results_url, tagQuarterReport):
        self.results_url = results_url
        self.base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(results_url))
        self.name = bkname
        self.tagQuarterReport = tagQuarterReport
        self.excel_url_result = ""

    def findQuaterlyReportUrl(self):
        self.excel_url_result = webCrawler.quaterlyDataFinder.parseResultsPage(self.results_url, self.tagQuarterReport, self.last_quarter_number,self.last_quarter_year)

    def dlQuaterlyReport(self):
        if self.excel_url_result == None:
            return 'Aucune url'

        resp = requests.get('{0}{1}'.format(self.base_url,self.excel_url_result))
        #remoteFile = urlopen(Request(series_url)).read()
        filePath= '{path}{bank}{quarter}.xls'.format(path=self.path_temp_file,bank=self.name,quarter=self.last_quarter)
        output = open(filePath, 'wb')
        output.write(resp.content)
        output.close()

        wb = open_workbook(filePath)
        return 'Fichier sauvegardé dans ' + filePath

    def readQuarterlyWb(self):
        return ""

    def __str__(self):
        return '{name}, lien pour les résultats du {quarter} : {url_link}'.format(name=self.name, quarter=self.last_quarter, url_link=self.excel_url_result)


class SocGen(Bank):
    
    def readQuarterlyWb(self):
        return "SocGen"