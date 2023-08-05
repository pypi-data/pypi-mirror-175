import itertools
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits import axisartist
from mpl_toolkits.axes_grid1 import host_subplot

# plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文
plt.rcParams["font.family"] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

def pro_bar_data(factors:list[str], tags:list[str], df:pd.DataFrame):
    """
    cacu mean and SE for each combinations of facotors\n
    data should be like this:\n
    | factor1 | factor2 | y1 | y2 |...\n
    |  f1_1   |   f2_1  |2.1 |-2  |...\n
    after process\n
    | factor1 | factor2 | y1(mean) | y1_SE(SE) | y1_N(sum_data) |...\n
    |  f1_1   |   f2_1  |2.1       |   -2      |   32           |...\n
    """
    if len(tags) == 0:
        tags = list(df.columns)[len(factors):]
    factor_contents:list[list[str]] = [ df[f].unique().tolist() for f in factors ]
    ndf = [factors.copy()]
    for tag in tags:
        ndf[0] += [tag, tag+'_SE', tag+'_N']
    for factorCombi in itertools.product(*factor_contents):
        line = []
        for idx, tag in enumerate(tags):
            factorMask = df[factors[0]] == factorCombi[0]
            for i in range(1, len(factors)):
                factorMask &= df[factors[i]] == factorCombi[i]
            values = np.array(df.loc[factorMask, [tag]])
            line.append(values.mean())
            line.append(values.std(ddof = 1)/np.sqrt(values.shape[0]))
            line.append(values.shape[0])
        ndf.append(list(factorCombi) + line)
    return pd.DataFrame(ndf[1:], columns=ndf[0])

def sort_df_factors(factors:list[str], tags:list[str], df:pd.DataFrame):
    """UnTested
    sort each combinations of facotors\n
    data should be like this:\n
    | factor1 | factor2 | y1 | y2 |...\n
    |  f1_1   |   f2_1  |2.1 |-2  |...\n
    |  f1_1   |   f2_2  |2.1 |-2  |...\n
    ...\n
    after sort if given facotors=['factor2', 'factor1']\n
    | factor2 | factor1 | y1 | y2 |...\n
    |  f2_1   |   f1_1  |2.1 |-2  |...\n
    |  f2_1   |   f1_2  |2.1 |-2  |...\n
    ...\n
    """
    if len(tags) == 0:
        tags = list(df.columns)[len(factors):]
    factor_contents:list[list[str]] = [ df[f].unique().tolist() for f in factors ]
    ndf = [factors.copy()]
    ndf[0] += tags
    for factorCombi in itertools.product(*factor_contents):
        factorMask = df[factors[0]] == factorCombi[0]
        for i in range(1, len(factors)):
            factorMask &= df[factors[i]] == factorCombi[i]
        ndf.append(list(factorCombi) + np.array(df.loc[factorMask, tags].values))
    return pd.DataFrame(ndf[1:], columns=ndf[0])

def plot_bar(factors:list[str], tags:list[str], df:pd.DataFrame, **kwargs):
    """
    stack bar plot with hue style\n
    factors:[low_lever_factor, medium_lever_factor, ...] or just one
    tags:[stack_low_y, stack_medium_y, ...] or just one
    df:df from pro_bar_data or sort_df_factors
        kwargs:
    width = 0.4
    bar_space = 0.2
    xrotations = [0]*len(factors)
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    offset = [(i+1)*(plt.rcParams['font.size']+8) for i in range(len(factors))]
    """
    ax1 = host_subplot(111, axes_class=axisartist.Axes)
    
    if len(tags) == 0:
        tags = list(df.columns)[len(factors):]
    
    def get_arg(arg_name:str, args:dict, default_value):
        return kwargs[arg_name] if arg_name in kwargs else default_value
    width = get_arg('width', kwargs, 0.4)
    bar_space = get_arg('bar_space', kwargs, 0.2)
    xrotations = get_arg('xrotations', kwargs, [0]*len(factors))
    xrotations.append(0)
    colors = get_arg('colors', kwargs, plt.rcParams['axes.prop_cycle'].by_key()['color'])
    offset = get_arg('offset', kwargs, [(i+1)*(plt.rcParams['font.size']+8) for i in range(len(factors))])
    
    factor_uc_sum = [ len(df[f].unique()) for f in factors ]
    factor_contents, fc_old, pos = [], '', []
    for i, f in enumerate(factors):
        factor_contents.append([])
        for fc in df[f]:
            if fc != fc_old:
                factor_contents[i].append(fc)
                fc_old = fc
    factor_contents.append([factors[-1]])#master level has an extra total axis as x_title
    for axis_idx, fc in enumerate(factor_contents[:-1]):
        pos.append([])
        if axis_idx == 0:
            for fc_idx in range(len(factor_contents[axis_idx+1])):
                st_pos = bar_space + (factor_uc_sum[axis_idx]*width+bar_space) * fc_idx
                pos[axis_idx] += [st_pos+width*(i+0.5) for i in range(factor_uc_sum[axis_idx])]
        else:
            sum_c, half_width = len(factor_contents[axis_idx]), 0.5/len(factor_contents[axis_idx])
            pos[axis_idx] = (np.arange(sum_c)/sum_c + half_width).tolist()
    pos.append([0.5])#master level has an extra total axis as x_title
    bottom = get_arg('bottom', kwargs, np.zeros(len(pos[0])))
    
    for yIdx, yName in enumerate(tags):
        ax1.bar(pos[0], df[yName], width = width, bottom = bottom, label=yName,
                edgecolor='white', color=colors[yIdx])
        bottom += df[yName]
        
    ax1.set_xlim(0, pos[0][-1]+bar_space+width/2)
    ax1.set_xticks(pos[0], factor_contents[0])
    plt.setp(ax1.axis["bottom"].major_ticklabels, rotation=xrotations[0])
    
    axs = []
    for idx, sub_pos in enumerate(pos[1:]):
        axs.append(ax1.twiny())
        axs[-1].set_xticks(sub_pos, factor_contents[idx+1])
        new_axisline = axs[-1].get_grid_helper().new_fixed_axis
        axs[-1].axis["bottom"] = new_axisline(loc="bottom", axes=axs[-1], offset=(0, -offset[idx]))
        plt.setp(axs[-1].axis["bottom"].major_ticklabels, rotation=xrotations[idx+1])
    
    return np.array(pos[0]), ax1