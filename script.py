# python code for your bank account
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
    
    lst_files_pdf = list(enumerate(localdir.rglob("*" +filePattern +"*.pdf")))
    lst_files_csv = list(enumerate(localdir.rglob("*" +filePattern +"*.csv"), start=len(lst_files_pdf)))
    
    files = lst_files_pdf + lst_files_csv
    for i, filename in files:
        print(filename)
        if "pdf" in str(filename):
            output_path = str(filename).replace(".pdf","")
            print(filename) 
            try:
                # Save all tables to CSV
                tabula.convert_into(filename, output_path, output_format="csv", pages="all")

            except FileNotFoundError:
                print("Error: PDF file not found.")
        else:
            output_path = str(filename)

        if "pdf" in str(filename):
            csv = pd.read_csv(f"{output_path}", sep=',', on_bad_lines='skip')
        else:
            csv = pd.read_csv(f"{output_path}", sep=';', on_bad_lines='skip')
      
        if i == 1:
            result_csv = csv
        else:
            result_csv = pd.concat([result_csv, csv])
      
        print("Rendering process completed")
        if not "csv" in str(filename):
            print(f'File generated: {output_path}.csv')  
    
    print("********* RELEVE *********")
    if not result_csv.empty:
        print(result_csv)

    csv_filtered_Credit = pd.DataFrame()
    csv_filtered_Debit = pd.DataFrame()
    result_csv.columns = result_csv.columns.str.replace("é", "e")
    csv_filtered_Credit = result_csv.copy()
    csv_filtered_Debit = result_csv.copy()
    print(result_csv.columns)
    pattern = r"[+-]?(?:\d*\/\d+|\d+\.\d*|\d+)" #any float
    for column_name in result_csv.columns:
        if "Credit" in column_name:
          csv_filtered_Credit = csv_filtered_Credit[csv_filtered_Credit[column_name].notna() & csv_filtered_Credit[column_name].str.contains(pattern, regex=True)]
          csv_filtered_Credit = csv_filtered_Credit.rename(columns={column_name: "Credit"})
        elif ("Debit" in column_name) or ("Unnamed" in column_name):
          csv_filtered_Debit = csv_filtered_Debit[csv_filtered_Debit[column_name].notna() & csv_filtered_Debit[column_name].str.contains(pattern, regex=True)]   
          csv_filtered_Debit = csv_filtered_Debit.rename(columns={column_name: "Debit"})
    
    csv_filtered_Credit = csv_filtered_Credit.loc[:, csv_filtered_Credit.columns.str.contains("Date|Libelle|Credit")]
    csv_filtered_Debit = csv_filtered_Debit.loc[:, csv_filtered_Debit.columns.str.contains("Date|Libelle|Debit")]
            
    print("********* CREDIT: credit_rlv.csv *********")
    csv_filtered_Credit.to_csv("credit_rlv.csv", index=False)
    print("********* DEBIT: debit_rlv.csv *********")
    csv_filtered_Debit.to_csv("debit_rlv.csv", index=False)
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jpype.startJVM()
    
    filePattern = input("pattern to search for filename: ")
    localpath = "C:/Users/Georges/lang/python/"
    localdir=Path(localpath)
    convertPdfToCsv(localdir, filePattern)
