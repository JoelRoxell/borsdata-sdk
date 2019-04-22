## Dist
`python -m pip install --user --upgrade setuptools wheel`

`python -m pip install --user --upgrade twine`

### Create dist
`python setup.py sdist bdist_wheel`


### Upload
`pythono -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
``