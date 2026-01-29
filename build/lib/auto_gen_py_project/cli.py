import argparse
from auto_gen_py_project.generator import create_project

def main():
    parser = argparse.ArgumentParser(description="Generate a Python package layout")
    parser.add_argument("name", help="Project name")
    args = parser.parse_args()
    create_project(args.name)