import argparse
from auto_gen_py_project.generator import create_project

def main():
    parser = argparse.ArgumentParser(
        description="Generate a standard Python project structure"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "-i", "--init",
        action="store_true",
        help="Initialize project layout in current folder instead of creating a new folder"
    )
    args = parser.parse_args()

    create_project(args.name, init_in_current_folder=args.init)