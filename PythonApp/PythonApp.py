import requests
import PyPDF2
from lxml import html
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from urllib.request import Request, urlopen
import xlutils
from xlrd import open_workbook
import classBank



def readSantanderQuaterlySeries(series_url):   
    resp = requests.get(series_url)
    remoteFile = urlopen(Request(series_url)).read()
    filePath="C:\\Users\\alexisl-fdc\\Downloads\\temp.xls"
    output = open(filePath, 'wb')
    output.write(resp.content)
    output.close()

    wb = open_workbook(filePath)
    for sheet in wb.sheets():
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

    items = []
    rows = []
    for row in range(1, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = Arm(*values)
        items.append(item)

    for item in items:
        print(item)
        print("Accessing one single value (eg. DSPName): {0}".format(item.dsp_name))
        print()
        
    return res

banks = []
banks.append( classBank.Bank("Danske Bank","https://www.danskebank.com/en-uk/ir/Reports/Pages/financial-reports.aspx","FINANCIAL STATEMENTS"))
banks.append( classBank.Bank("BBVA", "http://shareholdersandinvestors.bbva.com/TLBB/tlbb/bbvair/ing/financials/reports/index.jsp","RESULTS"))
banks.append( classBank.Bank("BNP","https://invest.bnpparibas.com/en/results","Quarterlyseries"))
banks.append( classBank.Bank("Credit Agricole","https://www.credit-agricole.com/finance/finance/communiques-de-presse-financiers","test"))
banks.append( classBank.Bank("Santander","http://www.santander.com/csgs/Satellite/CFWCSancomQP01/en_GB/Corporate/Shareholders-and-Investors/Financial-and-economic-information/Results.html","SERIES"))
banks.append( classBank.Bank("Societe Generale","https://backend.societegenerale.com/en/measuring-our-performance/information-and-publications/financial-results","SG_SERIES_TRIM"))
banks.append( classBank.Bank("Banco Popular Espanol","http://www.grupobancopopular.com/EN/INVESTORRELATIONS/FINANCIALINFORMATION/Paginas/InformesTrimestrales.aspx","QUARTERLY REPORT"))
banks.append( classBank.Bank("Nordea", "http://www.nordea.com/en/investor-relations/reports-and-presentations/select-reports-and-presentations/group-interim-reports/","FACTBOOK"))
banks.append( classBank.Bank("KBC", "https://www.kbc.com/fr/rapports-trimestriels#tab","CONSOLIDATED_RESULTS"))


for bank in banks:
    bank.findQuaterlyReportUrl()
    bank.dlQuaterlyReport()
    print(bank)