import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': ['tkinter', 'datetime', 'PIL', 'sqlite3', 'threading', 'traceback'],
    'include_files': [
        ('img', 'img'),
        ('tree', 'tree'),
        ('base', 'base'),
        ('interface.py', 'interface.py')
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Verttical GR",
    version="1.0",
    description="Gestão",
    options={"build_exe": build_exe_options},
    executables=[Executable("tree/interface.py", base=base)]
)
