PACKAGE_DIR=.
REPO_NAME=gitlab-lrz
PACKAGE_NAME=applyllm

build:
	python3 -m build ${PACKAGE_DIR} -o ${PACKAGE_DIR}/dist

publish:
	python3 -m twine upload --verbose --repository ${REPO_NAME} ${PACKAGE_DIR}/dist/*

clean:
	rm -rf ${PACKAGE_DIR}/__pycache__
	rm -rf ${PACKAGE_DIR}/dist

reload:
	python3 -m pip uninstall -y ${PACKAGE_NAME} && python3 -m pip install ${PACKAGE_DIR}/dist/${PACKAGE_NAME}*.whl

# make clean && make build && make reload
# make clean && make build && make publish

# https://earthly.dev/blog/python-makefile/
# make file need tab, instead of space 4, use cat -e -t -v  Makefile
# https://stackoverflow.com/questions/16931770/makefile4-missing-separator-stop/16945143#16945143
