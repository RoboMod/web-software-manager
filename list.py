#!/usr/bin/python

from softwares import *
import sys
import argparse
import os


# some internal helper functions
def check_dir(directory, softwares, rec=False):
    something = False
    for s in softwares:
        if s().check(directory):
            print os.path.abspath(directory) + ' - ' + s.__name__
            something = True
    if not something:
        print os.path.abspath(directory) + ' - no software detected'

    # run recursively throw directory if wanted
    if rec:
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                check_dir(os.path.join(root, name), softwares, rec)

# say hello
print "Web Software Manager"
print ""

# define argument parser
parser = argparse.ArgumentParser(description="List software, installations, versions,...")
parser.add_argument("-s", "--software", dest="software", action="store_true", default=False,
                    help="list all known software (not installations!)")
parser.add_argument("-i", "--installations", dest="installations", metavar="DIR",
                    help="list detected software in given DIR")
parser.add_argument("-r", "--recursive", dest="recursive", action="store_true", default=False,
                    help="run recursively throw the directory (only usefully with -i/--installations)")

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
        print(' - ' + s.__name__)
    print ""

# list installations
if args.installations is not None:
    # check if director exists
    if not os.path.isdir(args.installations):
        print "existing directory needed!"
        exit(-1)

    # ask each software if it detects an installations
    check_dir(args.installations, vars()['Software'].__subclasses__(), args.recursive)
      
