import pytest

from . import run_checker


@pytest.mark.parametrize('code,expected', [
    ('Request(x, callback=lambda x: x)', 1),
    ('scrapy.Request(x, callback=lambda x: x)', 1),
    ('scrapy.Request(x, lambda x: x)', 1),
    ('Request(x, callback=self.parse)', 0),
    ('scrapy.Request(x, callback=self.parse)', 0),
    ('scrapy.Request(x, self.parse)', 0),
])
def test_find_lambda_callback_issue(code, expected):
    issues = run_checker(code)
    assert len(issues) == expected
