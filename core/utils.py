import os 
import re 
import json
import base64 
import random
import time
import socket
import ipaddress
import urllib.parse
from configparser import ConfigParser, ExtendedInterpolation
from bs4 import BeautifulSoup
import tldextract

# Console colors
W = '\033[1;0m'   # white
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G, R, B, P, C, O, GR]

info = '{0}[*]{1} '.format(B, GR)
ques = '{0}[?]{1} '.format(C, GR)
bad = '{0}[-]{1} '.format(R, GR)
good = '{0}[+]{1} '.format(G, GR)

debug = '{1}[{0}DEBUG{1}]'.format(G, GR)

full_country_code = ['AF', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'CI', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'EH', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GN', 'GW', 'GY', 'HT', 'HM', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IL', 'IT', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY', 'LI', 'LT', 'LU', 'MO', 'MK', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'FM', 'MD', 'MC', 'MN', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'AN', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'SH', 'KN', 'LC', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'CS', 'SC', 'SL', 'SG', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK', 'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VE', 'VU', 'VN', 'VG', 'VI', 'WF', 'YE', 'ZW']


'''
 Beatiful print
'''


def print_block(text, tag='RUN'):
    print(f'{GR}' + '-'*40)
    print(f'{GR}[{B}{tag}{GR}] {G}{text}')
    print(f'{GR}' + '-'*40)


def print_banner(text):
    print_block(text, tag='RUN')


def print_debug(options, text):
    if options['debug']:
        print(debug, text)


def print_info(text):
    print(info + text)


def print_ques(text):
    print(ques + text)


def print_good(text):
    print(good + text)


def print_bad(text):
    print(bad + text)


def check_output(output):
    abs_path = os.path.abspath(output)
    if not_empty_file(output):
        print('{1}--==[ Check the output: {2}{0}'.format(abs_path, G, P))


def not_empty_file(filepath):
    if not filepath:
        return False
    fpath = os.path.normpath(filepath)
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

'''
 String utils
'''


def random_sleep(min=2, max=5):
    time.sleep(random.randint(min, max))


def resolve_input(string_in):
    if valid_ip(string_in):
        return string_in
    else:
        try:
            ip = socket.gethostbyname(get_domain(string_in))
            return ip
        except:
            return False
    return False


# just get main domain
def get_domain(string_in):
    parsed = urllib.parse.urlparse(string_in)
    domain = parsed.netloc if parsed.netloc else parsed.path
    return domain


# check if string is IP or not
def valid_ip(string_in):
    try:
        ipaddress.ip_interface(str(string_in).strip())
        return True
    except:
        return False


# just beatiful soup the html
def soup(html):
    soup = BeautifulSoup(html, "lxml")
    return soup


def get_tld(string_in):
    try:
        result = tldextract.extract(string_in)
        return result.domain
    except:
        return string_in


def get_asn_num(string_in):
    return str(string_in).lower().replace('as', '')


def get_json(text):
    return json.loads(text)


def get_query(url):
    return urllib.parse.urlparse(url).query


def get_path(url):
    return urllib.parse.urlparse(url).path


def get_parent(path):
    return os.path.dirname(path)


def get_filename(path):
    return os.path.basename(path)


def join_path(parent, child):
    parent = os.path.normpath(parent)
    child = os.path.normpath(child)
    return os.path.join(parent, child.strip('/'))


def strip_slash(string_in):
    if '/' in string_in:
        string_in = string_in.replace('/', '_')
    return string_in


# get country code from query
def get_country_code(query, source='shodan'):
    try:
        if source == 'shodan':
            m = re.search('country:\"[a-zA-Z]+\"', query)
            country_code = m.group().split(':')[1].strip('"')
        elif source == 'fofa':
            m = re.search('country=[a-zA-Z]+', query)
            country_code = m.group().split('=')[1].strip('"')

        elif source == 'censys':
            m = re.search(
                '(country\_code:.[a-zA-Z]+)|(country:.([\"]?)[a-zA-Z]+.[a-zA-Z]+([\"]?))', query)
            country_code = m.group()

        return country_code
    except:
        return False


# get city name from query
def get_city_name(query, source='shodan'):
    if source == 'shodan':
        m = re.search('city:\"[a-zA-Z]+\"', query)
        city_code = m.group().split(':')[1].strip('"')

    elif source == 'fofa':
        m = re.search('city=[a-zA-Z]+', query)
        country_code = m.group().split('=')[1].strip('"')

    return city_code


def get_asn(string_in):
    if not string_in:
        return False
    m = re.search(r'AS[0-9]+', string_in.upper())
    if m:
        asn_num = m.group()
        return asn_num
    else:
        return False


# get cve number
def get_cve(source):
    m = re.search('CVE-\d{4}-\d{4,7}', source)
    if m:
        cve = m.group()
        return cve
    else:
        return 'N/A'


def grep_the_IP(data, verbose=False):
    cidr_regex = "((\d){1,3}\.){3}(\d){1,3}(\/(\d){1,3})?"
    ips = []
    p = re.compile(cidr_regex)
    for m in p.finditer(data):
        ips.append(m.group())
        if verbose:
            print(m.group())
    return ips


# strip out the private IP
def strip_private_ip(data):
    new_data = []
    for item in data:
        try:
            if not ipaddress.ip_address(item).is_private:
                new_data.append(item)
        except:
            new_data.append(item)

    return new_data


def url_encode(string_in):
    return urllib.parse.quote(string_in)


def url_decode(string_in):
    return urllib.parse.unquote(string_in)


def just_b64_encode(string_in):
    return base64.b64encode(string_in.encode()).decode()


def just_b64_decode(string_in):
    return base64.b64decode(string_in.encode()).decode()


def is_json(string_in):
    try:
        json_object = json.loads(string_in)
    except:
        try:
            if type(literal_eval(string_in)) == dict:
                return True
        except:
            return False
    return True

'''
 File utils
'''


# get credentials
def get_cred(options, source):
    config_file = options.get('config')
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    if 'fofa' in source:
        cred = config.get('Credentials', 'fofa')
    if 'shodan' in source:
        cred = config.get('Credentials', 'shodan')
    if 'censys' in source:
        cred = config.get('Credentials', 'censys')
    if 'github' in source:
        cred = config.get('Credentials', 'github')

    print_debug(options, cred)
    username = cred.split(':')[0].strip()
    password = cred.split(':')[1].strip()

    return username, password


# set session 
def set_session(options, cookies, source):
    print_debug(options, cookies)
    config_file = options.get('config')
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)

    if 'fofa' in source:
        config.set('Cookies', 'fofa', cookies)
    if 'shodan' in source:
        config.set('Cookies', 'shodan', cookies)
    if 'censys' in source:
        config.set('Cookies', 'censys', cookies)

    with open(config_file, 'w') as configfile:
        config.write(configfile)


def make_directory(directory, verbose=False):
    directory = os.path.normpath(directory)
    if not os.path.exists(directory):
        if verbose:
            print_good('Make new directory: {0}'.format(directory))
        os.makedirs(directory)


def just_read(filename, get_json=False, get_list=False):
    if not filename:
        return False
    filename = os.path.normpath(filename)
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            data = f.read()
        if get_json and is_json(data):
            return json.loads(data)
        elif get_list:
            return data.splitlines()
        return data

    return False


def just_write(filename, data, is_json=False, verbose=False):
    real_path = os.path.normpath(filename)
    try:
        print_good("Writing {0}".format(filename)) if verbose else None
        if is_json:
            with open(real_path, 'a+') as f:
                json.dump(data, f)
        else:
            with open(real_path, 'a+') as f:
                f.write(data)
    except:
        print_bad("Writing fail: {0}".format(real_path))
        return False


# unique and strip the blank line
def just_cleanup(filename, verbose=True):
    if verbose:
        check_output(filename)
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            raw = f.read().splitlines()

        data = [x for x in raw if str(x).strip() != '']
        data.sort()
        with open(filename, 'w+') as o:
            for item in set(data):
                o.write(item + "\n")

    return False

