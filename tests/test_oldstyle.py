import pytest
from . import run_checker


@pytest.mark.parametrize('code,expected,issue_code', [
    ('response.urljoin("/foo")', 0, ''),
    ('urljoin(response.url, "/foo")', 1, 'SCP03'),
    ('url = urljoin(response.url, "/foo")', 1, 'SCP03'),
])
def test_has_old_urljoin(code, expected, issue_code):
    issues = run_checker(code)
    assert len(issues) == expected
    if not issues:
        return
    assert issue_code in issues[0][2]
