import pytest

from . import run_checker
from finders.oldstyle import UrlJoinIssueFinder


@pytest.mark.parametrize('code', [
    ('urljoin(response.url, "/foo")'),
    ('url = urljoin(response.url, "/foo")'),
])
def test_finds_old_style_urljoin(code):
    issues = run_checker(code)
    assert len(issues) == 1
    assert UrlJoinIssueFinder.msg_code in issues[0][2]


@pytest.mark.parametrize('code', [
    ('response.urljoin("/foo")'),
    ('url = urljoin()'),
])
def test_dont_find_old_style_urljoin(code):
    issues = run_checker(code)
    assert len(issues) == 0
