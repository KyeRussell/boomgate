import pytest
from .requirements_specifier import parse_requirements_specifier

requirement_specifiers = [
    "A",
    "A.B-C_D",
    "aa",
    "name",
    "name<=1",
    "name>=3",
    "name>=3,<2",
    "name@http://foo.com",
    "name [fred,bar] @ http://foo.com ; python_version=='2.7'",
    "name[quux, strange];python_version<'2.7' and platform_version=='2'",
    "name; os_name=='a' or os_name=='b'",
    # Should parse as (a and b) or c
    "name; os_name=='a' and os_name=='b' or os_name=='c'",
    # Overriding precedence -> a and (b or c)
    "name; os_name=='a' and (os_name=='b' or os_name=='c')",
    # should parse as a or (b and c)
    "name; os_name=='a' or os_name=='b' and os_name=='c'",
    # Overriding precedence -> (a or b) and c
    "name; (os_name=='a' or os_name=='b') and os_name=='c'",
]


@pytest.mark.parametrize("requirements_specifier", requirement_specifiers)
def test_parse_requirements_specifier(requirements_specifier):
    """Test :py:func:`parse_requirements_specifier`.

    This uses the suite of test specifiers in PEPM 508.
    """
    # This currently just tests that everything is parsable. It doesn't yet check if
    # the parsed output is correct.
    parse_requirements_specifier(requirements_specifier)
