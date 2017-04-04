# -*- coding:utf-8 -*-
  
import csv

# with open('eggs.csv', 'w', newline='') as csvfile:
#     #spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     spamwriter = csv.writer(csvfile)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

csvfile = open('eggs.csv', 'a+', newline='');
#spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter = csv.writer(csvfile)
spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
spamwriter.writerow([1, 1, 1, 1, 1])
csvfile.close()