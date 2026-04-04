# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tabula
import pandas as pd
from jpype import *
import jpype.imports
import re
import csv
from pathlib import Path


def convertPdfToCsv(localdir, filePattern):
    # Path to your PDF file
    pdf_path = localdir
    i = 0
    csv = pd.DataFrame()
    result_csv = pd.DataFrame()
    print(localdir)
    print(filePattern)
    
    for i, filename in enumerate(localdir.rglob("*" +filePattern +"*.pdf"), start=1):
        output_path = str(filename).replace(".pdf","")
        print(filename)
        try:
      
          # Save all tables to CSV
          tabula.convert_into(filename, output_path, output_format="csv", pages="all")
          csv = pd.read_csv(f"{output_path}", sep=',', on_bad_lines='skip')
      
          if i == 1:
              result_csv = csv
          else:
              result_csv = pd.concat([result_csv, csv])
      
          print("Rendering process completed")
          print(f'File generated: {output_path}.csv')

        except FileNotFoundError:
          print("Error: PDF file not found.")
      
    print("********* RELEVE *********")
    print(result_csv)
    
    csv_filtered_Credit = pd.DataFrame()
    csv_filtered_Debit = pd.DataFrame()
    csv_filtered_Credit = result_csv.copy()
    csv_filtered_Debit = result_csv.copy()
    print(result_csv.columns)
    pattern = r"[+-]?(?:\d*\/\d+|\d+\.\d*|\d+)" #any float
    csv_filtered_Credit = csv_filtered_Credit[csv_filtered_Credit['Crédit'].notna() & csv_filtered_Credit['Crédit'].str.contains(pattern, regex=True)]
    csv_filtered_Debit = csv_filtered_Debit[csv_filtered_Debit['Unnamed: 4'].notna() & csv_filtered_Debit['Unnamed: 4'].str.contains(pattern, regex=True)]
    print("********* CREDIT *********")
    print(csv_filtered_Credit[['Date Date de Valeur', 'Crédit']])
    print("********* DEBIT *********")
    csv_filtered_Debit = csv_filtered_Debit.rename(columns={'Unnamed: 4': 'Débit'})
    print(csv_filtered_Debit[['Date Date de Valeur', 'Débit']])
    
    csv_filtered_Credit.to_csv("credit.csv", index=False)
    csv_filtered_Debit.to_csv("debit.csv", index=False)
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jpype.startJVM()
    
    filePattern = input("pattern to search for filename: ")
    localpath = "C:/Users/Georges/lang/python/"
    localdir=Path(localpath)
    convertPdfToCsv(localdir, filePattern)
