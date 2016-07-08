
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""
__author__ = 'brsch'

import helper_functions
import os

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'


def pull_cases_by_court(court_id):
    """
    Given a court id, pull_cases_by_court will iterate through every cluster online, check if the case (cluster &
    opinion) corresponding to that cluster has been downloaded ( via is_downloaded() ) and will build up a list of
    [case_number, parent_directory] tuples that will enable quick iteration and creation of a dictionary of cases
    in other functions via Class_Case.json_to_case.

    :param court_id: court id by which to filter
    :return:
    """

    # Initial info about the online clusters database
    clusters_dict = helper_functions.url_to_dict(clusters_url)
    # Return variable
    case_numbers_and_parent_directories = []

    # Make sure we already have these subdirectories. Create them if not.
    subdirectories = [data_dir + r'\clusters\%s' % court_id, data_dir + r'\clusters\%s' % court_id]
    for subdir in subdirectories:
        if helper_functions.subdir_exists(subdir) is False:
            helper_functions.create_subdir(subdir)

    # Iterate through each page of database
    while clusters_dict['next'] is not None:

        # Iterate through each cluster on current page
        for individual_cluster in clusters_dict['results']:

            new_cluster_url = individual_cluster['cluster']
            new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
            new_cluster_docket_url = new_cluster_dict['dockets']
            new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)
            new_cluster_court = new_cluster_docket_dict['court']

            if new_cluster_court == court_id:
                file_number = new_cluster_dict['citation_id']
                parent_directory = court_id
                case_numbers_and_parent_directories.append([file_number, parent_directory])

                if not is_downloaded(file_number, parent_directory):
                    download_case(new_cluster_url)

        clusters_dict = helper_functions.url_to_dict(clusters_dict['next'])

    # Iterate through each cluster on last page
    for individual_cluster in clusters_dict['results']:

        new_cluster_url = individual_cluster['cluster']
        new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
        new_cluster_docket_url = new_cluster_dict['dockets']
        new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)
        new_cluster_court = new_cluster_docket_dict['court']

        if new_cluster_court == court_id:
            file_number = new_cluster_dict['citation_id']
            parent_directory = court_id
            case_numbers_and_parent_directories.append([file_number, parent_directory])

            if not is_downloaded(file_number, parent_directory):
                download_case(new_cluster_url)


def is_downloaded(file_number, parent_directory):
    # TODO
    """
    Should check if corresponding cluster & opinion json files have been downloaded to appropriate path:
        data_dir + r'\clusters\COURT NAME\FILE NUMBER.json
                            &
        data_dir + r'\opinions\COURT NAME\FILE NUMBER.json

    Return True or False.
    """
    return True


def download_case(cluster_url):
    # TODO
    """
    Download opinion and cluster files if they are missing.
    """
    pass


#############
# SCRIPTING
#############

site_dict_url = 'https://www.courtlistener.com/api/rest/v3/'
site_dict = helper_functions.url_to_dict(site_dict_url)
clusters_url = site_dict['clusters']
opinions_url = site_dict['opinions']
