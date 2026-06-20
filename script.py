# python code for your bank account
import tabula
import pandas as pd
from jpype import *
import jpype.imports
import re
import csv
from pathlib import Path


def convertPdfToCsv(localdir, filePattern="RLV"):
    # Path to your PDF file
    pdf_path = localdir
    i = 0
    csv = pd.DataFrame()
    result_csv = pd.DataFrame()
    print(localdir)
    print(filePattern)
    
    lst_files_pdf = list(enumerate(localdir.rglob(filePattern +"*.pdf")))
    lst_files_csv = list(enumerate(localdir.rglob(filePattern +"*.csv"), start=len(lst_files_pdf)))
    
    files = lst_files_pdf + lst_files_csv
    for i, filename in files:
        print(filename)
        if "pdf" in str(filename):
            output_path = str(filename).replace(".pdf","")
            f = Path(f"{output_path}.csv")
            f.unlink(missing_ok=True)
            try:
                # Save all tables to CSV
                tabula.convert_into(filename, output_path, output_format="csv", pages="all")

            except FileNotFoundError:
                print("Error: PDF file not found.")
        else:
            output_path = str(filename)

    for sep in [',', ';', '|', '\t']:
        try:
            csv = pd.read_csv('file.csv', sep=sep)
            if csv.shape[1] > 1:  # more than 1 column means sep worked
                break
               
        except Exception:
             continue
      
        if i == 1:
            result_csv = csv
        else:
            result_csv = pd.concat([result_csv, csv])
        print("Rendering process completed")
        if not "csv" in str(filename):
            print(f'File generated: {output_path}.csv')  
    
    print("********* RELEVE *********")
    csv_filtered_Credit = pd.DataFrame()
    csv_filtered_Credit = pd.read_csv(output_path)
    csv_filtered_Debit = pd.DataFrame()
    csv_filtered_Debit = pd.read_csv(output_path)
    #result_csv.columns = ["Credit", "Debit"]
    print(csv)
    if not result_csv.empty:
        print(result_csv)
    print(result_csv.columns)
    pattern = r"[+-]?(?:\d*\.\d+|\d+\.\d*)" #only float
    for column_name in result_csv.columns:
        print(column_name)
        if column_name != None:
            if ("Debit" in column_name) and not ("Credit" in column_name):
               #mask2 = csv_filtered_Debit[column_name].notna()
               #mask2 &= csv_filtered_Debit[column_name].contains(pattern, regex=True)              
               csv_filtered_Debit = csv_filtered_Debit.rename(columns={column_name: "Debit"})
            elif ("Credit" in column_name):
               #mask1= csv_filtered_Credit[column_name]
               #mask1 = csv_filtered_Credit[column_name].str.contains(pattern, regex=True)
               csv_filtered_Credit = csv_filtered_Credit.rename(columns={column_name: "Credit"})               
 

    #csv_filtered_Credit = csv_filtered_Credit.loc[:, csv_filtered_Credit.columns.str.contains("Date|Libelle|Operation|Credit")]
    #csv_filtered_Debit = csv_filtered_Debit.loc[:, csv_filtered_Debit.columns.str.contains("Date|Libelle|Operation|Debit")]
            
    print("********* CREDIT: credit_rlv.csv *********")
    csv_filtered_Credit.to_csv("credit_rlv.csv", index=False)
    print(csv_filtered_Credit)
    print("********* DEBIT: debit_rlv.csv *********")
    csv_filtered_Debit.to_csv("debit_rlv.csv", index=False)
    print(csv_filtered_Debit)
    

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jpype.startJVM()
    
    filePattern = input("pattern to search for filename (defaut = RLV): ")
    localpath = "C:/Users/Georges/lang/python/"
    localdir=Path(localpath)
    convertPdfToCsv(localdir, filePattern)
