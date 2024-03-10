import os
import subprocess
from tqdm import tqdm

def remove_include_paragraphs_from_input_file(input_file, output_file):
    output_lines = []

    with open(input_file, 'r') as file:
        lines = file.readlines()
        in_remove_section = False
        include_list = []

        for line in lines:
            if "should remove these lines:" in line:
                in_remove_section = True
            elif "The full include-list for" in line:
                in_remove_section = False

            if in_remove_section:
                include_list.append(line)

        # Write the modified include list to the output file
        with open(output_file, 'w') as output:
            for line in include_list:
                output.write(line)


def remove_unused_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        i = 0
        while i < len(lines):
            if ("remove these lines:" in lines[i] and lines[i + 1].strip() == "") or (
                    lines[i].strip() == "" and lines[i + 1].strip() == ""):
                i += 2
            else:
                file.write(lines[i])
                i += 1


def sort_lines_descending(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # 处理输入文件，将每一组的行号从大到小排序
    groups = []
    temp_file = ""
    total_group = []
    current_group = []
    for line in lines:
        if "remove these lines:" in line:
            total_group.append(temp_file)
            total_group.append(current_group)
            current_group = []
            temp_file = line
        elif line.strip().startswith('-'):
            current_group.append(line)
            current_group = sorted(current_group, key=lambda x: int(x.strip().split('// lines ')[-1].split('-')[-1]),
                                   reverse=True)

    # 处理输出文件，移除不需要的行
    with open(output_file, 'w') as f:
        for group in total_group:
            for line in group:
                f.write(line)


def remove_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        file_name = ""
    for line in tqdm(lines):
        if "should remove these lines:" in line:
            file_name = line.replace(" should remove these lines:\n", "")

        if line.startswith("- "):
            backup_file(file_name)
            delete_line(file_name,int(line.strip().split('// lines ')[-1].split('-')[-1]))
            build_path = "/home/csj/桌面/wesnoth/build"
            runcode = run_make(build_path)
            if runcode:
                backup_file(file_name)
            else:
                restore_file(file_name)

def backup_file(original_file):
    new_file = original_file + ".bak"
    try:
        with open(original_file, 'rb') as f:
            content = f.read()

        with open(new_file, 'wb') as f:
            f.write(content)

    except Exception as e:
        print("Error:", e)

def restore_file(original_file):
    backup_file = original_file + ".bak"
    try:
        with open(backup_file, 'rb') as f:
            content = f.read()
        with open(original_file, 'wb') as f:
            f.write(content)
        os.remove(backup_file)  # 删除备份文件
    except Exception as e:
        print("Error:", e)

def delete_line(file_path, line_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open(file_path, 'w', encoding='utf-8') as file:
        for index, line in enumerate(lines):
            if index != line_number - 1:
                file.write(line)

def run_make(directory):
    os.chdir(directory)
    try:
        subprocess.run(["make", "-j16"], check=True, text=True, capture_output=True)
        print("Make成功")
        return True
    except subprocess.CalledProcessError as e:
        print("Make失败")
        print("错误信息：", e.stderr)
        return False

def main():
    remove_include_paragraphs_from_input_file("/home/csj/桌面/wesnoth/build/iwyu.log", "/home/csj/桌面/wesnoth/build/iwyu_temp_1.log")
    remove_unused_lines("/home/csj/桌面/wesnoth/build/iwyu_temp_1.log","/home/csj/桌面/wesnoth/build/iwyu_temp_2.log")
    sort_lines_descending("/home/csj/桌面/wesnoth/build/iwyu_temp_2.log","/home/csj/桌面/wesnoth/build/iwyu_temp_3.log")
    remove_lines("/home/csj/桌面/wesnoth/build/iwyu_temp_3.log")


if __name__ == "__main__":
    main()
