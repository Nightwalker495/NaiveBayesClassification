#!/usr/bin/env python
# Written by: Milan Ondrasovic <milan.ondrasovic@gmail.com>

import sys
import csv
import fractions


class FreqTable:

    def __init__(self):
        self._occurrences = {}

    def __iter__(self):
        return iter(self._occurrences.items())

    def add_occurr(self, val):
        if val in self._occurrences:
            self._occurrences[val] += 1
        else:
            self._occurrences[val] = 1

    def get_freq(self, val):
        return self._occurrences.get(val, 0)

    def print(self, depth=0):
        indent = max(depth, 0) * '\t'
        for attr, freq in self._occurrences.items():
            print('{0}{1} = {2}'.format(indent, attr, freq))


class AttrFreqTable:

    def __init__(self, attr_name):
        self._attr_name = attr_name
        self._attr_freqs_for_outcome = {}

    def __iter__(self):
        return iter(self._attr_freqs_for_outcome.items())

    def add_occurr(self, outcome_val, attr_val):
        if outcome_val not in self._attr_freqs_for_outcome:
            self._attr_freqs_for_outcome[outcome_val] = FreqTable()

        self._attr_freqs_for_outcome[outcome_val].add_occurr(attr_val)

    def get_freq(self, outcome_val, attr_val):
        attr_freq = self._attr_freqs_for_outcome.get(outcome_val, None)

        return attr_freq.get_freq(attr_val) if attr_freq is not None else 0

    def print(self):
        print('Attribute name = {0}'.format(self._attr_name))

        for outcome, freq_table in self._attr_freqs_for_outcome.items():
            print('Outcome = {0}'.format(outcome))

            freq_table.print(1)


class Application:

    def __init__(self):
        self._outcome_freq_table = FreqTable()
        self._attr_freq_table_dict = {}

    def run(self):
        with open('./data/golf.csv') as in_file:
            reader = csv.DictReader(in_file, delimiter=',')
            self.__build_freq_tables(reader, 'play golf')

        self.print_freq_tables()

        return 0

    def print_freq_tables(self):
        for attr_freq_table in self._attr_freq_table_dict.values():
            attr_freq_table.print()
            print()

    def __build_freq_tables(self, reader, outcome_col_name):
        first_row = True

        for row in reader:
            if first_row:
                for key, value in row.items():
                    if key != outcome_col_name:
                        self._attr_freq_table_dict[key] = AttrFreqTable(key)
                first_row = False

            outcome = row[outcome_col_name]
            self._outcome_freq_table.add_occurr(outcome)

            for attr in self._attr_freq_table_dict.keys():
                self._attr_freq_table_dict[attr].add_occurr(outcome, row[attr])


if __name__ == '__main__':
    sys.exit(Application().run())
