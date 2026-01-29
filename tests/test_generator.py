from auto_gen_py_project.generator import create_project
from pathlib import Path
import shutil

def test_project_creation():
    name = "test_project"
    create_project(name)

    assert Path(name).exists()
    assert Path(name, name, "main.py").exists()

    shutil.rmtree(name)
