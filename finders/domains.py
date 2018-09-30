import ast
from six.moves.urllib.parse import urlparse

from finders import IssueFinder


class UnreachableDomainIssueFinder(IssueFinder):
    msg_code = 'SCP01'
    msg_info = "allowed_domains doesn't allow this URL from start_urls"

    def __init__(self, *args, **kwargs):
        super(UnreachableDomainIssueFinder, self).__init__(*args, *kwargs)
        self.allowed_domains = []
        self.start_urls = []

    def get_list_metadata(self, node):
        return [
            (subnode.lineno, subnode.col_offset, subnode.s)
            for subnode in node.value.elts
            if isinstance(subnode, ast.Str)
        ]

    def is_list_assignment(self, node, var_name):
        return (
            isinstance(node.targets[0], ast.Name) and
            isinstance(node.value, (ast.List, ast.Tuple)) and
            node.targets[0].id == var_name
        )

    def url_in_allowed_domains(self, url):
        netloc = urlparse(url).netloc
        return any(
            domain in netloc
            for _, _, domain in self.allowed_domains
        )

    def find_issues(self, node):
        if self.is_list_assignment(node, var_name='allowed_domains'):
            self.allowed_domains = self.get_list_metadata(node)

        if self.is_list_assignment(node, var_name='start_urls'):
            self.start_urls = self.get_list_metadata(node)

        if not all((self.allowed_domains, self.start_urls)):
            return

        for line, col, url in self.start_urls:
            if not self.url_in_allowed_domains(url):
                yield (line, col, self.message)
