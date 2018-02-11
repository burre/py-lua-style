#!/usr/bin/env python3
import sys
import os
import logging
from optparse import OptionParser, OptionGroup
import luastyle
from luastyle.core import FilesProcessor
from luastyle.indent import IndentOptions

def abort(msg):
    logging.error(msg)
    sys.exit()

def main():
    # parse options:
    parser = OptionParser(usage='usage: %prog [options] file|directory',
                          version='%prog ' + luastyle.__version__)
    cli_group = OptionGroup(parser, "CLI Options")
    cli_group.add_option('-r', '--replace',
                         action='store_true',
                         dest='replace',
                         help='write output in-place, replacing input',
                         default=False)
    cli_group.add_option('--type',
                         action="append",
                         type="string",
                         dest='extensions',
                         metavar='EXT',
                         help='file extension to indent (can be repeated) [lua]',
                         default=['lua'])
    cli_group.add_option('-d', '--debug',
                         action='store_true',
                         dest='debug',
                         help='enable debugging messages',
                         default=False)
    cli_group.add_option('-j', '--jobs',
                         metavar='N', type="int",
                         dest='jobs',
                         help='number of parallel jobs in recursive mode',
                         default=4)
    parser.add_option_group(cli_group)

    # Style options:
    default = IndentOptions()
    style_group = OptionGroup(parser, "Beautifier Options")
    style_group.add_option('-s', '--indent-size',
                           metavar='N', type="int",
                           dest='indent_size',
                           help='indentation size [2]',
                           default=2)
    style_group.add_option('-c', '--indent-char',
                           metavar='S', type="string",
                           dest='indent_char',
                           help='indentation character [" "]',
                           default=' ')
    style_group.add_option('-t', '--indent-with-tabs',
                           action='store_true',
                           dest='indent_with_tabs',
                           help='indent with tabs, overrides -s and -c',
                           default=False)
    style_group.add_option('-l', '--indent-level',
                           metavar='N', type="int",
                           dest='initial_indent_level',
                           help='initial indentation level [0]',
                           default=0)
    style_group.add_option('-A', '--assign-cont-level',
                           metavar='N', type="int",
                           dest='assign_cont_level',
                           help='continuation lines level in assignment [' + str(default.assign_cont_line_level) + ']',
                           default=default.assign_cont_line_level)
    style_group.add_option('-F', '--func-cont-level',
                           metavar='N', type="int",
                           dest='func_cont_level',
                           help='continuation lines level in function arguments',
                           default=default.func_cont_line_level)
    style_group.add_option('-C', '--comma-check',
                           action='store_true',
                           dest='comma_check',
                           help='check spaces after comma',
                           default=default.comma_check)
    style_group.add_option('-R', '--indent-return',
                           action='store_true',
                           dest='indent_return_cont',
                           help='indent return continuation lines on next level',
                           default=default.comma_check)
    parser.add_option_group(style_group)

    (options, args) = parser.parse_args()

    # check argument:
    if not len(args) > 0:
        abort('Expected a filepath or a directory path')

    # handle options:
    if options.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:\t%(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    # IndentRule options:
    indentOptions = IndentOptions()
    indentOptions.indent_size = options.indent_size
    indentOptions.indent_char = options.indent_char
    indentOptions.indent_with_tabs = options.indent_with_tabs
    indentOptions.initial_indent_level = options.initial_indent_level

    indentOptions.assign_cont_line_level = options.assign_cont_level
    indentOptions.func_cont_line_level = options.func_cont_level
    indentOptions.comma_check = options.comma_check
    indentOptions.indent_return_cont = options.indent_return_cont
    # build a filename list
    filenames = []
    if not os.path.isdir(args[0]):
        filenames.append(args[0])
    else:
        for root, subdirs, files in os.walk(args[0]):
            for filename in files:
                if not options.extensions or filename.endswith(tuple(options.extensions)):
                    filepath = os.path.join(root, filename)
                    filenames.append(filepath)

    # process files
    FilesProcessor(options.replace, options.jobs, indentOptions).run(filenames)

if __name__ == '__main__':
    main()
