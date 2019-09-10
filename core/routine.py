import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core import config
from core import utils
from core import routine

from modules import fofa
from modules import shodan
from modules import censys
from modules import zoomeye
from modules import gitsearch

from modules import sploitus
from modules import vulners
from modules import writeups
from modules import cvedetails
from modules import iposint


# query by module
def source_parsing(options):
    # search on specific search engine which is default routine
    if 'custom' in options.get('module'):
        if options.get('query_list'):
            queris = utils.just_read(options.get('query_list')).splitlines()

            for query in queris:
                options['query'] = query
                single_query(options)

        # query by multi source
        elif options.get('source_list'):
            query_by_source = utils.get_json(
                utils.just_read(options.get('source_list')))
            if type(query_by_source) == dict:
                for key, value in query_by_source.items():
                    options['source'] = key
                    options['query'] = value
                    single_query(options)
            else:
                utils.print_bad(
                    "Look like your Source file not correct the pattern")

        else:
            single_query(options)

    # do other mode
    special_mode = ['exploit', 'git', 'ip']
    if options.get('module') in special_mode:
        if options.get('target_list'):
            targets = utils.just_read(options.get('target_list')).splitlines()

            for query in targets:
                options['target'] = query
                module_query(options)
        else:
            module_query(options)


def module_query(options):
    utils.print_debug(options, options)
    query = options.get('target', False) if options.get(
        'target') else options.get('query')
    utils.print_info("Query: {0}".format(query))

    if 'exploit' in options.get('module'):
        if '|' in options.get('target'):
            options['product'] = options.get('target').split('|')[0].strip()

            if options['relatively']:
                utils.print_info("Running with relative version")
                exact_version = options.get('target').split('|')[1].strip()
                if '.' in exact_version:
                    options['version'] = exact_version.split('.')[0] + "."
            else:
                options['version'] = options.get(
                    'target').split('|')[1].strip()
        else:
            options['product'] = options.get('target')

        sploitus.Sploitus(options)
        vulners.Vulners(options)
        writeups.Writeups(options)
        # cvedetails.Cvedetails(options)

    if 'ip' in options.get('module'):
        iposint.IPOsint(options)

    # -m git -t 'sam'
    if 'git' in options.get('module'):
        gitsearch.GitSearch(options)


# really do a query
def single_query(options):
    utils.print_debug(options, options)
    utils.print_info("Query: {0}".format(options.get('query')))
    if not options.get('source'):
        utils.print_bad("You need to specify Search engine")
        return

    if 'fofa' in options.get('source'):
        fofa.Fofa(options)

    if 'shodan' in options.get('source'):
        shodan.Shodan(options)

    if 'censys' in options.get('source'):
        censys.Censys(options)

    if 'zoom' in options.get('source'):
        zoomeye.ZoomEye(options)
