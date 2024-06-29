# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Helper script for updating pyproject.toml

Check drawlib.__init__.py and get
- version
- lib name
- author
- contact

Then, updadate pyproject.toml
"""

import glob
import os


def cd_to_project_root():
    """Change directory to project root."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    os.chdir("../")


def count_lines_in_file(file_path):
    """Counts the number of lines in a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)


def count_lines_in_directory(directory):
    """Counts the number of lines in each Python file in the given directory and returns a sorted list."""
    file_lines = []
    for file_path in glob.glob(os.path.join(directory, "**", "*.py"), recursive=True):
        lines = count_lines_in_file(file_path)
        file_lines.append((file_path, lines))

    # Sort the list by the number of lines in descending order
    file_lines.sort(key=lambda x: x[1], reverse=True)
    return file_lines


def main(project_root):
    """Main function for counting lines."""
    print(f"==={project_root}===")
    lines_per_file = count_lines_in_directory(project_root)

    max_path_length = max(len(file_path) for file_path, _ in lines_per_file)
    for file_path, line_count in lines_per_file:
        print(f"{file_path.ljust(max_path_length)} : {line_count} lines")

    print("======================")
    total_lines = sum(line_count for _, line_count in lines_per_file)
    print(f"Total number of lines in all Python files: {total_lines}")


if __name__ == "__main__":
    cd_to_project_root()
    main("./drawlib")
    print()
    main("./tests")
