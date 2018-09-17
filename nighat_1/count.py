import openpyxl
from openpyxl import Workbook


dictionary = Workbook('pickles/dictionary.xlsx')
print(dictionary.active.title)