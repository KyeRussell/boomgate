<h1 align="center">Boomgate</h1>
<p align="center">
<img src="docs/logo..png" height="200px" />
</p>
<p align="center"><em>
    Identify and mitigate the risks of using third-party libraries.
</em></p>

<p align="center">
    <a href="https://pypi.org/project/boomgate/"><img src="https://img.shields.io/pypi/v/boomgate?color=%2334D058&label=PyPI%20package" alt="PyPI version"></a>
    <a href="https://github.com/KyeRussell/boomgate/actions/workflows/release.yaml"><img src="https://github.com/KyeRussell/boomgate/actions/workflows/release.yaml/badge.svg" alt="Release workflow status"></a>
    <a href="https://codecov.io/gh/KyeRussell/boomgate" ><img src="https://codecov.io/gh/KyeRussell/boomgate/graph/badge.svg?token=2XY75VWMGK"></a>
    <a href="https://boomgate.readthedocs.io"><img src="https://readthedocs.org/projects/boomgate/badge/" alt="Documentation on Read The Docs"></a>
</p>

---

This project is not remotely ready for anyone to look at, let alone use. It is in a very early proof-of-concept stage, focusing on iterative research and development. I have not settled on the project's architecture, and I am still exploring the problem space. As such, the quality of the code is very poor, and things are guaranteed to change.

I will not provide support, nor am I accepting PRs at this time.

---

## Vision

I intend for Boomgate to allow you to define a policy for your project that describes your risk acceptance with regard to your use of third-party dependencies. Boomgate will evaluate your project's third-party dependencies against this policy, report on any risks that you deem unacceptable, and—also per your defined policy—suggest mitigation strategies.

For example, you may decide that you are not willing to use a dependency if its author's email address's domain is not registered (i.e. DNS returns `NXDOMAIN`), or you may decide that all dependencies (barring a list of excepted 'trusted' dependencies) require a security audit before they can be used.

In this example, Boomgate can be configured to block your project's CI/CD pipeline if one of these conditions is met by your project's resolved dependencies. Importantly, this failure condition could simply be ressovled by an (explicit, attributable, auditable) verification by a human that a listed precaution has been taken (e.g., "Yes, I have audited the code in this new dependency.").

See my rough list of idea in the [GitHub issues list](https://github.com/KyeRussell/boomgate/issues).

## Developing

Clone the repository and run the following command:

```bash
uv pip install -e . -r pyproject.toml --extra=dev --extra=docs
```

This will install the project in editable mode with all development dependencies.

### Running tests

```bash
pytest
```
