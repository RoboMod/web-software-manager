#!/usr/bin/python
from scipy.stats.distributions import maxwell_gen

from softwares import *
from helpers.others import *
import sys
import argparse
import os
import operator


# some internal helper functions
def check_dir(directory, softwares):
    result = {os.path.abspath(directory): []}
    for s in softwares:
        if s().check(directory):
            result[os.path.abspath(directory)].append(s.__name__)
    return result

# say hello
print "Web Software Manager"
print ""

# define argument parser
parser = argparse.ArgumentParser(description="List software, installations, versions,...")
parser.add_argument("-s", "--software", dest="software", action="store_true", default=False,
                    help="list all known software (not installations!)")
parser.add_argument("-i", "--installations", dest="installations", metavar="DIR",
                    help="list detected software in given DIR")
parser.add_argument("-r", "--recursive", dest="recursive", nargs='?', type=chk_neg, const=-1, metavar="N",
                    help="run recursively till depth [N] (if given) throw the directory (only usefully with -i/--installations)")
parser.add_argument("-v", "--versions", dest="versions", nargs='?', const="all", metavar="SOFTWARE",
                    help="show (10 newest) versions of one(SOFTWARE) or all known software")
parser.add_argument("-u", "--unstable", dest="unstable", action="store_true", default=False,
                    help="show unstable versions, too (only usefully with -v/--versions)")
parser.add_argument("-a", "--all", dest="all", action="store_true", default=False,
                    help="show all (stable/unstable) versions")

# parse arguments
args = parser.parse_args()

# show help if no optional argument given
if len(sys.argv) == 1:
    parser.print_help()
    exit(-1)

# list known software
if args.software:
    print "known software:"

    softwares = vars()['Software'].__subclasses__()
    for s in sorted(softwares, key=lambda software: software.__name__):
        print ' - ' + s.__name__

    print ""

# list installations
if args.installations:
    # check if director exists
    if not os.path.isdir(args.installations):
        print "existing directory needed!"
        exit(-1)

    installations = {}

    # ask each software if it detects an installations
    installations.update(check_dir(args.installations, vars()['Software'].__subclasses__()))

    # run recursively throw directory if wanted
    if args.recursive:
        max_depth = args.recursive
        base_depth = os.path.abspath(args.installations).count(os.sep)
        for root, dirs, files in os.walk(args.installations):
            for name in dirs:
                if (max_depth > -1) and (os.path.abspath(root).count(os.sep) - base_depth >= max_depth):
                    break
                installations.update(check_dir(os.path.join(root, name), vars()['Software'].__subclasses__()))

    # display installations
    print "found installations at:"
    for i in sorted(installations.keys()):
        output = i + "\t- "

        if len(installations[i]) == 0:
            output += "no software detected"
        else:
            if len(installations[i]) > 1:
                output += "attention! more than one software could match, found: "
            output += ", ".join(sorted(installations[i]))

        print output
    print ""

# show versions
if args.versions:
    print "known software versions for:"

    softwares = vars()['Software'].__subclasses__()
    not_found = True
    for s in sorted(softwares, key=lambda software: software.__name__):
        # if not all is given, only run for the wanted software
        if args.versions is not "all":
            if s.__name__.lower() != args.versions.lower():
                continue

        not_found = False
        print ' - ' + s.__name__
        versions = s().getVersions(not args.unstable)
        if len(versions.keys()) > 0:
            sorted_versions = sort_versions(versions.keys())
            if args.all:
                print '   ' + ', '.join(sorted_versions)
            else:
                print '   ' + ', '.join(sorted_versions[:10]) + ('...' if len(sorted_versions) > 10 else "")
        else:
            print "   no versions found!"

    if not_found:
        print "software unknown!"

    print ""