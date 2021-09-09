build:
	python setup.py sdist bdist_wheel

upload-test: build
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload-prod: build
	python -m twine upload dist/*

deploy-tools: 
	python -m pip install --user --upgrade setuptools wheel
	python -m pip install --user --upgrade twine

clean: 
	rm -r dist
	rm -r build
	rm -r borsdata_sdk.egg-info