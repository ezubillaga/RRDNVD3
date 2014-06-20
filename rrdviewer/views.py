#!/usr/bin/env python
# Copyright 2014 David Irvine
#
# This file is part of RRD Viewer
#
# RRD Viewer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# RRD Viewer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RRD Viewer. If not, see <http://www.gnu.org/licenses/>.

import json
import os
import rrdtool

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

GRAPH_PATH='/tmp'

def get_graph(request, start_time, end_time, path):
    pass

def get_info(request, path):
    pass

def list_graphs(request):
    graphs = []
    for directory, subdirs, files in os.walk(GRAPH_PATH):
        for file in files:
            if file.endswith(".rrd"):
                info={}
                info_file="%s.info" % file[0:-4]
                info_file_path = (os.path.join(directory, info_file))
                if os.path.exists(info_file_path):
                    info=json.load(open(info_file_path))
                info['rrd_absolute_path'] = os.path.join(directory,file)
                info['relative_path'] = info['rrd_absolute_path']
                if info['relative_path'].startswith(GRAPH_PATH):
                    info['relative_path'] = info['relative_path'][len(GRAPH_PATH):]
                info['rrd_url'] = reverse('rrd_home', args=(info['relative_path']))
                for k,v in rrdtool.info(info['rrd_absolute_path']):
                    components=k.split(".")
                    if len(components) == 1:
                        info[components[0]]=v
                    else:
                        key=components[0]
                        key,t,index=key.partition("[")
                        index=index.rstrip("]")
                        if key not in info:
                            info[key]={}
                        if index not in info[key]:
                            info[key][index]={}
                        if len(components)==2:
                            info[key][index][components[1]]=v
                        elif len(components)==3:
                            i=info[key][index] # dict of third level entries
                            tkey=components[1]
                            tkey,t,tindex=key.partition("[")
                            tindex=index.rstrip("]")
                            if tkey not in i:
                                i[tkey]={}
                            if tindex not in i[key]:
                                i[key][tindex]={}
                            i[key][tindex][components[2]]=v
                graphs.append(info)
    return render_to_response(request, "graph_list.html", {'graphs':graphs,})