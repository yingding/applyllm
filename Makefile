PACKAGE_DIR=.
REPO_NAME=gitlab-lrz
PYPI_TEST=testpypi
PYPI_PROD=pypi
PROJECT_NAME=applyllm
PACKAGE_NAME=applyllm
PYTHON?=python3

# rm -rf ${PACKAGE_DIR}/__pycache__
# rm -rf ${PACKAGE_DIR}/dist

build:
	${PYTHON} -m build ${PACKAGE_DIR} -o ${PACKAGE_DIR}/dist

lrz:
	${PYTHON} -m twine upload --verbose --repository ${REPO_NAME} ${PACKAGE_DIR}/dist/*

testpypi:
	${PYTHON} -m twine upload --verbose --repository ${PYPI_TEST} ${PACKAGE_DIR}/dist/*

pypi:
	${PYTHON} -m twine upload --verbose --repository ${PYPI_PROD} ${PACKAGE_DIR}/dist/*

applyllm:
	${PYTHON} -m twine upload --verbose --repository ${PROJECT_NAME} ${PACKAGE_DIR}/dist/*

clean:
	${PYTHON} -c "import shutil; shutil.rmtree('__pycache__', True); shutil.rmtree('dist', True)"

reload:
	${PYTHON} -m pip uninstall -y ${PACKAGE_NAME} && ${PYTHON} -c "import glob,subprocess,sys; f=glob.glob('dist/${PACKAGE_NAME}*.whl'); sys.exit(subprocess.call([sys.executable,'-m','pip','install']+f))" 

reinstall:
	${PYTHON} -m pip uninstall -y ${PACKAGE_NAME} && ${PYTHON} -c "import glob,subprocess,sys; f=glob.glob('dist/${PACKAGE_NAME}*.whl'); sys.exit(subprocess.call([sys.executable,'-m','pip','install','--user']+f))"
 

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
