__author__ = 'brendan'

import helper_functions
import os
import tarfile

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'/data'


def download_url(url, destination_path, curl_path=r'C:/Users/brendan/Downloads/curl-7.38.0-win64/bin/curl'):
    """
    This is a quick and easy function that simulates clicking a link in your browser that initiates a download.
    It requires downloading the program CURL. Then the curl_path argument must point to whever your curl.exe executable
    is located.

    url:: the url from which data is to be downloaded.
    destination_path:: the downloaded file to be created.

    """
    os_string = '%s "%s" > %s' % (curl_path, url, destination_path)
    print os_string
    os.system(os_string)


def download_court_data(court_name, curl_path):
    """
    This function proceeds as follows:
        1) Given court_name, a string representing a CourtListener court, download_court_data first checks that there
        exists a subdirectory for court_name. This directory should contain within it a 'clusters' and 'opinions'
        sub-subdirectory. If these don't exist, they are created.
        2) download_court_data then compares how many files are in the 'clusters' sub-subdirectory to what is on the
        CourtListener server. If these numbers are not the same, all locally-saved files are deleted and re-downloaded
        and extracted to the 'clusters' sub-subdirectory.
        3) This process is then repeated for 'opinions'.
    """

    court_data_dir = data_dir + r'/%s' % court_name
    court_clusters_data_dir = court_data_dir + r'/clusters'
    court_opinions_data_dir = court_data_dir + r'/opinions'

    # Make a court data directory if we don't have one already
    if not os.path.exists(court_data_dir):
        os.makedirs(court_data_dir)
    if not os.path.exists(court_clusters_data_dir):
        os.makedirs(court_clusters_data_dir)
    if not os.path.exists(court_opinions_data_dir):
        os.makedirs(court_opinions_data_dir)

    ###################
    # FOR CLUSTERS DATA
    ###################
    court_metadata_url = 'https://www.courtlistener.com/api/rest/v3/clusters/?docket__court=%s' % court_name
    court_metadata = helper_functions.url_to_dict(court_metadata_url)
    num_files_on_server = court_metadata['count']
    files_in_dir = os.listdir(court_data_dir + r'/clusters')
    num_files_in_dir = len(files_in_dir)

    # If the number of files downloaded isn't the same as the number on the server
    if num_files_on_server != num_files_in_dir:
        print 'Re-downloading cluster data for court %s...' % court_name.upper()

        # Delete the files we currently have
        print '...deleting files...'
        for filename in files_in_dir:
            os.remove(r'%s/%s' % (court_clusters_data_dir, filename))

        # Download the .tar.gz file
        print '...downloading new .tar.gz file...'
        download_url(url='https://www.courtlistener.com/api/bulk-data/clusters/%s.tar.gz' % court_name,
                     destination_path=court_clusters_data_dir + r'/%s.tar.gz' % court_name,
                     curl_path=curl_path)

        # Extract it
        print '...extracting files...'
        with tarfile.open(court_clusters_data_dir + r'/%s.tar.gz' % court_name) as TarFile:
            TarFile.extractall(path=court_clusters_data_dir)
        # And delete .tar.gz file
        os.remove(r'%s/%s.tar.gz' % (court_clusters_data_dir, court_name))

        print '...done.'

    else:
        print "All server (cluster) files accounted for."

    ###################
    # FOR OPINIONS DATA
    ###################
    court_metadata_url = 'https://www.courtlistener.com/api/rest/v3/opinions/?docket__court=%s' % court_name
    court_metadata = helper_functions.url_to_dict(court_metadata_url)
    num_files_on_server = court_metadata['count']
    files_in_dir = os.listdir(court_data_dir + r'/opinions')
    num_files_in_dir = len(files_in_dir)

    # If the number of files downloaded isn't the same as the number on the server
    if num_files_on_server != num_files_in_dir:
        print 'Re-downloading opinions data for court %s...' % court_name.upper()

        # Delete the files we currently have
        print '...deleting files...'
        for filename in files_in_dir:
            os.remove(r'%s/%s' % (court_opinions_data_dir, filename))

        # Download the .tar.gz file
        print '...downloading new .tar.gz file...'
        download_url(url='https://www.courtlistener.com/api/bulk-data/opinions/%s.tar.gz' % court_name,
                     destination_path=court_opinions_data_dir + r'/%s.tar.gz' % court_name,
                     curl_path=curl_path)

        # Extract it
        print '...extracting files...'
        with tarfile.open(court_opinions_data_dir + r'/%s.tar.gz' % court_name) as TarFile:
            TarFile.extractall(path=court_opinions_data_dir)
        # And delete .tar.gz file
        os.remove(r'%s/%s.tar.gz' % (court_opinions_data_dir, court_name))

        print '...done.'

    else:
        print "All server (opinion) files accounted for."

# download_court_data('scotus', r'C:/Users/brendan/Downloads/curl-7.38.0-win64/bin/curl')
