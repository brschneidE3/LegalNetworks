__author__ = 'brsch'

import os
import download_data_batch
import gzip
import consolidate_data

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'

######################
# GET MASTER EDGE LIST
######################

# 1) DOWNLOAD CURL AND PLACE PATH TO CURL EXECUTABLE HERE:
curl_path = r'C:\Users\brsch\Downloads\curl-7.49.1-win64-mingw\bin\curl'

# 2) DOWNLOAD CITATIONS ZIP FILE
destination_path = r'%s\all.gz' % data_dir  # Don't change this
download_data_batch.download_url(
    url='https://www.courtlistener.com/api/bulk-data/citations/all.csv.gz',
    destination_path=destination_path,
    curl_path=curl_path)

# 3) UNZIP FILE INTO CITATIONS.CSV
with gzip.open(destination_path, 'rb') as gzip_file:
    file_content = gzip_file.read()
    gzip_file.close()
with open(data_dir + r'\citations.csv', 'w') as csv_file:
    csv_file.write(file_content)
    csv_file.close()

# 4) DELETE LEFTOVER GZ FILE
os.remove(destination_path)

#######################
# GET SCOTUS JSON FILES
#######################

# 5) Download the .json's corresponding to each scotus decision
download_data_batch.download_court_data('scotus', r'C:\Users\brsch\Downloads\curl-7.49.1-win64-mingw\bin\curl')

# 6) Create citations_sublist.csv in the scotus directory
master_citer_as_key, master_cited_as_key = consolidate_data.get_master_edge_dicts()
consolidate_data.create_edge_sublist('scotus', master_cited_as_key)
