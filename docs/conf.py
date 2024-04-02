from datetime import datetime

project = "Boomgate"
copyright = f"{datetime.now().year}, Kye Russell"
author = "Kye Russell"

extensions = ["myst_parser"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


html_theme = "shibuya"
html_theme_options = {
    "accent_color": "ruby",
    "nav_links": [
        {"title": "GitHub", "url": "https://github.com/KyeRussell/boomgate"},
        {"title": "PyPI", "url": "https://pypi.org/projects/boomgate"},
    ],
}

html_static_path = ["_static"]
