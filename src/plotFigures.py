from __future__ import division

import matplotlib as mp

mp.use('Agg')
from matplotlib import pyplot
import numpy as np
import scipy
from matplotlib.ticker import FormatStrFormatter

mp.rcParams["font.family"] = "serif"


def get_color(i):
    colors_ = ['blueviolet', 'dodgerblue', 'mediumseagreen', 'deeppink', 'coral', 'royalblue', 'midnightblue',
               'yellowgreen', 'darkgreen', 'mediumblue', 'DarkOrange', 'green', 'red', 'MediumVioletRed',
               'darkcyan', 'orangered', 'purple', 'cornflowerblue', 'saddlebrown', 'indianred', 'fuchsia', 'DarkViolet',
               'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
               'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'black', 'grey',
               'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellow']
    return colors_[i % len(colors_)]


def get_bar_color(i):
    colors_ = ['blueviolet', 'mediumseagreen', 'deeppink', 'coral', 'royalblue', "MediumVioletRed", 'midnightblue',
               'yellowgreen', 'darkgreen', 'mediumblue', 'DarkViolet', 'DarkOrange', 'green', 'red',
               'darkcyan', 'orangered', 'purple', 'cornflowerblue', 'saddlebrown', 'indianred', 'fuchsia',
               'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue',
               'slategray', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'black', 'grey',
               'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellow']
    return colors_[i % len(colors_)]


def get_pattern(m):
    #
    patterns = ["*", "+", "x", "o", ".", "/", "\\", "|", "-", "O"]
    return patterns[m % len(patterns)]


def get_marker(m):
    markers = ["d", "o", "s", "*", "p", 'H', '8', "v", (5, 2), "D", "<", ">", "x", 'o', 'v', '^', '<', '>', 's', 'p',
               ".",
               '*', 'h',
               'D', 'd']
    return markers[m % len(markers)]


def get_linestyle(ls, or_none=False):
    linest = ['-', '--', ':', '-.', '--']
    if or_none is True:
        return 'None'
    return linest[ls % len(linest)]


def plot_bars(b, A, inpname, x_label_rotation=0, xlab="", ylab="", xlabels="",
              labels="", error=None, fontscale=2, dim=[7, 5], scale=2, legendpos="out", lloc=2,
              out_style=[".pdf"], x_grid=True, y_grid=True, yranges=None, OPACITY=0.9, BAR_EDGE_COLORS=False,
              PATTERNS=False):
    fontsize = 20
    fig = pyplot.figure(figsize=(dim[0], dim[1]))
    ax = pyplot.subplot(111)

    ax.set_axisbelow(True)
    ax.xaxis.grid(x_grid)
    ax.yaxis.grid(y_grid)

    if BAR_EDGE_COLORS:
        BAR_EDGE_COLORS = [get_color(i) for i in range(len(xlabels))]
    else:
        BAR_EDGE_COLORS = ['black'] * len(xlabels)
    if PATTERNS:
        h = pyplot.bar(b, A, align='center', width=0.30, color=[get_color(i) for i in range(len(xlabels))],
                       edgecolor=BAR_EDGE_COLORS, linewidth=1.0,
                       alpha=OPACITY,
                       label=labels, hatch=get_pattern(0))
    else:
        h = pyplot.bar(b, A, align='center', width=0.30, color=[get_color(i) for i in range(len(xlabels))],
                       edgecolor=BAR_EDGE_COLORS, linewidth=1.0,
                       alpha=OPACITY,
                       label=labels)  #
    # pyplot.subplots_adjust(bottom=0.3)
    pyplot.ylabel(ylab)

    xticks_pos = [0.45 * patch.get_width() + patch.get_xy()[0] for patch in h]
    pyplot.xticks(xticks_pos, xlabels, ha='center', rotation=x_label_rotation)
    if yranges:
        pyplot.ylim(yranges[0], yranges[1])
    else:
        pyplot.ylim(min(A) * 0.6, max(A) * 1.05)
    # # Shrink current axis by 20%
    # #box = ax.get_position()
    # #ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    #
    # if legendpos == "out":
    #     legend = ax.legend((h), (labels),bbox_to_anchor=(1, 0.5),
    #                    loc="center left", borderaxespad=0., frameon=False)
    # elif legendpos == "nolegend":
    #     pass
    # else:
    #     legend = pyplot.legend(bbox_to_anchor=(1.05, 1), loc=lloc, borderaxespad=0., frameon=False)

    pyplot.tick_params(axis='both', which='major', labelsize=fontsize)
    pyplot.xlabel(xlab, fontsize=fontsize)
    pyplot.ylabel(ylab, fontsize=fontsize)

    for os in out_style:
        pyplot.savefig(inpname + os, bbox_inches='tight')
    pyplot.close(pyplot.gcf())


def plot_ecdf_lists(A, inpname, xlab="", ylab="CDF", labels="", fontscale=2, scale=2, legendpos="out", main="",
                    lloc=4, out_style=[".pdf"], dim=[7, 5], grid_on=True, legendborderspacing=1.15, FRAMEON=True,
                    x_lim_values=None, LEGEND_X_POS=1.7):
    # A is a list of lists and we will plot the ecdf of all these lists in the same plot

    afont = {'fontname': 'serif'}  # 'Arial'
    all_nan = True
    pyplot.figure(figsize=(dim[0], dim[1]))
    allelements = []
    for sub_list_i in A:
        for k in sub_list_i:
            allelements.append(k)

    if x_lim_values:
        range_values = x_lim_values[1] - x_lim_values[0]
        min_value = x_lim_values[0]
        max_value = x_lim_values[1]
    else:
        min_value = np.nanmin(allelements)
        max_value = np.nanmax(allelements)
        range_values = max_value - min_value

    pyplot.xlim(xmin=min_value - range_values * 0.1, xmax=max_value + range_values * 0.1)
    pyplot.ylim((-0.1, 1.1))
    ymin, ymax = pyplot.ylim()
    np.percentile_list = [25, 50, 75, 95]

    for i in range(0, len(A)):
        Asub = A[i]
        b = 1. * np.arange(len(Asub)) / (len(Asub) - 1)
        np.sorted_data = np.sort(Asub)

        np.percentile_points = np.percentile(np.sorted_data, np.percentile_list)
        y_values = [float(k / 100) for k in np.percentile_list]

        pyplot.plot(np.sorted_data, b, color=get_color(i), linewidth=scale)
        pyplot.plot(np.percentile_points, y_values, color=get_color(i), linestyle='None',
                    marker=get_marker(i), markersize=scale * 5, label=labels[i])
        if legendpos == "out":
            pyplot.legend(bbox_to_anchor=(LEGEND_X_POS, 1), borderaxespad=0., frameon=FRAMEON, numpoints=1)

        else:
            pyplot.legend(borderaxespad=legendborderspacing, loc=lloc, frameon=FRAMEON, numpoints=1)
        ax = pyplot.gca()
        if main != "":
            ax.set_title(main, y=1.0)

    pyplot.ylim((ymin, ymax))
    pyplot.tick_params(axis='both', which='major', labelsize=20)
    pyplot.xlabel(xlab, fontsize=20, **afont)
    pyplot.ylabel(ylab, fontsize=20, **afont)
    ax = pyplot.gca()
    ax.grid(grid_on)
    ax.set_facecolor((1, 1, 1))
    ax.set_xticklabels(ax.get_xticks(), **afont)
    ax.set_yticklabels(ax.get_yticks(), **afont)

    for os in out_style:
        pyplot.savefig(inpname + os, bbox_inches='tight')
    pyplot.close(pyplot.gcf())


def plot_graph(b, A, inpname=None, xlab="", ylab="", labels="", xticklabels=None, error=None, fontscale=2,
               dim=[8, 5], scale=1.5,
               legendpos="out", lloc="center right",
               out_style=[".pdf"], multiple_lines=True, x_grid=False, y_grid=False, groupby=1,
               colorby=None, horizontal_lines=[], horizontal_lines_labels=[],
               main="", onlyline=False, nolegend=False, nround=None, nlegendcol=1, fsize=18, x_tick_on=True,
               legend_pos_tuning=None, LEGEND_FRAME_BOUNDARY='white', LEGEND_FACE_COLOR="white", setyrange=None,
               x_tick_angle=0, LEGEND_X_POS=0.80, background_colors=None, Y_LOG=False, X_LOG=False,
               ONLY_INTEGER_VALUES_X_AXIS=False, marker_text=None):
    """Plot the columns of a matrix with b as the x-axis

    Parameters
    ----------
    b : list
        The x-axis data as a list.
    A : matrix
       Each column represents a scheme
    groupby: integer
        Represents the groups of clusters to have the same marker and same color BUT a different line-style
    inpname : string
        Figure will be saved to the folder using this input file name
    xlab : string
        Label for the X axis.
    ylab : string
        Label for the Y axis.
    label: string
        Legend text
    fontscale: integer
        The scale makes the fonts smaller or bigger compared to default
    dim: list of 2 integers
        Width and height of the figure
    scale: integer
        Marker scale
    legendpos: string, out, in
        Legend's position, inside the figure box, or outside
    lloc: string or integer
        location of the legend
    """
    # matplotlib.rc('font', family='sans-serif')
    # matplotlib.rc('font', serif='Arial')
    # matplotlib.rc('text', usetex='false')
    # matplotlib.rcParams.update({'font.size': 22})

    fig = pyplot.figure(figsize=(dim[0], dim[1]))
    ax = fig.add_subplot(111)
    ax.set_axisbelow(True)

    if not multiple_lines:
        ncols = 1
        nolegend = True
    else:
        ncols = A.shape[1]

    if colorby is None:
        colorby = ncols

    minA = np.nan
    maxA = np.nan

    if not np.isnan(np.min(A)):
        minA = np.nanmin(A)
    if not np.isnan(np.max(A)):
        maxA = np.nanmax(A)

    if not (np.isnan(maxA) and np.isnan(minA)):
        if maxA == minA:
            if minA > 0:
                minA = minA * 0.8
            elif minA < 0:
                minA = minA * 1.2
            else:
                minA = -0.1

        x_width = (max(b) - min(b)) / 10

        if setyrange:
            ymin_value, ymax_value = setyrange

        else:
            y_height = (maxA - minA) / 9
            if y_height == 0:
                y_height = maxA * 0.5
                if y_height == 0:
                    y_height = 0.5
            ymin_value = minA - y_height
            ymax_value = maxA + y_height
            if ymin_value == ymax_value:
                ymax_value = ymin_value + 1

        xmin = min(b) - x_width
        pyplot.xlim(xmin=xmin, xmax=max(b) + x_width)

        pyplot.ylim(ymin=ymin_value, ymax=ymax_value)

        ymin, ymax = pyplot.ylim()
        ax.xaxis.grid(x_grid)
        ax.yaxis.grid(y_grid)

        for ind, i in enumerate(horizontal_lines):
            pyplot.axhline(i, color='k', linestyle='--')
            pyplot.text(xmin + 0.5, ymax_value - 1, horizontal_lines_labels[ind], rotation=0, fontsize=15)

        if Y_LOG:
            ax.set_yscale('log')
        if X_LOG:
            ax.set_xscale('log')

        for i in range(ncols):
            if not multiple_lines:
                if error is not None:
                    pyplot.errorbar(b, A, yerr=error, color=get_color(i % groupby), linewidth=scale,
                                    markersize=scale * 8, marker=get_marker(int(np.floor(i / groupby))))
                else:
                    pyplot.plot(b, A, color=get_color(i % groupby), linewidth=scale,
                                markersize=scale * 8, marker=get_marker(int(np.floor(i / groupby))))
                    if marker_text:  #
                        marker_index = 0
                        for x, y in zip(b, A):
                            print(marker_text[marker_index])
                            pyplot.annotate(marker_text[marker_index],  # this is the text
                                            (x, y),  # this is the point to label
                                            textcoords="offset points",  # how to position the text
                                            xytext=(-1, 10),  # distance from text to points (x,y)
                                            ha='center')  # horizontal alignment can be left, right or center
                            marker_index = marker_index + 1

            else:
                if error is not None:
                    pyplot.errorbar(b, A[:, i], yerr=error[:, i], color=get_color(int(i / colorby)), linewidth=scale,
                                    markersize=scale * 8, marker=get_marker(i % groupby),
                                    label=labels[i])

                else:
                    pyplot.plot(b, A[:, i], color=get_color(int(i / colorby)), linewidth=scale,
                                markersize=scale * 8, marker=get_marker(i % groupby),
                                markeredgecolor=get_color(i % groupby),
                                label=labels[i])

        pyplot.ylim((ymin, ymax))
        pyplot.tick_params(axis='both', which='major', labelsize=fsize)
        if x_tick_on:
            ax.set_xticks(b)
            if xticklabels is None:
                x_tick_values = ax.get_xticks()
            else:
                x_tick_values = xticklabels
            if ONLY_INTEGER_VALUES_X_AXIS:
                ax.set_xticklabels([int(val) for val in x_tick_values])
            else:
                if nround:
                    ax.set_xticklabels([round(val, nround) for val in x_tick_values], rotation=x_tick_angle,
                                       fontsize=fsize)
                else:
                    ax.set_xticklabels(x_tick_values, rotation=x_tick_angle, fontsize=fsize - 4)
        ax.set_yticklabels(ax.get_yticks())
        ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
        ax.set_title(main)
        pyplot.xlabel(xlab, fontsize=fsize + 4)
        pyplot.ylabel(ylab, fontsize=fsize + 4)

        if not nolegend:
            if legendpos == "out":
                legend = pyplot.legend(bbox_to_anchor=(LEGEND_X_POS, 1), loc="upper right", borderaxespad=0.,
                                       frameon=True,
                                       ncol=nlegendcol, numpoints=1, prop={'size': 12})
            else:
                if lloc == "upper right":
                    pos = (0.97, 0.99)
                elif lloc == "upper left":
                    pos = (0.02, 0.97)
                elif lloc == "lower right":
                    pos = (0.99, 0.01)
                elif lloc == "lower left":
                    pos = (0.03, 0.01)
                elif lloc == "center":
                    pos = (0.65, 0.65)
                elif lloc == "center left":
                    lloc = "center"
                    pos = (0.35, 0.55)
                else:
                    pos = (0.25, 0.5)
                if legend_pos_tuning:
                    pos = legend_pos_tuning
                legend = pyplot.legend(bbox_to_anchor=pos, loc=lloc, borderaxespad=0., frameon=True, ncol=nlegendcol,
                                       columnspacing=0.2, numpoints=1, prop={'size': 12})

            frame = legend.get_frame()
            frame.set_facecolor(LEGEND_FACE_COLOR)
            frame.set_edgecolor(LEGEND_FRAME_BOUNDARY)

        if not background_colors:
            ax = pyplot.gca()
            if mp.__version__ == "2.2":
                ax.set_facecolor((1, 1, 1))
        else:
            for i in range(len(background_colors)):
                pyplot.axvspan(background_colors[i][0], background_colors[i][1], facecolor=background_colors[i][2],
                               alpha=0.2)

        if inpname == None:
            return pyplot.gcf()
        else:
            for os in out_style:
                pyplot.savefig(inpname + os, bbox_inches='tight')
        pyplot.close(pyplot.gcf())


def box_plot(title_str, fname, values, labels, ylabel, dim=[5, 3], fsize=22, rangle=0, y_range=None, x_grid=False,
             y_grid=True, group_by=2, ADD_STATS_AS_TEXT="MEAN"):
    # plot results
    pyplot.figure(figsize=(dim[0], dim[1]))
    box_plots = pyplot.boxplot(values, patch_artist=True, vert=True)

    # fill with colors

    for i, patch in enumerate(box_plots['boxes']):
        patch.set_facecolor(get_bar_color(int(i / group_by)))
        patch.set_alpha(0.5)

    pyplot.title(title_str)
    ax = pyplot.gca()
    ax.set_axisbelow(True)
    ax.xaxis.grid(x_grid)
    ax.yaxis.grid(y_grid)
    xyz = zip(*values)
    averages = [np.nanmean(k) for k in values]
    medians = [np.nanmedian(k) for k in values]
    mins = [np.nanmin(k) for k in values]

    if not y_range:
        min_value = min(map(min, xyz))
        max_value = max(map(max, xyz))
        y_range = [min_value - (max_value - min_value) * 0.1, max_value + (max_value - min_value) * 0.1]
    ax.set_ylim(ymin=y_range[0], ymax=y_range[1])

    pos = np.arange(len(values)) + 1
    averageValueLabels = [str(np.round(s, 2)) for s in averages]
    medianValueLabels = [str(np.round(s, 2)) for s in medians]

    i = 0
    position_tuner = 0.90  # 0.95 #  =sometimes we need to tune these
    for tick, label in zip(range(len(values)), ax.get_xticklabels()):
        if ADD_STATS_AS_TEXT == "MEAN_MEDIAN":
            stat_text = str(averageValueLabels[tick]) + "\n" + str(medianValueLabels[tick])
            position_tuner = 0.90
        elif ADD_STATS_AS_TEXT == "MEAN":
            stat_text = str(averageValueLabels[tick])
        elif ADD_STATS_AS_TEXT == "MEDIAN":
            stat_text = str(medianValueLabels[tick])
        else:
            stat_text = []
        ax.text(pos[tick], y_range[1] * position_tuner, stat_text,
                horizontalalignment='center', color='black', fontsize=int(fsize * 0.8))
        i += 1

    ax.set_ylabel(ylabel, fontsize=fsize)

    labels = [name.replace("Strategy", "") for name in labels]
    labels = [name.replace("_", ",") for name in labels]
    labels = [name.replace("GreedyMaxSum", "GREEDY") for name in labels]
    pyplot.rc('ytick', labelsize=fsize)
    ax.set_xticklabels(labels, rotation=rangle, fontsize=int(fsize * 0.9))
    ax.tick_params(top='off', right='off')
    ax.tick_params(axis='both', which='major', pad=8)
    pyplot.savefig(fname, bbox_inches='tight')
    pyplot.close(pyplot.gcf())


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.nanmean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, h  # m-h, m+h


def PathlossKeenanMotley(dist, center_frequency_hz=5.25e9):
    """
        Description Keenan Motley
    """
    # Keenan - Motley partition path loss  model constant
    speed_of_light = 300000000
    pl_fs = 10 * np.log10((speed_of_light / (center_frequency_hz * 4 * np.pi * dist)) ** 2)
    # linear pathloss coefficient: dB/m
    alpha = 0.44
    pl_db = pl_fs - alpha * dist
    pl_lin = 10 ** (pl_db / 10)

    return pl_lin


def to_dB(x):
    '''
    Converts linear to dB
    :param x: in linear
    :return: into dB
    '''
    if x > 0:
        y = 10.0 * np.log10(x)
    else:
        print("to_dB function error: ", x)
    return y


def from_dB(x):
    '''
    Converts from dB into linear
    :param x: in dB
    :return: into linear
    '''
    y = 10.0 ** (x / 10.0)
    return y


def linkSNR(distance, system_channel_BW_Hz=5e6):
    """
    the model for updating the link SNR from one time instant to another
    :return: linkSNR
    """
    Ptx_dbm = 15
    tx_antenna_gain = 3
    rx_antenna_gain = 3
    rx_noise_figure = 6

    thermal_noise_recv = -174  # dBm/Hz

    noise_dBm = thermal_noise_recv + 10 * np.log10(system_channel_BW_Hz) + rx_noise_figure
    receiver_noise_lin = 10 ** (noise_dBm / 10)

    pathloss_lin = PathlossKeenanMotley(distance)
    rx_pwr_db = Ptx_dbm + tx_antenna_gain + rx_antenna_gain + to_dB(pathloss_lin)
    snr = from_dB(rx_pwr_db) / (receiver_noise_lin)
    snr = to_dB(snr)
    return snr


if __name__ == '__main__':
    # generate some random values for x-axis
    param_to_increase = range(0, 100, 20)

    # generate some random values for y-axis
    y_values = np.random.random(len(param_to_increase))
    # plot a single line, save it in file "single-line.pdf"
    plot_graph(param_to_increase, y_values, "single-line", xlab="Parameter to increase", ylab="Statistic",
               multiple_lines=False)

    # generate a matrix with 3 columns and param-to-increase number of rows
    y_values = np.random.rand(len(param_to_increase), 3)

    plot_graph(param_to_increase, y_values, "three-lines", xlab="Parameter to increase", ylab="Statistic",
               labels=["case-1", "case-2", "case-3"], groupby=3, colorby=1, legendpos="in", lloc="lower left")
    y_values = [np.random.random(100000), np.random.random(5000), np.random.random(8000)]
    plot_ecdf_lists(y_values, "ecdf_test", xlab="Datarate (Mbps)", ylab="ECDF", labels=["case-1", "case-2", "case-3"],
                    legendpos="in", lloc="upper right")

    distances = range(10, 100, 10)
    pathloss = [PathlossKeenanMotley(d) for d in distances]
    plot_graph(distances, pathloss, "pathloss", xlab="Distance (m)", ylab="Pathloss (mW)",
               multiple_lines=False)
    rx_snr = [linkSNR(d) for d in distances]
    plot_graph(distances, rx_snr, "SNR", xlab="Distance (m)", ylab="SNR (dB)",
               multiple_lines=False)