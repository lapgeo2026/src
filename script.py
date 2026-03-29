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


def convertPdfToCsv(input):
    # Use a breakpoint in the code line below to debug your script.
    assert isinstance(input, object)
    file: str = str(input)
    
    # Path to your PDF file
    pdf_path = input
    output_path = input.replace(".pdf",".csv")

    try:
      
      # Save all tables to CSV
      tabula.convert_into(pdf_path, output_path, output_format="csv", pages="all")

      print("Rendering process completed")
      print(f'File generated: {input}.csv')  # Press Ctrl+F8 to toggle the breakpoint.

    except FileNotFoundError:
      print("Error: PDF file not found.")
      
    #with open(output_path, 'r', encoding='utf-8', errors='ignore') as file:
    #  lines = file.readlines()
        
    #  regex = re.compile(pattern)
    #  matches = []
    
    #  for line_number, line in enumerate(lines):
    #    if re.search(regex, line):
    #        matches.append((line_number + 1, line.strip()))

    #  if matches:
    #    print(f"Found string {pattern} matches in {output_path}:")
        
    #    for line_number, line in matches:
    #      print(f"- Line {line_number}: {line.strip()}")
    #  else:
    #      print(f"No matches found in {pdf_path} for the given string {pattern}.")

    de=pd.DataFrame(columns=["Date", "DateValeur", "Description", "Debit", "Credit"])
    df=pd.read_csv(f"{output_path}", sep=',', on_bad_lines='skip', quoting=csv.QUOTE_NONE)
    de=df.drop(labels=["Débit"], axis=1)
    print(df)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jpype.startJVM()
    
    filePattern = input("pattern to search for filename: ")
    #pattern = input("pattern to search in files: ")
    localpath = "C:/Users/Georges/lang/python/"
    localdir=Path(localpath)
    for filename in localdir.rglob("*" +filePattern +"*.pdf"):
      convertPdfToCsv(str(filename))
