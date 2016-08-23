__author__ = 'brendan'

import helper_functions
import os
import csv
import datetime
import matplotlib.pyplot as plt
import networkx as nx
import operator

proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'


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

    court_data_dir = data_dir + r'\%s' % court_name
    cluster_cases = {case: None for case in os.listdir(court_data_dir + r'\clusters')}
    num_clust = len(cluster_cases.keys())
    opinion_cases = {case: None for case in os.listdir(court_data_dir + r'\opinions')}
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

        cluster_file_data = helper_functions.json_to_dict(court_data_dir + r'\clusters\%s' % case)

        year, month, day = [int(element) for element in cluster_file_data['date_filed'].rsplit('-')]
        file_date = datetime.date(year=year, month=month, day=day)

        judges = cluster_file_data['judges']
        citation_id = "" if cluster_file_data['citation_id'] is None \
            else int(cluster_file_data['citation_id'])
        try:
            reporter_num = cluster_file_data['federal_cite_one']
        except KeyError:
            reporter_num = ''

        # OPPORTUNITY FOR FURTHER FILTERING HERE
        if has_opinion_file is True:
            opinion_file_data = helper_functions.json_to_dict(court_data_dir + r'\opinions\%s' % case)
            is_clean = check_if_clean(opinion_file_data)
        else:
            is_clean = True

        # SAVE ROW IN CONSOLIDATION.CSV
        data[case_number] = [str(case_number), has_cluster_file, has_opinion_file,
                             '%s/%s/%s' % (file_date.month, file_date.day, file_date.year), judges, citation_id,
                             reporter_num,
                             is_clean]

        clust_checked += 1
        if clust_checked % 100 == 0:
            print '...%s of %s clusters consolidated...' % (clust_checked, num_clust)

    num_op = len(opinion_cases.keys())
    op_checked = 0
    for case in opinion_cases.keys()[:5]:
        case_number = case.rsplit('.')[0]  # Drop '.json'
        opinion_file_data = helper_functions.json_to_dict(court_data_dir + r'\opinions\%s' % case)
        is_clean = check_if_clean(opinion_file_data)
        # Create what will be a row in consolidation.csv
        data[case_number] = [case_number, False, True, "", "", "", "", is_clean]

        op_checked += 1
        if op_checked % 1000 == 0:
            print '...%s of %s opinions consolidated...' % (op_checked, num_op)

    consolidated_data = [['case_no', 'cluster_file', 'opinion_file', 'date', 'judges', 'citation_id', 'reporter_number',
                          'is_clean']]
    for case in data.keys():
        consolidated_data.append(data[case])
    helper_functions.list_to_csv(data_dir + r'\%s\consolidation_test.csv'
                                 % court_name,
                                 consolidated_data)


def get_master_edge_dicts():
    """
    Produces two dictionaries from our master edge list: citer_as_key and cited_as_key, where the keys are citation ids
    and the values lists of the corresponding citation ids
    """

    with open(data_dir + r'\citations.csv') as masterfile:
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

    court_dir = data_dir + r'\%s' % court_name
    court_data = helper_functions.csv_to_list(court_dir,
                                              'consolidation.csv', 1, 0)

    print 'finding IDs in court...'
    citation_ids_in_court = []
    for row in court_data:
        is_clean = row[-1] == 'TRUE'
        if is_clean:
            opinion_id = int(row[0])
            citation_ids_in_court.append(opinion_id)

    edge_sublist = [['citing_opinion_id', 'cited_opinion_id']]
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

    helper_functions.list_to_csv(court_dir + r'\citations_sublist.csv', edge_sublist)


def master_text_dict(court_name):
    court_data_dir = data_dir + r'\%s' % court_name
    opinion_cases = {case: None for case in os.listdir(court_data_dir + r'\opinions')}
    num_op = len(opinion_cases.keys())

    master_data = {}
    op_checked = 0
    for case in opinion_cases.keys():

        # OPPORTUNITY FOR FURTHER FILTERING HERE
        opinion_file_data = helper_functions.json_to_dict(court_data_dir + r'\opinions\%s' % case)
        is_clean = check_if_clean(opinion_file_data)

        # SAVE ROW IN CONSOLIDATION.CSV
        list_of_words = []
        for key in opinion_file_data:
            value = opinion_file_data[key]
            if type(value) is unicode:
                for word in value.rsplit(' '):
                    if '<' in word or '>' in word:
                        pass
                    else:
                        word.replace(',', '')
                        list_of_words.append(word)
        word_hist_dict = make_word_hist_dict(list_of_words)
        master_data = add_to_master_hist_dict(word_hist_dict, master_data)

        op_checked += 1
        if op_checked % 100 == 0:
            print '...%s of %s opinions text analyzed...' % (op_checked, num_op)
            # sorted_master = sorted(master_data.items(), key=operator.itemgetter(1), reverse=True)
            # for top5 in sorted_master[:5]:
            #     print top5

    consolidated_data = [['word', 'count']]
    sorted_master = sorted(master_data.items(), key=operator.itemgetter(1), reverse=True)[:]
    for word, count in sorted_master:
        consolidated_data.append([word, count])
    helper_functions.list_to_csv(data_dir + r'\%s\text_histogram.csv'
                                 % court_name,
                                 consolidated_data)


def make_word_hist_dict(l):
    d = {}
    for x in l:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    return d


def add_to_master_hist_dict(d, master_d):
    for x in d:
        if x in master_d:
            master_d[x] += d[x]
        else:
            master_d[x] = d[x]
    return master_d


def check_if_clean(opinion_file_data):
    """
    Function subject to change, used to determine is a case is a 'clean' court case or not. Currently, the opinion file
    is checked for containing either 'denied' or 'certiorari'. If either of these are found, the case is deemed dirty.
    Else, the case is deemed clean.
    """
    for key in opinion_file_data.keys():
        value = opinion_file_data[key]
        if type(value) is unicode:
            if 'denied' in value or 'certiorari' in value:
                return False
    return True

# master_citer_as_key, master_cited_as_key = get_master_edge_dicts()
# create_edge_sublist('scotus', master_cited_as_key)

master_text_dict('scotus')
