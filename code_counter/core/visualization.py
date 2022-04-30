#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
from matplotlib import cm
import numpy as np
from collections import defaultdict


class GraphVisualization:
    def __init__(self, total_code_lines=0, total_blank_lines=0, total_comment_lines=0,
                 files_of_language=defaultdict(int), lines_of_language=defaultdict(int)):
        self.total_code_lines = total_code_lines
        self.total_blank_lines = total_blank_lines
        self.total_comment_lines = total_comment_lines
        self.code_type_count = defaultdict(int)
        self.file_type_count = defaultdict(int)

        for tp, file_count in files_of_language.items():
            count_count = lines_of_language[tp]
            self.code_type_count[tp] = count_count
            self.file_type_count[tp] = file_count

    def visualize(self):
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
