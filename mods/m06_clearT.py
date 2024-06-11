import unicodedata
import os
import re


def full2half(input_str):
    return ''.join([unicodedata.normalize('NFKC', char) for char in input_str])


try:
    from opencc import OpenCC

    cc = OpenCC('t2s')  # 't2s'表示繁体转简体


    def clearT(s):
        s = cc.convert(full2half(s))
        return s.strip().strip(r'\n').replace('\n', '\\n').replace('\r', '')

except ModuleNotFoundError:
    print('opencc 缺失，繁体转简体失效')


    def clearT(s):
        s = full2half(s)
        return s.strip().strip(r'\n').replace('\n', '\\n').replace('\r', '')


def get_all_files_in_directory(directory, ext=''):
    custom_sort_key_re = re.compile('([0-9]+)')

    def custom_sort_key(s):
        # 将字符串中的数字部分转换为整数，然后进行排序
        return [int(x) if x.isdigit() else x for x in custom_sort_key_re.split(s)]

    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(root, file)
                all_files.append(file_path)
    return sorted(all_files, key=custom_sort_key)
