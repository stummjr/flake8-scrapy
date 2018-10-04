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


class OldSelectorIssueFinder(IssueFinder):
    msg_code = 'SCP04'
    msg_info = 'use response.selector or response.xpath or response.css instead'

    def is_response_dot_body_as_unicode(self, node):
        """ Returns True if node represents `response.body_as_unicode()`
        """
        return (
            isinstance(node, ast.Call) and
            isinstance(node.func, ast.Attribute) and
            node.func.value.id == 'response' and
            node.func.attr == 'body_as_unicode'
        )

    def is_response_dot_text_or_body(self, node):
        """ Return whether or not a node represents `response.text` or
            `response.body`
        """
        return (
            isinstance(node, ast.Attribute) and
            node.value.id == 'response' and
            node.attr in ('text', 'body')
        )

    def issue_applies(self, node):
        return (
            isinstance(node.value, ast.Call) and
            isinstance(node.value.func, ast.Name) and
            node.value.func.id == 'Selector'
        )

    def find_issues(self, node):
        if not self.issue_applies(node):
            return

        if node.value.args:
            param = node.value.args[0]
            found_issue = (
                self.is_response_dot_body_as_unicode(param) or
                self.is_response_dot_text_or_body(param)
            )
            if found_issue:
                return [(node.lineno, node.col_offset, self.message)]

        # look for sel = Selector(text=response.text)
        for kw in node.value.keywords:
            found_issue = (
                kw.arg == 'text' and
                self.is_response_dot_text_or_body(kw.value) or
                self.is_response_dot_body_as_unicode(kw.value)
            )
            if found_issue:
                return [(node.lineno, node.col_offset, self.message)]
