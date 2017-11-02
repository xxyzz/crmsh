# Copyright (C) 2013 Kristoffer Gronlund <kgronlund@suse.com>
# See COPYING for license information.

# Helper completers

from . import xmlutil


def choice(lst):
    '''
    Static completion from a list
    '''
    def completer(args):
        return lst
    return completer


null = choice([])
attr_id = choice(["id="])

def call(fn, *fnargs):
    '''
    Call the given function with the given arguments.
    The function has to return a list of completions.
    '''
    def completer(args):
        return fn(*fnargs)
    return completer


def join(*fns):
    '''
    Combine the output of several completers
    into a single completer.
    '''
    def completer(args):
        ret = []
        for fn in fns:
            ret += list(fn(args))
        return ret
    return completer


booleans = choice(['yes', 'no', 'true', 'false', 'on', 'off'])


def resources(args):
    cib_el = xmlutil.resources_xml()
    if cib_el is None:
        return []
    nodes = xmlutil.get_interesting_nodes(cib_el, [])
    res = [x.get("id") for x in nodes if xmlutil.is_resource(x)]
    if args and args[0] in ['promote', 'demote']:
        return list(filter(xmlutil.RscState().is_ms, res))
    if args and args[0] == "started":
        return list(filter(xmlutil.RscState().is_running, res))
    if args and args[0] == "stopped":
        for item in filter(xmlutil.RscState().is_running, res):
            res.remove(item)
    return res


def resources_started(args):
    return resources(["started"])


def resources_stopped(args):
    return resources(["stopped"])


def primitives(args):
    cib_el = xmlutil.resources_xml()
    if cib_el is None:
        return []
    nodes = xmlutil.get_interesting_nodes(cib_el, [])
    return [x.get("id") for x in nodes if xmlutil.is_primitive(x)]


nodes = call(xmlutil.listnodes)

shadows = call(xmlutil.listshadows)

status_option = """full bynode inactive ops timing failcounts
                   verbose quiet xml simple tickets noheaders
                   detail brief""".split()
