from github import Github
from core import sender
from core import utils


class GitSearch():
    """docstring for GitSearch"""

    def __init__(self, options):
        self.options = options
        self.base_url = "https://github.com"
        self.query = options['query']
        utils.print_banner("Starting scraping from Github")
        self.output = self.options['output']
        self.source = self.options.get('source', 'code')

        self.sess = self.do_login()
        if self.sess:
            utils.print_good(
                "Github Authentication success")
        else:
            utils.print_bad("Github Authentication fail, you gonna lose some features")
        # really do something
        self.gen_output_path()
        self.initial()
        self.conclude()

    def initial(self):
        # search code
        if 'code' in self.source.lower() or self.source.lower() == '*':
            utils.print_good("Search for code by {0}".format(self.query))
            results = self.sess.search_code(
                order='desc', sort='indexed', query=self.query)
            self.main_routine(results, kind='code')

        # search issue
        if 'issue' in self.source.lower() or self.source.lower() == '*':
            utils.print_good("Search for issues by {0}".format(self.query))
            results = self.sess.search_issues(
                order='desc', query=self.query)
            self.main_routine(results, kind='issue')

        # search commit
        if 'commit' in self.source.lower() or self.source.lower() == '*':
            utils.print_good("Search for commits by {0}".format(self.query))
            results = self.sess.search_commits(
                order='desc', query=self.query)
            self.main_routine(results, kind='commit')

        # search repo
        if 'repo' in self.source.lower() or self.source.lower() == '*':
            utils.print_good("Search for repos by {0}".format(self.query))
            results = self.sess.search_repositories(
                order='desc', query=self.query)
            self.main_routine(results, kind='repo')

        # search user
        if 'user' in self.source.lower() or self.source.lower() == '*':
            utils.print_good("Search for users by {0}".format(self.query))
            results = self.sess.search_users(
                order='desc', query=self.query)
            self.main_routine(results, kind='user')

    # loop through page and get result
    def main_routine(self, results, kind='code'):
        pages = self.get_page(results)
        utils.print_info(f"Detect {str(pages)} pages by search for {kind}")
        for i in range(pages):
            # utils.print_info(f"Search in pages {str(i)}")
            page_results = results.get_page(page=i)
            if not page_results:
                return 
            # content from each page
            for result in page_results:
                if kind == 'code':
                    item = self.parse_code(result)
                if kind == 'issue':
                    item = self.parse_issue(result)
                if kind == 'commit':
                    item = self.parse_commit(result)
                if kind == 'repo':
                    item = self.parse_repo(result)
                if kind == 'user':
                    item = self.parse_user(result)
                self.write_result(item, kind=kind)

    def parse_code(self, result):
        content = result.decoded_content.decode('utf-8')
        raw_url = result.download_url
        full_url = result.html_url
        repo_url = result.repository.html_url
        user = self.parse_get_user(repo_url)

        item = {
            'content': content,
            'raw_url': raw_url,
            'full_url': full_url,
            'repo_url': repo_url,
            'user': user,
        }
        return item

    def parse_issue(self, result):
        content = result.raw_data
        raw_url = result.comments_url
        full_url = result.html_url
        repo_url = result.repository.html_url
        user = result.user.login

        item = {
            'content': content,
            'raw_url': raw_url,
            'full_url': full_url,
            'repo_url': repo_url,
            'user': user,
        }
        return item

    def parse_commit(self, result):
        content = result.raw_data
        raw_url = result.comments_url
        full_url = result.html_url
        repo_url = self.parse_get_repo(result.html_url)
        user = result.committer.login

        item = {
            'content': content,
            'raw_url': raw_url,
            'full_url': full_url,
            'repo_url': repo_url,
            'user': user,
        }
        return item

    def parse_repo(self, result):
        content = result.raw_data
        raw_url = result.comments_url
        full_url = result.html_url
        repo_url = result.html_url
        user = self.parse_get_user(repo_url)

        item = {
            'content': content,
            'raw_url': raw_url,
            'full_url': full_url,
            'repo_url': repo_url,
            'user': user,
        }
        return item

    def parse_user(self, result):
        content = result.raw_data
        repos_url = result.repos_url
        full_url = result.html_url
        orgs = self.parse_orgs(result.get_orgs())
        user = result.login
        item = {
            'content': content,
            'repos_url': repos_url,
            'full_url': full_url,
            'orgs': orgs,
            'user': user,
        }
        return item

    def get_page(self, results):
        return int(results.totalCount / 10)

    def parse_orgs(self, raw_orgs):
        orgs = [x.login for x in raw_orgs.get_page(page=0)]
        return ",".join(orgs)

    def parse_get_user(self, url):
        parsed = utils.get_path(url).strip('/')
        if '/' in parsed:
            return parsed.split('/')[0]
        else:
            return parsed

    def parse_get_repo(self, url):
        parsed = url.strip('/').split('commit')[0]
        return parsed

    # do login to github
    def do_login(self):
        username, password = utils.get_cred(self.options, source='github')
        g = Github(username, password)
        try:
            _ = g.get_emojis()
            return g
        except:
            utils.print_bad(f"Login fail as {username}")
            return False

    # verify if string is user or org
    def user_or_org(self, string_in):
        try:
            self.sess.get_organization(string_in)
            return {'org': string_in}
        except:
            pass
        try:
            self.sess.get_user(string_in)
            return {'user': string_in}
        except:
            pass
        return {}

    def gen_output_path(self):
        outdir = utils.get_parent(self.options.get('output'))
        basename = utils.get_filename(self.options.get('output'))
        self.options['repo_output'] = utils.join_path(outdir, f'repo-{basename}')
        self.options['user_output'] = utils.join_path(outdir, f'user-{basename}')
        self.options['org_output'] = utils.join_path(outdir, f'org-{basename}')

    def write_result(self, item, kind='code'):
        # for item in real_results:
        self.writing_raw(item)
        if kind != 'user':
            utils.just_write(
                self.options['repo_output'], item.get('repo_url') + "\n")
        # store user
        user = self.user_or_org(item.get('user'))
        if user.get('user'):
            utils.just_write(
                self.options['user_output'], user.get('user') + "\n")
        elif user.get('org'):
            utils.just_write(
                self.options['org_output'], user.get('org') + "\n")

        utils.just_cleanup(self.options['repo_output'], verbose=False)
        utils.just_cleanup(self.options['user_output'], verbose=False)
        utils.just_cleanup(self.options['org_output'], verbose=False)

    def writing_raw(self, item):
        if self.options.get('store_content'):
            utils.just_write(self.options['store_content'], str(item))

    def conclude(self):
        utils.print_block(self.options['repo_output'], tag='OUTPUT')
        utils.print_block(self.options['user_output'], tag='OUTPUT')
        utils.print_block(self.options['org_output'], tag='OUTPUT')
