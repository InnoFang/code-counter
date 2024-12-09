#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
import time
import datetime
from collections import defaultdict
from typing import DefaultDict, Optional

import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm


class GraphVisualization:
    """
    A class for visualizing statistical results after code counting.

    Parameters
    ----------
    total_code_lines: int
        Total number of code lines.

    total_blank_lines: int
        Total number of blank lines.

    total_comment_lines: int
        Total number of comment lines.

    files_of_language: DefaultDict[str, int]
        A dictionary containing the count of files for each code type.

    lines_of_language: DefaultDict[str, int]
        A dictionary containing the count of lines for each code type.

    Attributes
    ----------
    code_type_count: DefaultDict[str, int]
        A dictionary containing the count of lines for each code type.

    file_type_count: DefaultDict[str, int]
        A dictionary containing the count of files for each code type.
    """

    OFFSET = 0.05
    BASE_FONT_SIZE = 'x-large'

    def __init__(self,
                 total_code_lines: int = 0,
                 total_blank_lines: int = 0,
                 total_comment_lines: int = 0,
                 files_of_language: DefaultDict[str, int] = defaultdict(int),
                 lines_of_language: DefaultDict[str, int] = defaultdict(int)):
        self.total_code_lines = total_code_lines
        self.total_blank_lines = total_blank_lines
        self.total_comment_lines = total_comment_lines
        self.code_type_count = defaultdict(int)
        self.file_type_count = defaultdict(int)

        for tp, file_count in files_of_language.items():
            count_count = lines_of_language[tp]
            self.code_type_count[tp] = count_count
            self.file_type_count[tp] = file_count

    def __configure_plot(self, title: str, legend_title: str, legend_location: str) -> None:
        """
        Configure common plot settings.

        Parameters
        ----------
        title: str
            Title of the plot.

        legend_title: str
            Title of the legend.

        legend_location: str
            Location of the legend
        """
        plt.title(title)
        plt.legend(title=legend_title, loc=legend_location, bbox_to_anchor=(1.05, 1))

    def __set_font_properties(self, prop: fm.FontProperties, size: str) -> None:
        """
        Set font properties.

        Parameters
        ----------
        prop: fm.FontProperties
            FrontProperties instance.

        size: str
            Font size.
        """
        prop.set_size(size)

    def __save_plot(self, filename: Optional[str]) -> None:
        """
        Save the current plot to a file.

        Parameters
        ----------
        filename: str
            The name of the file to save.
        """
        if not filename:
            filename = f"CodeCounter_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(filename, bbox_inches='tight')
        print(f"Plot saved to: {os.path.abspath(filename)}")

    def visualize_total_statistics(self) -> None:
        """
        Visualize total statistics (pie chart for code, blank, and comment lines).
        """
        plt.subplot(121)

        total_keys = ['Code', 'Blank', 'Comment']
        total_values = [self.total_code_lines, self.total_blank_lines, self.total_comment_lines]
        explode = np.array([0., 0., 0.])
        explode[0] = GraphVisualization.OFFSET  # Offset the label `Code` outward a little

        patches, l_text, p_text = plt.pie(total_values, labels=total_keys, autopct='%2.1f%%',
                                          explode=explode, startangle=90)
        self.__set_font_properties(fm.FontProperties(), GraphVisualization.BASE_FONT_SIZE)
        plt.setp(l_text, fontproperties=fm.FontProperties(size=GraphVisualization.BASE_FONT_SIZE))
        plt.setp(p_text, fontproperties=fm.FontProperties(size=GraphVisualization.BASE_FONT_SIZE))
        plt.axis('equal')
        self.__configure_plot("Total Statistics", "Index", 'best')

    def visualize_code_files_and_lines(self) -> None:
        """
        Visualize code files and lines (inner pie for code files, outer pie for code lines).
        """
        plt.subplot(122)

        length: int = len(self.code_type_count)
        colors = cm.rainbow(np.arange(length) / length)
        wedge_props = dict(width=0.3, edgecolor='w')
        size = 0.3

        patches1, l_text1, p_text1 = plt.pie(list(self.code_type_count.values()),
                                             labels=list(self.code_type_count.keys()), autopct='%2.1f%%', radius=1,
                                             wedgeprops=wedge_props, colors=colors, pctdistance=0.85, labeldistance=1.1)
        patches2, l_text2, p_text2 = plt.pie(list(self.file_type_count.values()),
                                             labels=list(self.file_type_count.keys()), autopct='%2.1f%%',
                                             radius=1 - size,
                                             wedgeprops=wedge_props, colors=colors, pctdistance=0.8, labeldistance=0.4)

        self.__set_font_properties(fm.FontProperties(), GraphVisualization.BASE_FONT_SIZE)
        self.__set_font_properties(fm.FontProperties(), 'large')
        plt.setp(p_text1, fontproperties=fm.FontProperties(size=GraphVisualization.BASE_FONT_SIZE))
        plt.setp(p_text2, fontproperties=fm.FontProperties(size='medium'))
        plt.setp(l_text1, fontproperties=fm.FontProperties(size='x-large'))
        plt.setp(l_text2, fontproperties=fm.FontProperties(size='small'))
        plt.axis('equal')
        self.__configure_plot("Inner Pie: Code Files, Outer Pie: Code Lines", "Abbreviation", 'best')

    def visualize(self, filename: Optional[str] = None):
        """
        Visualize statistical results using subplots.
        """
        with plt.style.context('seaborn'):  # Change to your preferred style
            plt.figure('Visualization of Statistical Results', figsize=(15, 6))
            self.visualize_total_statistics()
            self.visualize_code_files_and_lines()
            # plt.show()
            self.__save_plot(filename)

    @PendingDeprecationWarning
    def visualize_old(self):
        plt.figure('Visualization of Statistical Results', figsize=(15, 6))

        size = 0.3
        wedgeprops = dict(width=0.3, edgecolor='w')
        proptease = fm.FontProperties()

        plt.subplot(121)
        total_keys = ['Code', 'Blank', 'Comment']
        total_values = [self.total_code_lines, self.total_blank_lines, self.total_comment_lines]
        explode = np.array([0., 0., 0.])
        explode[0] = 0.05  # Offset the label `Code` outward a little
        patches, l_text, p_text = plt.pie(total_values, labels=total_keys, autopct='%2.1f%%',
                                          explode=explode, startangle=90)
        proptease.set_size('x-large')
        plt.setp(l_text, fontproperties=proptease)
        plt.setp(p_text, fontproperties=proptease)
        plt.axis('equal')
        plt.title("Total Statistics")
        plt.legend(title="Index", loc='best', bbox_to_anchor=(0, 1))

        plt.subplot(122)
        length = len(self.code_type_count)
        colors = cm.rainbow(np.arange(length) / length)
        patches1, l_text1, p_text1 = plt.pie(list(self.code_type_count.values()),
                                             labels=list(self.code_type_count.keys()), autopct='%2.1f%%', radius=1,
                                             wedgeprops=wedgeprops, colors=colors, pctdistance=0.85, labeldistance=1.1)
        patches2, l_text2, p_text2 = plt.pie(list(self.file_type_count.values()),
                                             labels=list(self.file_type_count.keys()), autopct='%2.1f%%',
                                             radius=1 - size,
                                             wedgeprops=wedgeprops, colors=colors, pctdistance=0.8, labeldistance=0.4)
        # font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
        proptease.set_size('x-large')
        plt.setp(l_text1, fontproperties=proptease)
        proptease.set_size('large')
        plt.setp(p_text1, fontproperties=proptease)
        proptease.set_size('medium')
        plt.setp(p_text2, fontproperties=proptease)
        proptease.set_size('small')
        plt.setp(l_text2, fontproperties=proptease)
        plt.axis('equal')
        plt.title("Inner Pie: Code Files, Outer Pie: Code Lines")
        plt.legend(list(self.code_type_count.keys()), title="Abbreviation", loc='best', bbox_to_anchor=(1.05, 1))
        plt.show()
