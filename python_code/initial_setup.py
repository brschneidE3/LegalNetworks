__author__ = 'brsch'

import os
import download_data_batch

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'

# Download and unzip citations.csv
download_data_batch.download_url(
    url='https://www.courtlistener.com/api/bulk-data/citations/all.csv.gz',
    destination_path=r'C:\PyCharm\Projects\all.gz')
