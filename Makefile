configure:
	git submodule update --init
	pip install -r requirements.txt

test:
	pytest tests -x

clean:
	rm -rf assets
	rm -rf tests/__pycache__ tests/*.pyc tests/assets tests/utils/__pycache__
	rm -rf debugclient/__pycache__  debugclient/*.pyc
