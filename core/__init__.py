import os
import pathlib

# Ensure the package points to the app implementation inside toppers_project
# The real app code lives at: <project-root>/toppers_project/<app_name>
APP_DIR = pathlib.Path(__file__).resolve().parent.parent / 'toppers_project' / 'core'
if APP_DIR.exists():
	__path__.insert(0, str(APP_DIR))
