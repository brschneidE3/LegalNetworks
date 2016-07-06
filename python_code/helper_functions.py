
"""
ADD A DESCRIPTION OF WHAT THIS FILE IS FOR
"""

__author__ = 'brendan'

import os
import numpy as np
import csv
import ast
import urllib2


def subdir_exists(path):
    # TODO
    pass


def create_subdir(subdir):
    # TODO
    pass


def url_to_dict(url):
    """
    :param url: String representing a json-style object on Court Listener's REST API
    :return: html_as_dict, a dictionary of the data on the HTML page
    """
    response = urllib2.urlopen(url)
    html = response.read()
    html = html.replace('false', 'False')
    html = html.replace('true', 'True')
    html = html.replace('null', 'None')
    html_as_dict = ast.literal_eval(html)
    return html_as_dict


def csv_to_list(directory, filename, has_header=0, want_header=0):

    if directory[-1] == '\\' or filename[0] == '\\':
        pass
    else:
        directory += '\\'
    the_file = open(directory + filename)
    filelist = list(the_file)
    the_file.close()

    if has_header == 1 and want_header == 0:
        first_row = 1
    else:
        first_row = 0

    for i in range(len(filelist)):
        filelist[i] = filelist[i][:-1].rsplit(',')

    filelist = filelist[first_row:]

    return filelist


def list_to_dict(the_list, has_header=0, want_header=0):

    return_dict = {}

    if has_header == 1 and want_header == 0:
        first_row = 1
    else:
        first_row = 0

    for row in the_list[first_row:]:
        if len(row[1:]) > 1:
            values = row[1:]
        else:
            values = row[1]
        return_dict[row[0]] = values

    return return_dict


def column_to_list(the_list, column_index, has_header=0, want_header=0):
    output = []

    if has_header == 1 and want_header == 0:
        first_row = 1
    else:
        first_row = 0

    for row in the_list[first_row:]:
        output += [row[column_index]]

    return output


def print_dict(dict):
    for element in dict:
        print element, ": ", dict[element]


def print_list(List):
    for row in List:
        print row


def compare_dicts(list_of_dicts):
    """
    Requires that dicts have the same keys
    """
    for element in list_of_dicts[0]:
        print element, ": ", [dict_i[element] for dict_i in list_of_dicts]


def dict_values(dict, tuple_index, tuple_index_value):
    """
    :param dict: a dictionary whose keys are a tuple
    :param tuple_index: index of tuple that is of interest
    :param tuple_index_value: value required of tuple at tuple_index
    :return: list of appropriate keys of dict & corresponding values
    """
    keys = []
    values = []
    for tuple in dict:
        tuple_value_of_interest = tuple[tuple_index]
        if tuple_value_of_interest == tuple_index_value:
            keys.append(tuple)
            values.append(dict[tuple])
        else:
            0
    return keys, values


def sum_x_to_y(dictionary,x,y):
    total = 0
    for i in range(x, y+1):
        total += dictionary[i]
    return total


def cumulate(input_dict,lifetime=float("inf")):
    output = {}

    start = min(input_dict.keys())
    end = max(input_dict.keys())

    for year in range(start,end+1):
        cum_to_now = sum_x_to_y(input_dict,start,year)

        if year - start >= lifetime:
            retired_years = year - start - lifetime
            ret_to_now = sum_x_to_y(input_dict,start,start + retired_years)
        else:
            ret_to_now = 0

        output[year] = cum_to_now - ret_to_now

    return output


def unique(the_list):
    elements = []
    for element in the_list:
        if element in elements:
            pass
        else:
            elements.append(element)
    return elements


def list_to_csv(directory_and_filename, list):
    if directory_and_filename[-4:] == '.csv':
        directory_and_filename = directory_and_filename[:-4]
    with open(directory_and_filename + '.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in list:
            spamwriter.writerow(row)

    csvfile.close()


def add_row_to_csv(directory, filename, row, columns_to_skip):
    row = ['' for i in range(columns_to_skip)] + row
    with open(directory + '/' + filename + '.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(row)
    csvfile.close()


def add_version_to_filename(directory, filename):

    if directory[-1] == '\\':
        pass
    else:
        directory += '\\'
    file_name = directory + filename
    counter = 1
    file_name_parts = os.path.splitext(file_name) # returns ('/path/file', '.ext')
    while os.path.isfile(file_name):
        file_name = file_name_parts[0] + '_' + str(counter) + file_name_parts[1]
        counter += 1
    return file_name


def list_value_finder(list,key,key_index,value_index):
    for row in list:
        if row[key_index] == key:
            value = row[value_index]
            break

    return value


def column_of_list(list,column_index):
    column_values = []

    for row in list:
        column_values.append(row[column_index])

    return column_values


def table_to_tupled_dictionary(list,num_col_headers, Bool_has_header_row):

    num_rows = len(list)
    num_cols = len(list[0])
    tupled_dictionary = {}

    if num_col_headers > 0:
        header_col_values = column_of_list(list,0)
        print "header_col_values = ", header_col_values
    else:
        header_col_values = [i for i in range(0,num_rows)]
        print "header_col_values = ", header_col_values

    if Bool_has_header_row == 1:
        header_row_values = list[0]
        print "header_row_values = ", header_row_values
    else:
        header_row_values = [j for j in range(0,num_cols)]
        print "header_row_values = ", header_row_values

    for i in range(1,num_rows):
        for j in range(1,num_cols):
            print "i = ", i
            print "j = ", j
            tupled_dictionary[(header_col_values[i], header_row_values[j])] = list[i][j]
            print (header_col_values[i], header_row_values[j]), " : ", list[i][j]

    return tupled_dictionary


def dict_to_list(dictionary):
    output_list = []

    for key in dictionary:
        key_list = [str(key)]
        value_list = [dictionary[key]]
        output_row = key_list + value_list
        output_list.append(output_row)

    return output_list

def comparison_test(dict1, dict2):

    success_bool = True
    max_delta = 0

    for element in dict1:

        if dict1[element] != dict2[element]:
            delta = abs(dict1[element] - dict2[element])

            if delta > max_delta:
                max_delta = delta

            success_bool = False

    print "Largest delta: ", max_delta
    return success_bool

def remove_by_element(input_list, element_to_remove, all_Or_first):

    if all_Or_first == "all":
        list_so_far = []
        for element in input_list:

            if element == element_to_remove:
                0
            else:
                list_so_far.append(element)
        return list_so_far

    elif all_Or_first == "first":
        for i in range(len(input_list)):

            if i == len(input_list) - 1 and input_list[i] == element_to_remove:
                return input_list[:i]

            elif input_list[i] == element_to_remove:
                return input_list[:i] + input_list[i+1:]

def pairwise_add_lists(list1,list2):
    summed_list = []
    for i in range(len(list1)):
        summed_list.append(list1[i] + list2[i])
    return summed_list

def pairwise_add_dicts(dict1, dict2):
    summed_dict = {}
    for key in dict1:
        summed_dict[key] = dict1[key] + dict2[key]
    return summed_dict

def pairwise_divide_lists(nums, denoms):
    divided_list = []
    for i in range(len(nums)):
        divided_list.append(float(nums[i])/float(denoms[i]))
    return divided_list

def remove_by_index(input_list, index_to_remove):

    output_list = input_list[:index_to_remove] + input_list[index_to_remove+1:]
    return output_list

def index_finder(list_with_header_row, column_header):

    for j in range(len(list_with_header_row[0])):
        if list_with_header_row[0][j] == column_header:
            return j
    print "Column header %s not found."%column_header

def Excel_NPV(rate,values):

    orig_npv = np.npv(rate, values)
    Excel_npv = orig_npv/(1+rate)

    return Excel_npv


def dictionary_to_XLnpv(rate, dictionary, years):

    values = [dictionary[year] for year in years]
    Excel_npv = Excel_NPV(rate,values)

    return Excel_npv


def isnumeric(num):

    try:
        float(num)
        return True
    except ValueError:
        return False


def DeleteFilenamesStartingWith(Directory, StartingString):

    for filename in os.listdir(Directory):
        if filename.startswith(StartingString):
            os.remove(os.path.join(Directory, filename))

def HasDuplicates(list):

    elements = []
    for element in list:
        if element in elements:
            print 'Duplicate detected.'
            return True
        else:
            elements.append(element)
    print "No duplicates detected."
    return False

def FindDictKey(dict,value):

    for key in dict:
        if dict[key] == value:
            return key
    print "Value not found."
    return None

def SumOfListColumn(list,column_index,rows_to_skip):
    total = 0
    for row in list[rows_to_skip:]:
        total += row[column_index]
    return total


def AvgOfListColumn(list,column_index,rows_to_skip=0):
    total = 0
    row_count = 0
    for row in list[rows_to_skip:]:
        total += float(row[column_index])
        row_count += 1
    if row_count > 0:
        return float(total)/float(row_count)
    else:
        print "Div by 0 error"

def CreateTotalRow(List,RowsToSkip,ColsToSkip):
    TotalRow = []
    for j in range(ColsToSkip,len(List[0])):
        TotalRow.append(SumOfListColumn(List,j,RowsToSkip))
    return TotalRow

def Flatten(ListOfLists):
    ReturnList = [item for sublist in ListOfLists for item in sublist]
    return ReturnList

def PrintTabularResults(header_list,data_list):
    import tabulate
    tabulated_data = tabulate.tabulate(data_list,tuple(header_list))
    print tabulated_data
    return tabulated_data

def TransposeTable(table):
    transposed_table = [[x[i] for x in table] for i in range(len(table[0]))]
    return transposed_table

def InterfaceCountdown(SecondsToCountdown):
    import time
    SecsLeft = int(SecondsToCountdown)
    while SecsLeft > 0:
        print "... %d ..." % SecsLeft
        time.sleep(1)
        SecsLeft -= 1

def SortListByColumn(List,ColumnIndex):
    from operator import itemgetter
    sorted_List = sorted(List, key=itemgetter(ColumnIndex))
    return sorted_List

def SortListByRow(List,RowIndex):
    List = zip(*List)
    List.sort(key=lambda x: x[RowIndex])
    List = zip(*List)
    return List


def PercentileOfList(List,Percentile,Ascending=True):
    """
    :param List: list of values [value1, .... , valueN]
    :param Percentile: desired percentile of List (inclusive)
    :return:
    """
    N = len(List)
    K = int(Percentile*N) #Number of data points
    ascending_List = sorted(List)

    if Ascending == True:
        return ascending_List[:K]
    else:
        return ascending_List[::-1][:K]