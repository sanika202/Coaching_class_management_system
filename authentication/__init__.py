import pathlib

APP_DIR = pathlib.Path(__file__).resolve().parent.parent / 'toppers_project' / 'authentication'
if APP_DIR.exists():
	__path__.insert(0, str(APP_DIR))
