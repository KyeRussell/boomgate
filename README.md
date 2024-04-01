# boomgate

Boomgate helps you identify and mitigate the risks of using third-party libraries in
your Python projects.

## ⚠️ This is in a pre-pre-pre-release state! ⚠️

This project is not remotely ready for anyone to look at, let alone use.

I will not provide support, nor will I accept PRs.

## Vision

I intend for Boomgate to allow you to define a policy for your project that describes
the risks you are willing to accept when using third-party libraries. Boomgate will
evaluate your project's dependencies against this policy, report on any risks that you
deem unacceptable, and—also per your defined policy—suggest mitigation strategies.

For example, you may decide that you are not willing to use a dependency if its author's
email address's domain is not registered (i.e. DNS returns `NXDOMAIN`), or you may
decide that all dependencies (barring a list of excepted 'trusted' dependencies) require
a security audit before they can be used.

In this example, Boomgate can be configured to block your project's CI/CD pipeline if
one of these conditions is met by your project's resolved dependencies.

See my rough list of idea in the
[GitHub issues list](https://github.com/KyeRussell/boomgate/issues).

## Developing

To get started, clone the repository and run the following command:

```bash
uv pip install -e . -r pyproject.toml --extra=dev
```

This will install the project in editable mode with all development dependencies.
