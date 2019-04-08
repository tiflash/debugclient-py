configure:
	git submodule update --init
	python -m pip install -r requirements.txt
	python tests/utils/configenv.py

test:
	tox .

clean:
	rm -rf assets
	rm -rf tests/__pycache__ tests/*.pyc tests/assets tests/utils/__pycache__
	rm -rf debugclient/__pycache__  debugclient/*.pyc
