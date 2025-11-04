# Data Science and Machine Learning Vault

The required _Python_ version for this project is _3.12.x._

## About me

My name is _Santiago Komadina_ and I've been working at Jala Soft & Jala University for the past couple years. I am one of the original members of the **Generative AI** team in _Jala R&D_.

I've been specialized in NLP and GEN AI.

Starting this year, I am also a professor at _Jala University_ teaching deep learning and generative AI.

## Setup environment

As usual setup your virtual environment:

```
$ python -m venv .venv
$ source venv/bin/activate
$ pip install --upgrade pip setuptools
$ pip install -r requirements-dev.txt
$ pip install -e .
```

*Note:* May be you can automatize this process? What does Alan in Valis can tell you about that?

## Basic code compliance

```
$ black .
All done! ✨ 🍰 ✨
X files left unchanged.
$ mypy .
Success: no issues found in X source files
```

## About the CI/CD pipeline

This `monorepo` comes with a pre-configured CI/CD pipeline that is triggered every time a push is made to a **merge request** or when a **merge request** is integrated into the **main** branch.

The pipeline is configured to:

- Execute **code compliance** checks.
- Generate documentation.

> You may add more stages or jobs to the pipeline, but make sure you **do not remove the existing ones**. In addition, make sure you do your best to **keep the pipeline green** at all times.
