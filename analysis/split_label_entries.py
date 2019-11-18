# -*- coding: utf-8 -*-

import csv
import sys
import pandas as pd

if __name__ == '__main__':
    file_path = sys.argv[1]
    new_file_path = 'new_file.csv'
    
    # read csv
    print('---------reading csv------------')
    df = pd.read_csv(file_path).fillna('')
    
    print('------------splitting up labels--------------')
    new_table = []
    for index, row in df.iterrows():
        
        if not row[2]:
            temp = []
            for i in range(len(row)):
                temp.append(row[i])
            new_table.append(temp)
            continue

        labels = row[2].split('/')
        for label in labels:
            temp = []
            for i in range(len(row)):
                if i != 2:
                    temp.append(row[i])
                else:
                    temp.append(label.strip())
            new_table.append(temp)
    
    # write data to file
    print('---------writing to file------------')
    with open(new_file_path, encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(df.columns)
        writer.writerows(new_table)
    f.close()
    