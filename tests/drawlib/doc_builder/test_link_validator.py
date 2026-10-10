# Copyright (c) 2026 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

import pytest

from drawlib._builder.doc_builder.compiler.base import validate_markdown_links


def test_validate_markdown_links_valid() -> None:
    content = """# Sample Document

Here are valid links:
- [Relative Page](./page.md)
- [Parent Page](../other/doc.md)
- [Web Link](https://github.com/yuichi110/drawlib)
- [HTTP Link](http://example.com)
- [Anchor](#section-1)
- ![Local Image](_assets/logo.png)
- [Mail](mailto:hello@example.com)

Code blocks with file:// or absolute paths must be ignored:
```python
path = "file:///usr/local/google/home/test"
os.system("/usr/bin/python")
```

Inline code must also be ignored: `file:///path/to/file` and `/home/user`.
"""
    # Should not raise any exception
    validate_markdown_links("/path/to/doc.md", content)


@pytest.mark.parametrize(
    "bad_link,expected_target",
    [
        ("[Bad Link](file:///usr/local/home/test.md)", "file:///usr/local/home/test.md"),
        ("[Bad Link](file://C:/Users/test/doc.md)", "file://C:/Users/test/doc.md"),
        ("[Bad Link](/usr/local/share/doc.md)", "/usr/local/share/doc.md"),
        ("[Bad Link](/home/user/workspace/doc.md)", "/home/user/workspace/doc.md"),
        ("[Bad Link](/Users/john/repo/doc.md)", "/Users/john/repo/doc.md"),
        (r"[Bad Link](C:\Users\john\repo\doc.md)", r"C:\Users\john\repo\doc.md"),
        ('<a href="file:///tmp/doc.html">Link</a>', "file:///tmp/doc.html"),
        ('<img src="/home/user/pic.png" alt="Pic">', "/home/user/pic.png"),
    ],
)
def test_validate_markdown_links_violations(bad_link: str, expected_target: str) -> None:
    content = f"""# Header

Some introductory text.
{bad_link}
End of document.
"""
    with pytest.raises(ValueError) as excinfo:
        validate_markdown_links("/path/to/doc.md", content)

    err = str(excinfo.value)
    assert 'Forbidden absolute path or file:// URL detected in "/path/to/doc.md":' in err
    assert "Line 4:" in err
    assert expected_target in err
