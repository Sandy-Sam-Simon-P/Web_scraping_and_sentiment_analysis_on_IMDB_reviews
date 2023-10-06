import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from dotenv import load_dotenv

if not load_dotenv(): # This condition will exit the program if there is no .env file
    print("Could not load .env file or it is empty. Please check if it exists and is readable.")
    exit(1)

# loading environmental variables
input = os.environ.get("Input_file_path")
Extracted_files = os.environ.get("Extracted_files")

def web_scrap(filepath): # main function to extract the data from thw website
    excel_data = pd.read_excel(filepath)
    data_frame = pd.DataFrame(excel_data)
    # iterrating the rows in the excel file
    for index, row in data_frame.iterrows():
        print("Movie : ",row['Movie_name'], "and URL_ID : ", row['URL_ID'])
        req = requests.get(row['URL'])
        soup = BeautifulSoup(req.content, "html.parser")
        b= [""]
        All_divs = soup.find_all('div', {'class': 'content'})
        for div in All_divs:
            a = div.find_all('div', {'class': 'text show-more__control'})
            b += a
        final_content = ""
        for i in b:
            final_content += str(b)
        # Removing the HTML tags from the data
        clean = re.compile('<.*?>')
        res = re.sub(clean,'',final_content)
        # creating text files with the movie name and saving the data in those files
        file = open(f"{Extracted_files}/{row['Movie_name']}.txt","w+", encoding="utf-8")
        file.write(res)
        file.close
        
# calling the function
web_scrap(input)

