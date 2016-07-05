
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""
__author__ = 'idc9'

import os
import sys
import json
import datetime


proj_cwd = os.path.dirname(os.getcwd())
data_dir = proj_cwd + r'\data'


# def get_cases_in_jurisdiction(juris_abv='nced', file_type='opinions',
#                               data_dir='../data'):
#     """
#     Given the juristidction, file type and root path to data
#     Returns a list of case ids in that jurisdiction
#     :param juris_abv:
#     :param file_type:
#     :param data_dir:
#     :return:
#     """
#
#     # path leading to the jurisdiction files
#     path = data_dir + '/' + file_type + '/' + juris_abv + '/'
#
#     # TODO: throw an exception
#     # Check that the directory exists
#     if not os.path.isdir(path):
#         print 'not a legal path'
#         return []
#     else:
#         return [int(f.split('.json')[0]) for f in os.listdir(path)]


def json_to_case(file_number, parent_dir):

        file_suffix = r'%s\%s.json' % (parent_dir, file_number)
        cl_file = data_dir + r'\clusters\%s' % file_suffix
        op_file = data_dir + r'\opinions\%s' % file_suffix

        # Open the cluster and opinion json files
        with open(cl_file) as data_file:
            cl_data_temp = json.load(data_file)

        with open(op_file) as data_file:
            op_data_temp = json.load(data_file)

        # TODO: do this more succinctly
        # Convert to utf8 from unicode
        cl_data = {}
        for k in cl_data_temp.keys():
            value = cl_data_temp[k]
            if k == 'opinions_cited':
                cl_data['opinions_cited'] = [v.encode('utf8') for v in value]
            elif type(value) == unicode:
                cl_data[k.encode('utf8')] = value.encode('utf8')
            else:
                cl_data[k.encode('utf8')] = value

        op_data = {}
        for k in op_data_temp.keys():
            value = op_data_temp[k]
            if k == 'opinions_cited':
                op_data['opinions_cited'] = [v.encode('utf8') for v in value]
            elif type(value) == unicode:
                op_data[k.encode('utf8')] = value.encode('utf8')
            else:
                op_data[k.encode('utf8')] = value

        try:
            case_name = cl_data['case_name']
        except KeyError:
            case_name = None

        try:
            case_id = cl_data['citation_id']
        except KeyError:
            case_id = None

        try:
            docket_url = cl_data['dockets']
        except:
            docket_url = None

        if 'date_filed' in cl_data.keys():
            # TODO: make sure date is always in this format
            date_explode = cl_data['date_filed'].split('-')
            file_date = datetime.date(int(date_explode[0]),
                                      int(date_explode[1]),
                                      int(date_explode[2]))
            date = file_date
        else:
            date = None

        # FIXME ???
        # Get the case text
        text = op_data['html']
        if len(text) == 0:
            text = op_data['html_with_citations']
        elif len(text) == 0:
            text = op_data['plain_text']
        elif len(text) == 0:
            text = op_data['html_lawbox']
        elif len(text) == 0:
            text = ''
            print('case ' + str(i) + ' has no text')

        case_instance = CaseClass(case_name, case_id, date, text, docket_url)
        return case_instance


def create_dict_of_cases(list_of_file_numbers_and_parent_dirs):
    """
    Iterate through the list of file numbers and parent dirs,
     run json_to_case on each pair and
     create dictionary of the cases.
    """
    pass


class CaseClass:
    """
    Case class that store the metadata for a case node
    Union of opinion and cluster files
    Stores: case_name, case_id, date, case text
    """
    def __init__(self, case_name, case_id, date, text, docket_url):

        self.case_name = case_name
        self.case_id = case_id
        self.date = date
        self.text = text
        self.docket_url = docket_url

    def __repr__(self):
        return "Name: \t %s \n"\
               "Id \t \t %s \n"\
               "Date \t %s \n"\
            % (self.case_name, self.case_id, self.date)

#############
# SCRIPTING
#############

# Cases in the nced
# nced_case_ids = get_cases_in_jurisdiction('nced')

cl_file = data_dir + '/clusters/nced/1361899.json'
op_file = data_dir + '/opinions/nced/1361899.json'

# Create case object
case = json_to_case(file_number=1361899, parent_dir='nced')
print case
