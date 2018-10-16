# -*- encoding: utf-8 -*-

import collections
from math import floor
from datetime import datetime,date,time
from collections import defaultdict
from urllib.parse import urlparse

def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    list_url = []

    allowed_request_type = ['OPTIONS','GET','HEAD','POST','PUT','PATCH','DELETE','TRACE','CONNECT']
    most = []
    solution_dict = defaultdict(list)
    if request_type is not None:
        allowed_request_type = request_type
    with open("log.log") as f:
        for line in f:
            log_parse = line.split(" ")
            if len(log_parse) >= 2:
                request_type = log_parse[2][1:]
                if allowed_request_type.count(request_type) != 0:
                    url_info = log_parse[3].split("//")
                    if (url_info[0] not in ignore_urls) and (
                            ignore_files is False or have_file(url_info[1]) is False) \
                            and time_check(log_parse,start_at,stop_at) and is_valid(log_parse[3]):
                        if ignore_www:
                            if 'www.' in url_info[1]:
                                url_info[1] = url_info[1][4:]
                        list_url.append(url_info[1])
                        if slow_queries:
                            solution_dict[url_info[1]] += [0,0]
                            solution_dict[url_info[1]][0] += int(log_parse[6])
                            solution_dict[url_info[1]][1] += 1

        if slow_queries:
            unsorted_list = []
            for g in solution_dict:
                new_list = solution_dict.get(g,0)
                new_list[0] = floor(new_list[0] / new_list[1])
                unsorted_list.append(new_list[0])
            unsorted_list.sort()
            unsorted_list = unsorted_list[-5:]
            unsorted_list.reverse()
            return unsorted_list
        else:
            counter = collections.Counter(list_url)
            for elem,count in counter.most_common(5):
                most.append(count)
        return most


def have_file(url):
    new = url.split('/')
    check = new[len(new) - 1]
    i = check.find('.')
    if i==-1 or (len(check) - 1)==i:
        return False
    else:
        return True


def time_check(now,min,max):
    if min is None and max is None:
        return True
    else:
        test1 = now[0][1:]
        mass1 = test1.split('/')
        d = date(2018,3,int(mass1[0]))
        test2 = now[1][:-1]
        mass2 = test2.split(':')
        t = time(int(mass2[0]), int(mass2[1]), int(mass2[2]))
        now = datetime.combine(d,t)
        if min is None:
            if now < max:
                return True
            else:
                return False
        elif max is None:
            if now > min:
                return True
            else:
                return False
        else:
            if max > now > min:
                return True
            else:
                return False


def is_valid(url, qualifying=None):
    min_attributes = ('scheme','netloc')
    qualifying = min_attributes if qualifying is None else qualifying
    token = urlparse(url)
    return all([getattr(token, qualifying_attr)
                for qualifying_attr in qualifying])
