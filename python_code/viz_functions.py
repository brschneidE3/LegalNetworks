__author__ = 'michael

import networkx as nx
import matplotlib.pyplot as plt
import os
import datetime
from operator import itemgetter
import numpy as np
import calendar
from __future__ import division
import time

def years_useable(graph_object):
    '''
    prints out the years you can use for the two functions:
        1. spring_layout(graph_object, start_year, end_year, save_dir)
        2. chronological_indeg_layout(graph_object, start_year, end_year, save_dir)
    '''
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    print "years you should use: from " , min(years) , " to " , max(years)

def years_useable_after_del(graph_object):
    '''
    prints out the years you can use for the two functions:
        1. spring_layout_after_del(graph_object, start_year, end_year, save_dir)
        2. chronological_indeg_layout_after_del(graph_object, start_year, end_year, save_dir)
    '''
    G = graph_object.copy()

    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    print "after deleting nodes, years you should use: from " , min(years) , " to " , max(years)

def rank_plot_and_histogram(graph_object, deg_type, save_dir):
    '''
    USAGE: rank_plot_and_histogram(D, 'in_degree', 'some_directory/plot_test0.png')
    
    deg_type: 'in_degree', 'out_degree', 'degree'
        Note: degree = in_degree + out_degree
    '''
    if deg_type == 'in_degree':
        ###################################
        # In-Degree Rank Plot and Histogram
        ###################################
        # Make an in-degree rank plot of network
        in_degree_sequence = sorted([tup[1] for tup in sorted(graph_object.in_degree_iter(), reverse=True)], reverse=True)  # in degree sequence
        in_dmax = max(in_degree_sequence)
        plt.subplot(121)
        plt.loglog(in_degree_sequence, 'b-', marker='o')
        plt.title("In Degree rank plot")
        plt.ylabel("in degree")
        plt.xlabel("rank")

        # Make a histogram of the in-degrees
        plt.subplot(122)
        in_data = in_degree_sequence
        # fixed bin size
        in_bins = np.arange(min(in_degree_sequence), max(in_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(in_data)-5, max(in_data)+5])
        plt.hist(in_data, bins=in_bins, alpha=0.5)
        plt.title('in degree histogram')
        plt.xlabel('variable X (bin size = 5)')
        plt.ylabel('count')
        plt.savefig(save_dir)

    if deg_type == 'out_degree':
        ####################################
        # Out-Degree Rank Plot and Histogram
        ####################################
        # Make an out-degree rank plot of network
        out_degree_sequence = sorted([tup[1] for tup in sorted(graph_object.out_degree_iter(), reverse=True)], reverse=True)  # out degree sequence
        out_dmax = max(out_degree_sequence)
        plt.subplot(121)
        plt.loglog(out_degree_sequence, 'b-', marker='o', color='red')
        plt.title("Out Degree rank plot")
        plt.ylabel("out degree")
        plt.xlabel("rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        out_data = out_degree_sequence
        # fixed bin size
        out_bins = np.arange(min(out_degree_sequence), max(out_degree_sequence), 5)  # fixed bin size
        plt.xlim([min(out_data)-5, max(out_data)+5])
        plt.hist(out_data, bins=out_bins, alpha=0.5, color='red')
        plt.title('Out degree histogram')
        plt.xlabel('variable X (bin size = 5)')
        plt.ylabel('count')
        plt.savefig(save_dir)

    if deg_type == 'degree':
        ################################
        # Degree Rank Plot and Histogram
        ################################
        # Make a degree rank plot of network
        degree_sequence = sorted([tup[1] for tup in sorted(graph_object.degree_iter(), reverse=True)], reverse=True)  # degree sequence
        dmax = max(degree_sequence)
        plt.subplot(121)
        plt.loglog(degree_sequence, 'b-', marker='o', color = 'purple')
        plt.title("Degree rank plot")
        plt.ylabel("degree")
        plt.xlabel("rank")

        # Make a histogram of the out-degrees
        plt.subplot(122)
        data = degree_sequence
        # fixed bin size
        bins = np.arange(min(degree_sequence), max(degree_sequence), 5)  # fixed bin size
        plt.xlim([min(data)-5, max(data)+5])
        plt.hist(data, bins=bins, alpha=0.5, color='purple')
        plt.title('degree histogram')
        plt.xlabel('variable X (bin size = 5)')
        plt.ylabel('count')
        plt.savefig(save_dir)


def spring_layout(graph_object, start_year, end_year, save_dir):
    '''
    USAGE: spring_layout(D, 1980, 1989, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
          -If no 'year' attribute, your graph_object can't use this function

    NOTE: TAKES (MUCH) LONGER FOR BIGGER NETWORKS, compared to chronological_indeg_layout
    '''

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    # Remove nodes that aren't contained (inclusively) between 'start_year' and 'end_year' you want to analyze:
    G.remove_nodes_from(nodes_to_delete)

    #Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] =='':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    #Get Title
    title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes'

    ##########################################################################
    # Draw Network with Spring Layout (Default) and Colored Nodes by In-Degree
    ##########################################################################
    start_time = time.time() # start timer to approximate how long it takes to plot/draw the network

    # set figure size, set figure title
    fig = plt.figure()
    fig.set_size_inches(30, 30)
    fig.suptitle(title, fontsize=30)

    # In-Degree of ech node in a list (for coloring the nodes by in-degree later using cmap=plt.cm.Blues)
    in_degrees_G = G.in_degree() ## dict of key (node) : value (in-degree)
    nodes_G = G.nodes() ## list of nodes
    n_color_G = np.asarray([in_degrees_G[n] for n in nodes_G]) ## list of node's respective in-degrees

    # draw network
    pos_G = nx.spring_layout(G)
    nx.draw(G, pos=pos_G, node_size = 30, arrows=True, with_labels=False, node_color=n_color_G, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid')
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time)) # end timer to approximate how long it takes to plot/draw the network

def chronological_indeg_layout(graph_object, start_year, end_year, save_dir):
    '''
    USAGE: chronological_indeg_layout(D, 1980, 1989, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
          -If no 'year' attribute, your graph_object can't use this function
    '''

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()
    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    # Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Date Attribute for G.nodes()
    dates = []
    cases_without_dates = []
    for each_node in G.nodes():
        if G.node[each_node]['date'] == '':
            cases_without_dates.append(each_node)
        else:
            dates.append(G.node[each_node]['date'])

    # Get Title
    title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes'

    #################################
    # For Coloring by In-Degree Later
    #################################
    # In-Degree of each node in a list (for coloring the nodes by in-degree later using cmap=plt.cm.Blues)
    in_degrees_G = G.in_degree()
    nodes_G = G.nodes()
    n_color_G = np.asarray([in_degrees_G[n] for n in nodes_G]) 

    ####################################################
    # Get X- and Y- Coordinates for Chronological Layout
    ####################################################
    ### X-Coordinates for each node in network:

    # X-Coordinates are YEAR VALUES (i.e. 1986 June 16th = 1989.458333...)
    X_G = []
    for specific_date in dates:
        temp_day = specific_date.day
        temp_month = specific_date.month
        temp_year = specific_date.year
        total_months = 12
        if temp_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            total_days = 31
        elif temp_month == 4 or 6 or 9 or 11:
            total_days = 30
        else: #temp_month = 2
            if calendar.isleap(temp_year):
                total_days = 29
            else: # it isn't leap year
                total_days = 28
        date_to_int = temp_year + (temp_month-1)/total_months + (temp_day-1)/(total_months * total_days)
        X_G.append(date_to_int)

    ### Y-Coordinates for each node in network:

    # Y-Coordinates are the respective in-degree of each node:
    Y_G = n_color_G

    ### make list of tuples of (x,y) coordinates for respective nodes: [(x1,y1), (x2,y2), ... , (xn,yn)]:
    list_of_tuples_G = zip(X_G, Y_G)

    #######################################################################
    # Draw Network with Chronological Layout and Colored Nodes by In-Degree
    #######################################################################
    '''
    Note: Ill-Advised to Change Around sizes/scaling/margins/etc. of plot, unless otherwise stated
    '''
    start_time = time.time() # start timer to approximate how long it takes to plot/draw the network

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50, 30)
    fig.suptitle(title, fontsize=50)

    # draw network
    pre_pos_G = dict(zip(G.nodes(), list_of_tuples_G)) # make a dictionary and assign each node its coordinate point
    pos_G = nx.spring_layout(G, fixed = G.nodes(), pos = pre_pos_G) # you have to fix the nodes in place!
    nx.draw_networkx(G, pos = pos_G, node_size=50, arrows=False, with_labels=False, node_color=n_color_G, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid')
    '''
    Note: you can...
        1. turn on arrows (although not really necessary, since you know nodes at right are citing the nodes at left)
        2. change the coloring of nodes--i.e. cmap = plt.cm.Reds
    * Other characteristics are optimized for visualization purposes in the author's humble opinion, but feel free to change for experimentation
    '''

    # add xlabel, remove ylabel, set x-margin, set y-margin, set x-ticks
    plt.xlabel("time", fontsize=50)
    plt.ylabel("in-degree", fontsize=50)
    axes = plt.gca()
    axes.set_xlim([min(years), max(years)+1])
    axes.set_ylim([min(Y_G)-1, max(Y_G)+1])
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time)) # end timer to approximate how long it takes to plot/draw the network

def chronological_indeg_layout_after_del(graph_object, start_year, end_year, save_dir):
    '''
    USAGE: chronological_indeg_layout_after_del(D, 1980, 1989, 'some_directory/plot_test.png')

    NOTE: graph_object should contain 'year' attribute for each node; If not, simply make one from 'date' attribute
          -If no 'year' attribute, your graph_object can't use this function
    '''

    ###############
    # Make Graph G
    ###############
    G = graph_object.copy()

    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    nodes_to_delete = []
    for each_node in G.nodes():
        if not (start_year <= G.node[each_node]['year'] <= end_year):
            nodes_to_delete.append(each_node)

    G.remove_nodes_from(nodes_to_delete)

    # Get Year Attribute for G.nodes()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    # Get Date Attribute for G.nodes()
    dates = []
    cases_without_dates = []
    for each_node in G.nodes():
        if G.node[each_node]['date'] == '':
            cases_without_dates.append(each_node)
        else:
            dates.append(G.node[each_node]['date'])

    # Get Title
    title = str(min(years)) + '-' + str(max(years)) + ' SCOTUS Network with ' + str(G.number_of_nodes()) + ' Nodes, after Deleting Zero-Degree Nodes'

    #################################
    # For Coloring by In-Degree Later
    #################################
    # In-Degree of each node in a list (for coloring the nodes by in-degree later using cmap=plt.cm.Blues)
    in_degrees_G = G.in_degree()
    nodes_G = G.nodes()
    n_color_G = np.asarray([in_degrees_G[n] for n in nodes_G]) 

    ####################################################
    # Get X- and Y- Coordinates for Chronological Layout
    ####################################################
    ### X-Coordinates for each node in network:

    # X-Coordinates are YEAR VALUES (i.e. 1986 June 16th = 1989.458333...)
    X_G = []
    for specific_date in dates:
        temp_day = specific_date.day
        temp_month = specific_date.month
        temp_year = specific_date.year
        total_months = 12
        if temp_month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
            total_days = 31
        elif temp_month == 4 or 6 or 9 or 11:
            total_days = 30
        else: #temp_month = 2
            if calendar.isleap(temp_year):
                total_days = 29
            else: # it isn't leap year
                total_days = 28
        date_to_int = temp_year + (temp_month-1)/total_months + (temp_day-1)/(total_months * total_days)
        X_G.append(date_to_int)

    ### Y-Coordinates for each node in network:

    # Y-Coordinates are the respective in-degree of each node:
    Y_G = n_color_G

    ### make list of tuples of (x,y) coordinates for respective nodes: [(x1,y1), (x2,y2), ... , (xn,yn)]:
    list_of_tuples_G = zip(X_G, Y_G)

    #######################################################################
    # Draw Network with Chronological Layout and Colored Nodes by In-Degree
    #######################################################################
    '''
    Note: Ill-Advised to Change Around sizes/scaling/margins/etc. of plot, unless otherwise stated
    '''
    start_time = time.time() # start timer to approximate how long it takes to plot/draw the network

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50, 30)
    fig.suptitle(title, fontsize=50)

    # draw network
    pre_pos_G = dict(zip(G.nodes(), list_of_tuples_G)) # make a dictionary and assign each node its coordinate point
    pos_G = nx.spring_layout(G, fixed = G.nodes(), pos = pre_pos_G) # you have to fix the nodes in place!
    nx.draw_networkx(G, pos = pos_G, node_size=50, arrows=False, with_labels=False, node_color=n_color_G, cmap=plt.cm.Blues, edge_color='black', width=1.0/10, style='solid')
    '''
    Note: you can...
        1. turn on arrows (although not really necessary, since you know nodes at right are citing the nodes at left)
        2. change the coloring of nodes--i.e. cmap = plt.cm.Reds
    * Other characteristics are optimized for visualization purposes in the author's humble opinion, but feel free to change for experimentation
    '''

    # add xlabel, remove ylabel, set x-margin, set y-margin, set x-ticks
    plt.xlabel("time", fontsize=50)
    plt.ylabel("in-degree", fontsize=50)
    axes = plt.gca()
    axes.set_xlim([min(years), max(years)+1])
    axes.set_ylim([min(Y_G)-1, max(Y_G)+1])
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time)) # end timer to approximate how long it takes to plot/draw the network

def indeg_time_series_plot(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: indeg_time_series_plot(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time()

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network (In-Degree Information)", fontsize=35)

    #####################################################
    # In-Degree Information (Mean or Median) of Each Year
    #####################################################
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    in_degrees_G = G.in_degree() ## dict of key (node) : value (in-degree)
    n_color_G = [in_degrees_G[n] for n in nodes_G] ## list of nodes's respective in-degrees

    year_indeg = zip(years, n_color_G) ## make list of tuples [(year_1, indeg_1), (year_2, indeg_2), ... , (year_n, indeg_n)]
    sorted_by_year = sorted(year_indeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average in-degree in each year, median in-degree in each year
    year_indeg_dict = {} ## get a dictionary of { {year : [all the in_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_indeg_dict.has_key(each_tuple[0]):
            year_indeg_dict[each_tuple[0]] = []
        year_indeg_dict[each_tuple[0]].append(each_tuple[1])

    in_degrees_mean_list = [] ## get the respective mean of in-degrees for each year
    in_degrees_median_list = [] ## get the respective median of in-degrees for each year
    for value in year_indeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        in_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        in_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_indeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/500 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.legend(["Mean In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time))

def outdeg_time_series_plot(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: outdeg_time_series_plot(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time()

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network (Out-Degree Information)", fontsize=35)

    #####################################################
    # Out-Degree Information (Mean or Median) of Each Year
    #####################################################
    G = graph_object.copy()

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    out_degrees_G = G.out_degree() ## dict of key (node) : value (out-degree)
    n_color_G = [out_degrees_G[n] for n in nodes_G] ## list of nodes's respective out-degrees

    year_outdeg = zip(years, n_color_G) ## make list of tuples [(year_1, outdeg_1), (year_2, outdeg_2), ... , (year_n, outdeg_n)]
    sorted_by_year = sorted(year_outdeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average out-degree in each year, median out-degree in each year
    year_outdeg_dict = {} ## get a dictionary of { {year : [all the out_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_outdeg_dict.has_key(each_tuple[0]):
            year_outdeg_dict[each_tuple[0]] = []
        year_outdeg_dict[each_tuple[0]].append(each_tuple[1])

    out_degrees_mean_list = [] ## get the respective mean of out-degrees for each year
    out_degrees_median_list = [] ## get the respective median of out-degrees for each year
    for value in year_outdeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        out_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        out_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_outdeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/500 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.legend(["Mean Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/500"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time))

def indeg_time_series_plot_after_del(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: indeg_time_series_plot_after_deletion(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time()

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network After Deleting Zero-Degree Nodes (In-Degree Information)", fontsize=35)

    ######################################################################################
    # In-Degree Information (Mean or Median) of Each Year After Deleting Zero-Degree Nodes
    ######################################################################################
    G = graph_object.copy()

    # remove nodes with zero degree
    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    in_degrees_G = G.in_degree() ## dict of key (node) : value (in-degree)
    n_color_G = [in_degrees_G[n] for n in nodes_G] ## list of nodes's respective in-degrees

    year_indeg = zip(years, n_color_G) ## make list of tuples [(year_1, indeg_1), (year_2, indeg_2), ... , (year_n, indeg_n)]
    sorted_by_year = sorted(year_indeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average in-degree in each year, median in-degree in each year
    year_indeg_dict = {} ## get a dictionary of { {year : [all the in_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_indeg_dict.has_key(each_tuple[0]):
            year_indeg_dict[each_tuple[0]] = []
        year_indeg_dict[each_tuple[0]].append(each_tuple[1])

    in_degrees_mean_list = [] ## get the respective mean of in-degrees for each year
    in_degrees_median_list = [] ## get the respective median of in-degrees for each year
    for value in year_indeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        in_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        in_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_indeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/15 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.legend(["Mean In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.legend(["Median In-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, in_degrees_mean_list)
        plt.plot(sorted_years, in_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean In-Degree of Each Year", "Median In-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time))

def outdeg_time_series_plot_after_del(graph_object, mean_bool, median_bool, total_cases_bool, save_dir):
    '''
    USAGE: outdeg_time_series_plot_after_deletion(D, True, True, True, 'some_directory/plot_test.png')
    '''
    
    start_time = time.time()

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Entire SCOTUS Network After Deleting Zero-Degree Nodes (Out-Degree Information)", fontsize=35)

    ######################################################################################
    # Out-Degree Information (Mean or Median) of Each Year After Deleting Zero-Degree Nodes
    ######################################################################################
    G = graph_object.copy()

    # remove nodes with zero degree
    solitary = [n for n,d in G.degree_iter() if d==0]
    G.remove_nodes_from(solitary)

    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes with empty year attributes
    G.remove_nodes_from(cases_without_years)    

    nodes_G = G.nodes() ## list of nodes
    out_degrees_G = G.out_degree() ## dict of key (node) : value (out-degree)
    n_color_G = [out_degrees_G[n] for n in nodes_G] ## list of nodes's respective out-degrees

    year_outdeg = zip(years, n_color_G) ## make list of tuples [(year_1, outdeg_1), (year_2, outdeg_2), ... , (year_n, outdeg_n)]
    sorted_by_year = sorted(year_outdeg, key=itemgetter(0)) ## sort the above tuples by year in increasing order

    # average out-degree in each year, median out-degree in each year
    year_outdeg_dict = {} ## get a dictionary of { {year : [all the out_degrees within that year]} , ... , {year: ... } }
    for each_tuple in sorted_by_year:
        if not year_outdeg_dict.has_key(each_tuple[0]):
            year_outdeg_dict[each_tuple[0]] = []
        year_outdeg_dict[each_tuple[0]].append(each_tuple[1])

    out_degrees_mean_list = [] ## get the respective mean of out-degrees for each year
    out_degrees_median_list = [] ## get the respective median of out-degrees for each year
    for value in year_outdeg_dict.itervalues():
        some_mean = sum(value)/len(value)
        out_degrees_mean_list.append(some_mean)
        some_median = np.median(np.array(value))
        out_degrees_median_list.append(some_median)

    # total cases count in each year:
    total_cases_list = []
    for value in year_outdeg_dict.itervalues():
        total_cases_list.append(len(value))    

    # scale down the total_cases by 500 for visualization optimization
    scaled_total_cases_list = [x/15 for x in total_cases_list]    

    # Plot:
    if (mean_bool==True) and (median_bool==False) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.legend(["Mean Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==False):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.legend(["Median Out-Degree of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    elif (mean_bool==False) and (median_bool==False) and (total_cases_bool==True):
        plt.plot(sorted_years, total_cases_list)
        plt.legend(["Total Cases of Each Year"], loc='upper left', fontsize=35)
    elif (mean_bool==True) and (median_bool==True) and (total_cases_bool==True):
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)
    else: ## (mean_bool==False) and (median_bool==False) and (total_cases_bool==False):
        print "Printing Everything Instead..."
        plt.plot(sorted_years, out_degrees_mean_list)
        plt.plot(sorted_years, out_degrees_median_list)
        plt.plot(sorted_years, scaled_total_cases_list)
        plt.legend(["Mean Out-Degree of Each Year", "Median Out-Degree of Each Year", "(Total Cases of Each Year)/15"], loc='upper left', fontsize=35)

    plt.xlabel('Years', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)

    print("--- %s seconds ---" % (time.time() - start_time))

def total_vs_zero_cases(graph_object, save_dir):
    start_time = time.time()

    # figure size adjust, figure title
    fig = plt.figure()
    fig.set_size_inches(50,30)
    fig.suptitle("Number of Zero-Degree Cases vs. Total Number of Cases of Each Year in Entire SCOTUS Network", fontsize=35)
    #################################################################
    # Total Number of Cases vs. Number of Zero-Degree Cases Each Year
    #################################################################
    G = graph_object.copy()
    years = []
    cases_without_years = []
    for each_node in G.nodes():
        if G.node[each_node]['year'] == '':
            cases_without_years.append(each_node)
        else:
            years.append(G.node[each_node]['year'])

    sorted_years = list(set(years))

    # Remove the nodes without empty year attributes
    G.remove_nodes_from(cases_without_years)

    nodes_G = G.nodes() ## list of nodes
    degrees_G = G.degree() ## dict of key (node) : value (degree)
    n_color_G = [degrees_G[n] for n in nodes_G] ## list of nodes's respective degrees

    year_deg = zip(years, n_color_G) ## get list of tuples, where each tuple is (node_year, node_degree)
    sorted_by_year = sorted(year_deg, key=itemgetter(0)) ## sort the list of tuples by year in increasing order

    # zero degree cases count in each year:
    year_deg_dict = {}
    for each_tuple in sorted_by_year:
        if not year_deg_dict.has_key(each_tuple[0]):
            year_deg_dict[each_tuple[0]] = []
        if each_tuple[1] == 0:
            year_deg_dict[each_tuple[0]].append(each_tuple[1])

    zero_deg_count_list = []
    for value in year_deg_dict.itervalues():
        zero_deg_count_list.append(len(value))

    # total cases count in each year:
    year_deg_dict2 = {}
    for each_tuple in sorted_by_year:
        if not year_deg_dict2.has_key(each_tuple[0]):
            year_deg_dict2[each_tuple[0]] = []
        year_deg_dict2[each_tuple[0]].append(each_tuple[1])

    total_cases_list = []
    for value in year_deg_dict2.itervalues():
        total_cases_list.append(len(value))

    # Plot:
    plt.plot(sorted_years, zero_deg_count_list) #zero degrees plot
    plt.plot(sorted_years, total_cases_list) # total cases plot
    plt.legend(['No. of Zero Degree Cases/Year','Total No. of Cases/Year'],loc='upper left', fontsize=35)
    plt.xlabel('Years', fontsize=30)
    plt.ylabel('Number of Cases', fontsize=30)
    axes=plt.gca()
    axes.set_xlim([min(sorted_years), max(sorted_years)])
    plt.xticks(np.arange(min(sorted_years), max(sorted_years)+1, 5))
    plt.savefig(save_dir)
    plt.show()

    print("--- %s seconds ---" % (time.time() - start_time))

