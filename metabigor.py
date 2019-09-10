#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from core import config
from core import utils
from core import routine

__author__ = '@j3ssiejjj'
__version__ = 'v1.0'


def parsing_argument(args):
    options = config.config(args)
    routine.source_parsing(options)


def main():
    config.banner(__author__, __version__)
    parser = argparse.ArgumentParser(
        description="Command line Search Engines without any API key")

    parser.add_argument('-c', '--config', action='store', dest='config_path',
                        help='config file')

    parser.add_argument('--cookies', action='store',
                        dest='cookies', help='content of cookies cookie')

    parser.add_argument('-m', '--module', action='store',
                        dest='module', help='Specific predefine module', default='custom')

    parser.add_argument('-t', '--target', action='store',
                        dest='target', help="Target for module (pattern: -t 'software|version')")

    parser.add_argument('-T', '--target_list', action='store',
                        dest='target_list', help='Target for module')

    parser.add_argument('-s', '--source', action='store',
                        dest='source', help='name of search engine (e.g: shodan, censys, fofa)')

    parser.add_argument('-S', '--source_list', action='store',
                        dest='source_list', help='JSON config for multiple search engine (e.g: shodan, censys, fofa)')

    parser.add_argument('-q', '--query', action='store',
                        dest='query', help='Query from search engine')

    parser.add_argument('-Q', '--query_list', action='store',
                        dest='query_list', help='List of query from search engine')

    # parser.add_argument('-d', '--outdir', action='store',
    #                     dest='outdir', help='Directory output', default='.')

    parser.add_argument('-o', '--output', action='store',
                        dest='output', help='Output file name', default='output')

    parser.add_argument('--raw', action='store',
                        dest='raw', help='Directory to store raw query', default='raw')

    parser.add_argument('--proxy', action='store',
                        dest='proxy', help='Proxy for doing request to search engine e.g: http://127.0.0.1:8080 ')

    parser.add_argument('-b', action='store_true', dest='brute', help='Force to brute force the country code')

    parser.add_argument('--disable_pages', action='store_true', dest='disable_pages', help="Don't loop though the pages")

    parser.add_argument('--store_content', action='store_true',
                        dest='store_content', help="Store the raw HTML souce or not")

    parser.add_argument('-hh', action='store_true', dest='helps', help='Print more help')
    parser.add_argument('-M', action='store_true',
                        dest='modules_help', help='Print available modules')

    parser.add_argument('--rel', action='store_true',
                        dest='relatively', help='Get exact app and version')

    parser.add_argument('--debug', action='store_true', dest='debug', help='Print debug output')
    parser.add_argument('--update', action='store_true',
                        dest='update', help='Update lastest version from git')

    args = parser.parse_args()

    if len(sys.argv) == 1 or args.helps:
        config.custom_help()
    if args.modules_help:
        config.modules_help()
    if args.update:
        config.update()

    parsing_argument(args)


if __name__ == '__main__':
    main()
