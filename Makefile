# https://gnuwin32.sourceforge.net/downlinks/make.php
.PHONY: init run build clean

init:
	@python -m venv .\venv\ --prompt fishrl && .\venv\scripts\activate.bat && pip install -r .\requirements.txt

build:
	@echo building
	@.\venv\scripts\activate.bat
	@python ./build/combine_files.py && pyinstaller --onefile ./src/onefile.py
	@echo done

run:
	@echo running
	@.\venv\scripts\activate.bat
	@python ./src/main.py

run-native: build
	@echo running
	@.\dist\onefile.exe

clean:
	@echo cleaning
	@del onefile.spec
	@rmdir /s .\dist
	@rmdir /s .\build\onefile
