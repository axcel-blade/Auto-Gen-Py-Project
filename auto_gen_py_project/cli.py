import argparse
from auto_gen_py_project.generator import create_project

def main():
    parser = argparse.ArgumentParser(
        description="Generate a standard Python package layout"
    )
    parser.add_argument(
        "name",
        help="Project name (e.g. my_library)"
    )

    args = parser.parse_args()
    create_project(args.name)
