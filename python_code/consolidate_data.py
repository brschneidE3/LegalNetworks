__author__ = 'brendan'

import helper_functions
import os
import csv
import datetime
import matplotlib.pyplot as plt
import networkx as nx

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'/data'


def consolidate(court_name):
    """
    Given court_name, a string representing a CourtListener court, consolidate will iterate through every file in the
    'clusters' and 'opinions' subdirectories, beginning with 'clusters'. For every case, the following information is
    grabbed:
        -Case number: INT -- note: this is not the same as the citation id
        -Cluster file: BOOLEAN True if we have a cluster file for this case
        -Opinion file: BOOLEAN True if we have an opinion file for this case
        -Date: DATETIME object based on CourtListener's 'file_date'
        -Judges: LIST of judges found in the cluster file
        -citation_id: INT representing the citation id found in the cluster file

    A summary of all of this information is then exported to a CSV in the court parent directory.
    """

    court_data_dir = data_dir + r'/%s' % court_name
    cluster_cases = {case: None for case in os.listdir(court_data_dir + r'/clusters')}
    num_clust = len(cluster_cases.keys())
    opinion_cases = {case: None for case in os.listdir(court_data_dir + r'/opinions')}
    num_op = len(opinion_cases.keys())
    print '%s cluster files, %s opinion files detected.' % (num_clust, num_op)

    data = {}
    print 'Consolidating cluster files...'
    clust_checked = 0
    for case in cluster_cases.keys():
        case_number = case.rsplit('.')[0]  # Drop '.json'
        has_cluster_file = True

        if case in opinion_cases.keys():
            has_opinion_file = True
            del opinion_cases[case]
        else:
            has_opinion_file = False

        cluster_file_data = helper_functions.json_to_dict(court_data_dir + r'/clusters/%s' % case)

        year, month, day = [int(element) for element in cluster_file_data['date_filed'].rsplit('-')]
        file_date = datetime.date(year=year, month=month, day=day)

        judges = cluster_file_data['judges']
        citation_id = "" if cluster_file_data['citation_id'] is None \
            else int(cluster_file_data['citation_id'])

        data[case_number] = [str(case_number), has_cluster_file, has_opinion_file,
                             '%s/%s/%s' % (file_date.month, file_date.day, file_date.year),
                             judges, citation_id]

        clust_checked += 1
        if clust_checked % 100 == 0:
            print '...%s of %s clusters consolidated...' % (clust_checked, num_clust)

    num_op = len(opinion_cases.keys())
    op_checked = 0
    for case in opinion_cases.keys()[:5]:
        case_number = case.rsplit('.')[0]  # Drop '.json'
        data[case_number] = [case_number, False, True, "", "", ""]

        op_checked += 1
        if op_checked % 100 == 0:
            print '...%s of %s opinions consolidated...' % (op_checked, num_op)

    consolidated_data = [['case_no', 'cluster_file', 'opinion_file', 'date', 'judges', 'citation_id']]
    for case in data.keys():
        consolidated_data.append(data[case])
    helper_functions.list_to_csv(data_dir + '/%s/consolidation.csv'
                                 % court_name,
                                 consolidated_data)


def get_master_edge_dicts():
    """
    Produces two dictionaries from our master edge list: citer_as_key and cited_as_key, where the keys are citation ids
    and the values lists of the corresponding citation ids
    """

    with open(data_dir + r'/citations.csv') as masterfile:
        csv_reader = csv.reader(masterfile)
        next(csv_reader)  # Skip header

        citer_as_key = {}
        cited_as_key = {}

        row_i = 0
        for row in csv_reader:
            row_i += 1

            citer = int(row[0])
            cited = int(row[1])

            try:
                citer_as_key[citer].append(cited)
            except KeyError:
                citer_as_key[citer] = [cited]

            try:
                cited_as_key[cited].append(citer)
            except KeyError:
                cited_as_key[cited] = [citer]

            if row_i % 100000 == 0:
                print '%s rows loaded.' % row_i

    return citer_as_key, cited_as_key


def create_edge_sublist(court_name, master_cited_as_key):
    """
    Given a court name (and a corresponding consolidation file) and a master edge list, create_edge_sublist will create
    a citations.csv file in the court's directory, representing the subset of edges in which both nodes are in
    court_name's court.
    """

    court_dir = data_dir + r'/%s' % court_name
    court_data = helper_functions.csv_to_list(court_dir,
                                              'consolidation.csv', 1, 0)

    print 'finding IDs in court...'
    citation_ids_in_court = []
    for row in court_data:
        opinion_id = int(row[0])
        citation_ids_in_court.append(opinion_id)

    edge_sublist = [['citing', 'cited']]
    num_ids = len(citation_ids_in_court)
    id = 0
    for opinion_id in citation_ids_in_court:
        try:
            list_of_citers = master_cited_as_key[opinion_id]
        except KeyError:
            list_of_citers = []

        for citer in list_of_citers:
            if citer in citation_ids_in_court:
                edge_sublist.append([citer, opinion_id])

        id += 1
        if id % 1000 == 0:
            print '%s of %s IDs checked (%s)' % (id, num_ids, float(id)/num_ids)

    helper_functions.list_to_csv(court_dir + r'/citations_sublist.csv', edge_sublist)

# master_citer_as_key, master_cited_as_key = get_master_edge_dicts()
# create_edge_sublist('scotus', master_cited_as_key)
