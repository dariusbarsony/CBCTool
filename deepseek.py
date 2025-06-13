import pandas as pd
from openai import OpenAI
from textExtract import textExtract
from io import StringIO
import re

filename = 'example.pdf'
filename2 = 'example2.pdf'
filename3 = 'example3.pdf'

example_csv = "Zeefkromme: M50 van zand fractie,Zeefkromme: D60/D10 ratio,Fractie tot 1 mm,Fractie tot 250 um,Fractie tot 63 um,Fractie tot 20 um,Fractie tot 2 um,Leemfractie,Organische Stof,Grof,Bodemvreemd"

def readData(filename):
    t = textExtract(filename)
    text = t.readPage()

    client = OpenAI(api_key="sk-68fb8d2b95c249dc8bb101c13df24c49", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "please try to fill in the following csv file format: {} with data from text: {} and return a csv file for each sample".format(example_csv, text)},
        ],
        stream=False
    )

    tables = response.choices[0].message.content
    print(tables)
    
    # find the required tables for a specific sample
    output = re.findall("\((\d+)\)\n```csv\n([\s\S][^```]*)", tables)

    # write sample output to csv files per sample
    for sample, data in output:
        df = pd.read_csv(StringIO(data), header=0)
        df.to_csv('data_sample_{}.csv'.format(sample))

readData(filename2)