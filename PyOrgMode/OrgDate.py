
# -*- encoding: utf-8 -*-
##############################################################################
#
#    PyOrgMode, a python module for treating with orgfiles
#    Copyright (C) 2010 Jonathan BISSON (bissonjonathan on the google thing).
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re
import time

class OrgDate:
    """Functions for date management"""

    format = 0
    TIMED = 1
    DATED = 2
    WEEKDAYED = 4
    ACTIVE = 8
    INACTIVE = 16
    RANGED = 32
    REPEAT = 64
    CLOCKED = 128

    # TODO: Timestamp with repeater interval
    DICT_RE = {'start': '[[<]',
               'end':   '[]>]',
               'date':  '([0-9]{4})-([0-9]{2})-([0-9]{2})(\s+([\w.]+))?',
               'time':  '([0-9]{2}):([0-9]{2})',
               'clock': '([0-9]{1}):([0-9]{2})',
               'repeat': '[\+\.]{1,2}\d+[dwmy]'}

    def __init__(self, value=None):
        """
        Initialisation of an OrgDate element.
        """
        self.set_value(value)

    def parse_datetime(self, s):
        """
        Parses an org-mode date time string.
        Returns (timed, weekdayed, time_struct, repeat).
        """
        search_re = '(?P<date>{date})(\s+(?P<time>{time}))?'.format(
            **self.DICT_RE)
        s = re.search(search_re, s)

        weekdayed = (len(s.group('date').split()) > 1)
        weekday_suffix = ""
        if weekdayed is True:
            weekday_suffix = s.group('date').split()[1]
        formats = {
            'timed_weekday': [True, '{0} {1} {2}', '%Y-%m-%d %a %H:%M'],
            'timed': [True, '{0} {2}', '%Y-%m-%d %H:%M'],
            'nottimed_weekday': [False, '{0} {1}', '%Y-%m-%d %a'],
            'nottimed': [False, '{0}', '%Y-%m-%d'],
        }

        # We ignore weekdays (e.g. "Mon", "Tue") because a single org file
        # could mix dates in many locales, e.g. if it was edited through
        # many compters, each with a different language
        PARSE_WEEKDAYS=False

        if s.group('time'):
            if weekday_suffix == "" or not PARSE_WEEKDAYS:
                format_date = 'timed'
            else:
                format_date = 'timed_weekday'
        else:
            if weekday_suffix == "" or not PARSE_WEEKDAYS:
                format_date = 'nottimed'
            else:
                format_date = 'nottimed_weekday'

        return (formats[format_date][0], weekdayed,
                time.strptime(
                    formats[format_date][1].format(s.group('date').split()[0],
                                                   weekday_suffix,
                                                   s.group('time')),
                    formats[format_date][2]))

    def set_value(self, value):
        """
        Setting the value of this element (automatic recognition of format)
        """
        self.value = None  # By default…
        # Checking whether it is an active date-time or not
        if value[0] == '<':
            self.format |= self.ACTIVE
        elif value[0] == '[':
            self.format |= self.INACTIVE

        # time range on a single day
        search_re = ('{start}(?P<date>{date})\s+(?P<time1>{time})'
                     '-(?P<time2>{time}){end}').format(**self.DICT_RE)
        match = re.search(search_re, value)

        if match:
            timed, weekdayed, self.value = self.parse_datetime(
                match.group('date') + ' ' + match.group('time1'))
            if weekdayed:
                self.format |= self.WEEKDAYED
            timed, weekdayed, self.end = self.parse_datetime(
                match.group('date') + ' ' + match.group('time2'))

            self.format |= self.TIMED | self.DATED | self.RANGED
            return
        # date range over several days
        search_re = ('{start}(?P<date1>{date}(\s+{time})?){end}--'
                     '{start}(?P<date2>{date}(\s+{time})?){end}').format(
            **self.DICT_RE)
        match = re.search(search_re, value)
        if match:
            timed, weekdayed, self.value = self.parse_datetime(
                match.group('date1'))
            if timed:
                self.format |= self.TIMED
            if weekdayed:
                self.format |= self.WEEKDAYED
            timed, weekdayed, self.end = self.parse_datetime(
                match.group('date2'))
            self.format |= self.DATED | self.RANGED
            return
        # single date with no range
        search_re = ('{start}(?P<datetime>{date}(\s+{time})?)' +
                     '(\s+(?P<repeat>{repeat}))?{end}').format(
                        **self.DICT_RE)
        match = re.search(search_re, value)
        if match:
            timed, weekdayed, self.value = self.parse_datetime(
                match.group('datetime'))
            if match.group('repeat'):
                self.repeat = match.group('repeat')
                self.format |= self.REPEAT
            self.format |= self.DATED
            if timed:
                self.format |= self.TIMED
            if weekdayed:
                self.format |= self.WEEKDAYED
            self.end = None
            return
        # clocked time
        search_re = '(?P<clocked>{clock})'.format(**self.DICT_RE)
        match = re.search(search_re, value)
        if match:
            self.value = value
            self.format |= self.CLOCKED

    def get_value(self):
        """
        Get the timestamp as a text according to the format
        """

        if self.value is None:
            return ""

        fmt_dict = {'time': '%H:%M'}
        if self.format & self.ACTIVE:
            fmt_dict['start'], fmt_dict['end'] = '<', '>'
        else:
            fmt_dict['start'], fmt_dict['end'] = '[', ']'
        if self.format & self.WEEKDAYED:
            fmt_dict['date'] = '%Y-%m-%d %a'
        if self.format & self.CLOCKED:
            fmt_dict['clock'] = "%H:%M"
        elif not self.format & self.WEEKDAYED:
            fmt_dict['date'] = '%Y-%m-%d'
        if self.format & self.RANGED:
            if self.value[:3] == self.end[:3]:
                # range is between two times on a single day
                assert self.format & self.TIMED
                return (time.strftime(
                    '{start}{date} {time}-'.format(**fmt_dict), self.value) +
                        time.strftime('{time}{end}'.format(**fmt_dict),
                                      self.end))
            else:
                # range is between two days
                if self.format & self.TIMED:
                    return (time.strftime(
                        '{start}{date} {time}{end}--'.format(**fmt_dict),
                        self.value) +
                            time.strftime(
                                '{start}{date} {time}{end}'.format(**fmt_dict),
                                self.end))
                else:
                    return (time.strftime(
                        '{start}{date}{end}--'.format(**fmt_dict),
                        self.value) +
                            time.strftime(
                                '{start}{date}{end}'.format(**fmt_dict),
                                self.end))
        if self.format & self.CLOCKED:
            # clocked time, return as is
            return self.value
        else:  # non-ranged time
            # Repeated
            if self.format & self.REPEAT:
                fmt_dict['repeat'] = ' ' + self.repeat
            else:
                fmt_dict['repeat'] = ''
            if self.format & self.TIMED:
                return time.strftime(
                    '{start}{date} {time}{repeat}{end}'.format(
                        **fmt_dict),
                    self.value)
            else:
                return time.strftime(
                    '{start}{date}{repeat}{end}'.format(**fmt_dict),
                    self.value)
