# How to set up for deploy to PyPi

```bash
python setup.py sdist bdist_wheel
```

# How to deploy to PyPi

## First time

```bash
python -m twine upload dist/*
```

## Update the modules

```bash
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
