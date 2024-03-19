# Script: use-iwyu-delete-include

This script is designed to remove specific lines from code files and test the build process to ensure that the code still builds successfully after the removal.

## Features:

remove_include_paragraphs_from_input_file: This function removes include paragraphs from the input file based on specific criteria.
remove_unused_lines: This function removes unused lines from the input file.
sort_lines_descending: This function sorts the lines in each group in descending order based on line numbers.
remove_lines: This function removes specific lines from the code file, tests the build process, and restores the file if the build fails.

## Usage:

Modify the input file as needed.
Run the script using the appropriate function to remove lines.
The script will test the build process and either keep the changes if the build is successful or restore the original file if the build fails.

## Instructions:

Run the script with the desired function to remove lines from code files.
Make sure to backup files before making any changes.
Monitor the build process to ensure that the code still builds successfully after line removal.

## Note:

This script requires Python 3.x and the tqdm package to be installed.
Use caution when removing lines from code files, as it may impact the functionality of the code.
Always backup files and verify the build process after making changes.
Disclaimer: Use this script at your own risk. The author is not responsible for any code or system failures resulting from the use of this script.

## 中文说明

[点击查看中文说明](README_CN.md)