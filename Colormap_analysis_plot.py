import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap


def colormap_plot(data_score_df, var_names, N_groups, group_names = [], annot_flag = True, thr_flag = True, score_thr = 0, colorbar_flag = True, fig_title = "", yticks_flag = True, save_flag = False, save_dir = ""):
    # data_score_df (dataframe):        Dataframe containing the data to create the plots. Rows should correspond to the number of variables, ordered according to var_names, and columns ordered as group_names. It can contain z-scores, chi-2's, p-values, etc.
    # var_names (list of strings):      Names of the analysed variables to be shown in the colormap (y-axes)
    # group_names (list of strings):    Names of the cluster-wise comparison columns . If not specified it will be named numerically corresponding to the groups. 
    # annot_flag (Boolean):             If true, values from data_score_df are shown on the heatmap.
    # thr_flag (Boolean):               If true, score_thr is considered and only values whose absolute value is higher than the threshold are shown on the heatmap (if annot_flag = True)
    # score_thr (float):                Threshold for which annotations to show. Absolute values from data_score_df smaller than the threshold are not shown if the thr_flag flag is true. 
    # colorbar_flag (Boolean):          If true, the plot shows the colorbar
    # fig_title (string):               Define the title of the colormap plot.
    # yticks_flag (Boolean):            If true, yticks (var_names) are shown on the plot
    # save_flag (Bolean):               If true, the figure is saved in "save_dir" folder.
    # save_dir (string):                Directory to where to save the figure if "save_flag = True". Also should indicate the name of the figure. Example: "directory/feat_score_heatmap.jpg"
 
    # Dataframe with the information to plot. Making it generic with the colnames
    if len(group_names) == 0: # Define cluster-wise comparison names if empty
        for group in range(N_groups-1):
            for group_compare in range(group+1, N_groups):
                group_names.append("{}-{}".format(group, group_compare))

    data_heatmap_df = pd.DataFrame(index = var_names)

    for i in range(len(data_score_df.columns)):
        data_heatmap_df[group_names[i]] = data_score_df.iloc[:, i]
    data_heatmap_df.fillna(0, inplace=True)

    # Datafarme for annotations to show
    if (annot_flag == True) & (thr_flag == False):
        data_heatmap_annot_df = data_heatmap_df.copy()
    elif (annot_flag == False):
        data_heatmap_annot_df = pd.DataFrame(np.nan, index = data_heatmap_df.index, columns = data_heatmap_df.columns)
    elif (annot_flag == True) & (thr_flag == True):
        data_heatmap_annot_df = data_heatmap_df.mask(abs(data_heatmap_df) < score_thr)
    null_cells = data_heatmap_annot_df.isnull()
    annotations = data_heatmap_annot_df.astype(float).round(2).astype(str).round(3).mask(null_cells, "")

    # Colormap plot
    #    Create a green-red divergent colormap
    color_points = 250
    color_separation = np.linspace(min(data_heatmap_df.min()), max(data_heatmap_df.max()), color_points-1)
    color_sep = (color_separation[2]- color_separation[1])
    color_sep_mid = color_sep/2
    color_separation = color_separation - color_separation[color_separation > 0][0]
    color_separation = np.append(color_separation, color_separation[-1]+color_sep)
    len_red = len(color_separation[color_separation < 0])
    len_green = len(color_separation[color_separation > 0])
    rd_map = plt.cm.get_cmap("Reds", 256)
    gr_map = plt.cm.get_cmap("Greens", 256)
    newcolors = np.concatenate((rd_map(np.linspace(0, 1, len_red))[::-1], np.array((1, 1, 1, 1)).reshape((1,-1)), gr_map(np.linspace(0, 1, len_green))))
    my_cmap = ListedColormap(newcolors)
    #    Create the plot
    f, axs = plt.subplots(1, 2, gridspec_kw={'width_ratios':[1, 0.1]}, figsize=(10, 15))
    ax1 = axs[0]
    axcb = axs[1]
    xticks = np.array(group_names)
    h1 = sns.heatmap(data_heatmap_df, annot=annotations, fmt="s", cmap=my_cmap, vmin=min(color_separation)-color_sep_mid, vmax=max(color_separation)+color_sep_mid, annot_kws={"size":15}, xticklabels=xticks, linewidths=1, ax=ax1, cbar=colorbar_flag, cbar_ax=axcb)
    h1.set_title("{}".format(fig_title), fontsize=25)
    h1.set_ylabel("")
    if colorbar_flag == True:
        cbar = h1.collections[0].colorbar
        cbar.ax.tick_params(labelsize=15)
        h1.figure.axes[1].set_ylabel("Z-Score", size=25)
    if yticks_flag == False:
        h1.set_yticks([])
    tl = h1.get_xticklabels()
    h1.set_xticklabels(tl, rotation=0, fontsize=15)
    tly = h1.get_yticklabels()
    h1.set_yticklabels(tly, rotation=0, fontsize=15)
    #plt.suptitle("GroupA vs GroupB", fontsize=35)
    if save_flag == True:
        plt.savefig(save_dir, dpi=300)
    plt.show()