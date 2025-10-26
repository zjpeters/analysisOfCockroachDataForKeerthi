#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 10:20:32 2025

@author: zjpeters
"""
import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

# rawdata where csvs are stored
rawdata = os.path.join('/','home','zjpeters','Documents','otherLabs','cockroachData','rawdata')
# derivatives folder where output is stored
derivatives = os.path.join('/','home','zjpeters','Documents','otherLabs','cockroachData','derivatives')

#%% load group data

group_movement = pd.read_csv(os.path.join(rawdata, 'group','movement_analysis_group','group_movement_analysis_all_frames.csv'))
group_tracking = pd.read_csv(os.path.join(rawdata, 'group','movement_analysis_group','group_movement_analysis_tracking.csv'))

group_quadrant_pref = pd.read_csv(os.path.join(rawdata, 'group','quadrant_coordinates_group', 'group_quadrant_analysis_all_frames.csv'))

group_quadrant_indices = pd.read_csv(os.path.join(rawdata, 'group','quadrant_coordinates_group', 'quadrant_indices_group','group_quadrant_pref_indices_tracking.csv'))

#%% begin preparation for plotting
plt.close('all')
# get a list of unique experimental conditions
exp_conds = list(np.unique(group_quadrant_indices['experiment_type']))

# loop over each condition and plot box plots with data scattered on top
data_to_plot = {}
column_to_select = 'PI_stimulus'
for cond in enumerate(exp_conds):
    # restrict to data from single condition and column, and add to dictionary
    data_to_plot[cond[0]] = group_quadrant_indices[group_quadrant_indices['experiment_type'] == cond[1]][column_to_select]
# plot data within dictionary as violin plot with inner scatter of data on top of plot
plt.figure()
ax = sns.violinplot(data_to_plot, inner='point', alpha=0.6)
# set the x-ticks to correspond to experiment
ax.set_xticks(range(len(exp_conds)))
ax.set_xticklabels(exp_conds)
# can change title to whatever, currently just using the column name
plt.title(column_to_select)
plt.show()

#%% turn above into a function for repeatability

def violinPlotWithScatter(inputDataframe, columnToPlot, plotTitle=None):
    exp_conds = list(np.unique(inputDataframe['experiment_type']))
    
    # loop over each condition and plot box plots with data scattered on top
    data_to_plot = {}
    for cond in enumerate(exp_conds):
        # restrict to data from single condition and column, and add to dictionary
        data_to_plot[cond[0]] = inputDataframe[inputDataframe['experiment_type'] == cond[1]][columnToPlot]
    # plot data within dictionary as violin plot with inner scatter
    plt.figure()
    ax = sns.violinplot(data_to_plot, inner='point', alpha=0.6)
    # set the x-ticks to correspond to experiment
    ax.set_xticks(range(len(exp_conds)))
    ax.set_xticklabels(exp_conds)
    # can change title to whatever, currently just using the column name
    if plotTitle == None:
        plt.title(columnToPlot)
    else:
        plt.title(plotTitle)
    plt.show()
    
#%% import solo data and plot using above function
plt.close('all')
solo_quadrant_indices = pd.read_csv(os.path.join(rawdata, 'solo', 'quadrant_solo', 'quadrant_indices_solo', 'quadrant_preference_indices_all_frames.csv'))

violinPlotWithScatter(solo_quadrant_indices, 'PI_stimulus')
plt.savefig(os.path.join(derivatives, 'solo_quadrant_indices_PI_stimulus_violin_plots_with_scatter.png'), dpi=300)
violinPlotWithScatter(group_quadrant_indices, 'PI_stimulus')
plt.savefig(os.path.join(derivatives, 'group_quadrant_indices_PI_stimulus_violin_plots_with_scatter.png'), dpi=300)

#%% create function for boxplots with scatter
plt.close('all')
def boxPlotWithScatter(inputDataframe, columnToPlot, plotTitle=None):
    exp_conds = list(np.unique(inputDataframe['experiment_type']))
    
    # loop over each condition and plot box plots with data scattered on top
    data_to_plot = {}
    for cond in enumerate(exp_conds):
        # restrict to data from single condition and column, and add to dictionary
        data_to_plot[cond[0]] = inputDataframe[inputDataframe['experiment_type'] == cond[1]][columnToPlot]
    # plot data within dictionary as violin plot with inner scatter
    plt.figure()
    ax = sns.boxplot(data_to_plot, boxprops={'alpha': 0.4})
    sns.stripplot(data_to_plot)
    # set the x-ticks to correspond to experiment
    ax.set_xticks(range(len(exp_conds)))
    ax.set_xticklabels(exp_conds)
    # can change title to whatever, currently just using the column name
    if plotTitle == None:
        plt.title(columnToPlot)
    else:
        plt.title(plotTitle)
    plt.show()
    
boxPlotWithScatter(group_quadrant_indices, 'PI_stimulus')
plt.savefig(os.path.join(derivatives, 'group_quadrant_indices_PI_stimulus_box_plots_with_scatter.png'), dpi=300)

#%% create a dataframe that combines bottom_ns and top_ns into singular ns
group_quadrant_indices_ns = group_quadrant_indices
group_quadrant_indices_ns = group_quadrant_indices_ns.replace({'top_ns': 'Open area'}, regex=True)
group_quadrant_indices_ns = group_quadrant_indices_ns.replace({'bottom_ns': 'Open area'}, regex=True)

# set the order of preferred stimulus so that when plotted, open area is on bottom
group_quadrant_indices_ns['preferred_stimulus_or_quadrant'] = pd.Categorical(group_quadrant_indices_ns['preferred_stimulus_or_quadrant'], ['Nothing','Feces','Iso','Open area'])
#%% stacked bar chart for preference
# plots the group along the x axis, and proportion of preferred stim on y axis
plt.close('all')
plt.figure()
ax = sns.histplot(
    data=group_quadrant_indices_ns,
    x="batch", hue="preferred_stimulus_or_quadrant", color="experiment_type",
    multiple="fill", stat="proportion",
    discrete=True, shrink=.8
)
plt.title('Proportion of subjects per batch preferred stimulus')
plt.show()

plt.savefig(os.path.join(derivatives, 'group_quadrant_indices_preferred_stimulus_or_quadrant_stacked_box_plot.png'), dpi=300)