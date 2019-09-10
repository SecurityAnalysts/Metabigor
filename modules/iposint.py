from core import sender
from core import utils


class IPOsint():
    """docstring for IPOsint"""

    def __init__(self, options):
        self.options = options
        # setting stuff depend on search engine
        # asn:123
        self.query = options.get('query', None)
        # target should be example.com
        self.target = options.get('target', None)
        self.output = self.options['output']
        utils.print_banner("Starting IPOsint module")
        # really do something
        self.initial()

    def initial(self):
        company = utils.get_tld(self.target)
        self.asnlookup(company)
        self.get_asn()
        self.parse_query()

    def parse_query(self):
        if not self.query:
            return None
        if '|' in self.query:
            name = self.query.split("|")[0]
            value = self.query.split("|")[1]
            if 'asn' in name:
                ips = self.get_asn_ip(value)
                utils.just_write(self.options['output'], "\n".join(ips))
                utils.just_cleanup(self.options['output'])

    def asnlookup(self, company):
        utils.print_banner(f"Starting scraping {company} from asnlookup.com")
        url = f'http://asnlookup.com/api/lookup?org={company}'
        r = sender.send_get(self.options, url, None)
        data = r.json()
        if not data:
            utils.print_bad('No IP found')
        else:
            content = "\n".join(data)
            print(content)
            utils.just_write(self.options['output'], content)
            utils.just_cleanup(self.options['output'])

    def get_asn(self):
        ip_target = utils.resolve_input(self.target)
        if not ip_target:
            return False
        utils.print_banner(f"Starting scraping detail ASN of {ip_target}")

        utils.print_info(f'Get ASN from IP: {ip_target}')
        url = f'https://ipinfo.io/{ip_target}/json'
        r = sender.send_get(self.options, url, None)
        org_info = r.json().get('org')
        asn = utils.get_asn(org_info)
        if asn:
            utils.print_info(f"Detect target running on {asn}")
            ips = self.get_asn_ip(asn)
            utils.just_write(self.options['output'], "\n".join(ips))
            utils.just_cleanup(self.options['output'])
        else:
            return False

    def get_asn_ip(self, asn):
        asn_num = utils.get_asn_num(asn)
        url = 'https://mxtoolbox.com/Public/Lookup.aspx/DoLookup2'
        data = {"inputText": f"asn:{asn_num}", "resultIndex": 1}
        r = sender.send_post(
            self.options, url, data, is_json=True)
        content = r.text
        ips = utils.grep_the_IP(content, verbose=True)
        return ips
