.PHONY: clean dist publish test_publish
.IGNORE: clean

clean:
	rmdir /s/q "./dist"

dist: clean
	py -m pip install 'twine>=1.5.0' 'build>=1.2.2'
	py -m build

publish: dist
	py -m twine upload --repository pypi dist/*


test_publish: dist
	py -m twine upload --repository testpypi dist/*
