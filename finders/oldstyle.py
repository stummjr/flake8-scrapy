import ast

from finders import IssueFinder


class UrlJoinIssueFinder(IssueFinder):
    msg_code = 'SCP03'
    msg_info = 'urljoin(response.url, "/foo") can be replaced by response.urljoin("/foo")'

    def find_issues(self, node):
        if not self.issue_applies(node):
            return

        first_param = node.args[0]
        if not isinstance(first_param, ast.Attribute):
            return

        if first_param.value.id == 'response' and first_param.attr == 'url':
            # found it: first param to urljoin is response.url
            yield (node.lineno, node.col_offset, self.message)

    def issue_applies(self, node):
        return (
            isinstance(node.func, ast.Name) and
            node.func.id == 'urljoin' and
            node.args
        )
