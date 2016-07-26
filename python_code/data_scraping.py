
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""
__author__ = 'brsch'

import helper_functions
import os
import time
import json

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'

# Unchanging courtlistener API info

site_dict_url = 'https://www.courtlistener.com/api/rest/v3/'
site_dict = helper_functions.url_to_dict(site_dict_url)
# clusters_url = site_dict['clusters']

starting_page = 2161
clusters_url = 'https://www.courtlistener.com/api/rest/v3/clusters/?page=%s' % starting_page
opinions_url = site_dict['opinions']


def pull_cases_by_court(court_id):
    """
    Given a court id, pull_cases_by_court will iterate through every cluster online, check if the case (cluster &
    opinion) corresponding to that cluster has been downloaded ( via is_downloaded() ) and will build up a list of
    [case_number, parent_directory] tuples that will enable quick iteration and creation of a dictionary of cases
    in other functions via Class_Case.json_to_case.
    :param court_id: court id by which to filter
    :return:
        case_numbers_and_parent_directories:
            list of the case numbers and the parents directories where they are located
    """
    start = time.time()

    # Initial info about the online clusters database
    clusters_dict = helper_functions.url_to_dict(clusters_url)
    num_to_inspect = clusters_dict['count']
    inspected = 0.
    page = starting_page

    # List of case numbers and parent directories that will eventually be returns
    case_numbers_and_parent_directories = []

    # Make sure we already have subdirectories for this court. Create them if not.
    subdirectories = [data_dir + r'\clusters\%s' % court_id, data_dir + r'\opinions\%s' % court_id]
    for subdir in subdirectories:
        if not os.path.isdir(subdir):
            os.makedirs(subdir)

    # As long as there are more pages to iterate through
    while clusters_dict['next'] is not None:

        # Iterate through each cluster on current page
        for individual_cluster in clusters_dict['results']:
            time.sleep(2)  # Make sure we don't overload the server
            inspected += 1.
            pct_inspected = inspected / num_to_inspect

            url_id_number = individual_cluster['resource_uri'].rsplit('/')[-2]
            new_cluster_url = site_dict_url + r'clusters/%s' % url_id_number
            new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)

            new_cluster_docket_url = new_cluster_dict['docket']
            new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)

            try:
                new_cluster_court = new_cluster_docket_dict['court'].rsplit('/')[-2]

                if new_cluster_court == court_id:
                    file_number = new_cluster_dict['citation_id']
                    parent_directory = court_id
                    case_numbers_and_parent_directories.append([file_number, parent_directory])

                    if not is_downloaded(file_number, parent_directory):
                        download_case(new_cluster_dict, file_number, parent_directory)
                    # print '%s DOWNLOADED. (%s)' % (file_number, pct_inspected)

                else:
                    pass
                    # print '%s passed. (%s)' % (new_cluster_dict['citation_id'], pct_inspected)

            except KeyError:  # If there is no court data
                pass

        print 'page %s checked. (%s)' % (page, pct_inspected)
        page += 1
        clusters_dict = helper_functions.url_to_dict(clusters_dict['next'])

    # Iterate through each cluster on last page
    for individual_cluster in clusters_dict['results']:
        time.sleep(2)  # Make sure we don't overload the server

        new_cluster_url = individual_cluster['cluster']
        new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
        new_cluster_docket_url = new_cluster_dict['dockets']
        new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)
        try:
            new_cluster_court = new_cluster_docket_dict['court']

            if new_cluster_court == court_id:
                file_number = new_cluster_dict['citation_id']
                parent_directory = court_id
                case_numbers_and_parent_directories.append([file_number, parent_directory])

                if not is_downloaded(file_number, parent_directory):
                    download_case(new_cluster_dict, file_number, parent_directory)
        except KeyError:  # If there is no court data
            pass

    finish = time.time()
    elapsed = finish - start
    print "Download took %s minutes" % elapsed / 60.
    return case_numbers_and_parent_directories


def is_downloaded(file_number, parent_directory):
    """
    Should check if corresponding cluster & opinion json files have been downloaded to appropriate path:
        data_dir + r'\clusters\COURT NAME\FILE NUMBER.json
                            &
        data_dir + r'\opinions\COURT NAME\FILE NUMBER.json
    Return True or False.
    """
    op_downloaded = os.path.exists(data_dir + r'\opinions\%s\%s.json' % (file_number, parent_directory))
    cl_downloaded = os.path.exists(data_dir + r'\clusters\%s\%s.json' % (file_number, parent_directory))
    return op_downloaded and cl_downloaded


def download_case(cluster_dict, file_number, parent_directory):
    # TODO
    """
    Download opinion and cluster files if they are missing.
    """
    with open(data_dir + r'\clusters\%s\%s.json' % (parent_directory, file_number), 'w') as fp:
        json.dump(cluster_dict, fp)

    opinion_url = cluster_dict['resource_uri'].replace('clusters', 'opinions')
    opinion_dict = helper_functions.url_to_dict(opinion_url)
    with open(data_dir + r'\opinions\%s\%s.json' % (parent_directory, file_number), 'w') as fp:
        json.dump(opinion_dict, fp)


#############
# SCRIPTING
#############
ids_and_parents = pull_cases_by_court('scotus')
helper_functions.list_to_csv(data_dir + r'\scotus_ids.csv', ids_and_parents)
