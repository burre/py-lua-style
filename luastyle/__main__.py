#!/usr/bin/env python3
import sys
import os
import logging
from optparse import OptionParser
import luastyle.rules


def abort(msg):
    logging.error(msg)
    sys.exit()

def dynamicImport(cls):
    my_class = getattr(luastyle.rules, cls)
    return my_class

def main():
    # parse options:
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--debug", action="store_true",  dest="debug", help="enable debugging messages", default=False)
    parser.add_option("-r", "--rewrite", action="store_true",  dest="rewrite", help="rewrite current file", default=False)
    (options, args) = parser.parse_args()

    # check argument:
    if not len(args) > 0:
        abort('Expected a file name')
    if not os.path.exists(args[0]):
        abort('File ' + sys.argv[1] + ' doesn\'t exists')

    # handle options:
    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    # read whole file:
    logging.info('Working on file ' + args[0])
    input = ''
    with open(args[0]) as file:
        input = file.read()

    # chaining rules:
    optionalRules = []
    rules = [
        luastyle.rules.ReplaceStrRule(),
        luastyle.rules.RemoveCommentRule(),
        luastyle.rules.IndentRule()] + optionalRules

    output = input
    for rule in rules:
        logging.info('Applying ' + rule.__class__.__name__)
        output = rule.apply(output)

    for rule in reversed(rules):
        logging.info('Reverting ' + rule.__class__.__name__)
        output = rule.revert(output)

    if not options.rewrite:
        logging.info('done.')
        logging.info(output)
    else:
        f = open(args[0], 'r+')
        f.seek(0)
        f.write(output)
        f.truncate()
        f.close()
        logging.info('file rewrited.')

if __name__ == "__main__":
    main()