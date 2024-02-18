PACKAGE_DIR=.
REPO_NAME=gitlab-lrz
PYPI_TEST=testpypi
PYPI_PROD=pypi
PROJECT_NAME=applyllm
PACKAGE_NAME=applyllm

build:
	python3 -m build ${PACKAGE_DIR} -o ${PACKAGE_DIR}/dist

lrz:
	python3 -m twine upload --verbose --repository ${REPO_NAME} ${PACKAGE_DIR}/dist/*

testpypi:
	python3 -m twine upload --verbose --repository ${PYPI_TEST} ${PACKAGE_DIR}/dist/*

pypi:
	python3 -m twine upload --verbose --repository ${PYPI_PROD} ${PACKAGE_DIR}/dist/*

applyllm:
	python3 -m twine upload --verbose --repository ${PROJECT_NAME} ${PACKAGE_DIR}/dist/*

clean:
	rm -rf ${PACKAGE_DIR}/__pycache__
	rm -rf ${PACKAGE_DIR}/dist

reload:
	python3 -m pip uninstall -y ${PACKAGE_NAME} && python3 -m pip install ${PACKAGE_DIR}/dist/${PACKAGE_NAME}*.whl

reinstall:
	python3 -m pip uninstall -y ${PACKAGE_NAME} && python3 -m pip install --user ${PACKAGE_DIR}/dist/${PACKAGE_NAME}*.whl
 

# local reload
# make clean && make build && make reload

# kf notebook reinstall
# make clean && make build && make reinstall

# local release pypi package upload
# make clean && make build && make pypi

# https://earthly.dev/blog/python-makefile/
# make file need tab, instead of space 4, use cat -e -t -v  Makefile
# https://stackoverflow.com/questions/16931770/makefile4-missing-separator-stop/16945143#16945143
# can't upload with twine for pypi project using project token with `make applyllm`.
