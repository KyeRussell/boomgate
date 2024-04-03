from . import RequirementsFile


class TestParseRequirementsFile:
    def test_empty_file(self):
        assert RequirementsFile.parse_requirements_file("") == []

    def test_simulated(self):
        file = """\
django==3.2
requests>=2.25
"""
        assert RequirementsFile.parse_requirements_file(file) == [
            {"package": "django", "operator": "==", "version": "3.2"},
            {"package": "requests", "operator": ">=", "version": "2.25"},
        ]

    def test_invalid(self):
        file = "<><>hacked<><>"
        try:
            RequirementsFile.parse_requirements_file(file)
        except ValueError as e:
            assert str(e) == "Invalid requirement line: <><>hacked<><>"
        else:
            assert False, "Expected ValueError"
