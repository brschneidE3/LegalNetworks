
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""
__author__ = 'brsch'

import helper_functions
import os

import urllib
import json

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

        new_cluster_url = individual_cluster['cluster'] ## where is this key?
        new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
        new_cluster_docket_url = new_cluster_dict['dockets'] ## where is this key?
        new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)
        new_cluster_court = new_cluster_docket_dict['court'] ## where is this key?

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
        data_dir + r'\clusters\COURT NAME\FILE NUMBER.json'
                            &
        data_dir + r'\opinions\COURT NAME\FILE NUMBER.json'

    Return True or False.
    """

    some_boolean = os.path.exists(data_dir + r"/clusters/" + parent_directory + r"/" + file_number + r".json") and os.path.exists(data_dir + r"/opinions" + parent_directory + r"/" + file_number + r".json")
    return some_boolean


def download_case(new_cluster_url):
    # TODO
    """
    Download opinion and cluster files if they are missing.
    """

    ## get json object
    uh = urllib.urlopen(new_cluster_url)
    data = uh.read()
    js = json.loads(str(data))

    ## get the court_id / parent_directory
    new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
    new_cluster_docket_url = new_cluster_dict['dockets']
    new_cluster_docket_dict = helper_functions.url_to_dict(new_cluster_docket_url)
    new_cluster_court = new_cluster_docket_dict['court']
    parent_directory = new_cluster_court

    ## get the citation_id / file_number
    new_cluster_dict = helper_functions.url_to_dict(new_cluster_url)
    file_number = new_cluster_dict['citation_id']

    ## make cluster.json into a file with the proper directory path
    file_name = data_dir + r'/clusters/' + parent_directory + r'/' + file_number + r'.json'
    with open(file_name, 'w') as outfile:
        json.dumps(js, outfile, indent=4)

    ## for opinion file:
    new_opinion_url = new_cluster_dict['sub_opinions']
    uh2 = urllib.urlopen(new_opinion_url)
    data2 = uh2.read()
    js2 = json.loads(str(data2))

    ## make opinion.json into a file with the proper directory path
    file_name2 = data_dir + r'/opinions/' + parent_directory + r'/' + file_number + r'.json'
    with open(file_name2, 'w') as outfile2:
        json.dumps(js2, outfile2, indent=4)


    ## TODO? :
    ## I just follow the same code syntax as lines 45, 47, 49 for the unknown keys... so this code isn't foolproof yet logically speaking
    ## im still not sure where the keys are found "cluster", "dockets", "court" in lines 45, 47, 49 (any tips Brendan?)
    pass


#############
# SCRIPTING
#############

site_dict_url = 'https://www.courtlistener.com/api/rest/v3/'
site_dict = helper_functions.url_to_dict(site_dict_url)
clusters_url = site_dict['clusters']
opinions_url = site_dict['opinions']
