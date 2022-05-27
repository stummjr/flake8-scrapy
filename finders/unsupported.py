import ast

from finders import IssueFinder


class LambdaCallbackIssueFinder(IssueFinder):
    msg_code = 'SCP05'
    msg_info = 'callback should not be a lambda'

    def is_scrapy_request(self, node):
        return (
            isinstance(node.func, ast.Attribute) and
            node.func.value.id == 'scrapy' and
            node.func.attr == 'Request'
        )

    def is_raw_request(self, node):
        return (
            isinstance(node.func, ast.Name) and
            node.func.id == 'Request'
        )

    def issue_applies(self, node):
        return (
            self.is_raw_request(node) or
            self.is_scrapy_request(node)
        )

    def find_issues(self, node):
        if not self.issue_applies(node):
            return

        if len(node.args) >= 2:
            callback = node.args[1]
            if isinstance(callback, ast.Lambda):
                return [(callback.lineno, callback.col_offset, self.message)]

        for kw in node.keywords:
            if kw.arg == 'callback' and isinstance(kw.value, ast.Lambda):
                return [(node.lineno, node.col_offset, self.message)]
