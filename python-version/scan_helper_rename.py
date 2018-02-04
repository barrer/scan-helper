# -*- coding: utf-8 -*-
# version: python 3
# ==========
# 作用：
# 批量重命名文件
# ==========
# 操作步骤：
# 使用时修改main方法中的"re.sub"替换规则
# ==========
import sys, os, re

path = '/Users/osx/Desktop/test'  # 处理目录【修改】
suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】


def get_file_list(file_list_path, file_list_suffix):
    """得到指定后缀的文件列表"""

    exclude = (['.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini'])
    result_list = []
    if os.path.isfile(file_list_path):
        result_list.append(os.path.abspath(file_list_path))
    else:
        for dir_path, dir_names, file_names in os.walk(file_list_path):
            if os.path.abspath(dir_path) != os.path.abspath(file_list_path):  # 只允许 1 层目录
                continue
            for name in file_names:
                if (not os.path.basename(name) in exclude) \
                        and (os.path.splitext(name)[1][1:] == file_list_suffix):  # 指定后缀
                    abs_path = os.path.abspath(os.path.join(dir_path, name))
                    result_list.append(abs_path)
    return result_list


def main():
    """主方法／main方法"""

    count = 0
    file_list = get_file_list(path, suffix)
    for tar in file_list:
        base_name = os.path.basename(tar)
        new_base_name = re.sub('Untitled.FR12 - ', '', base_name)
        new_path = os.path.join(os.path.dirname(tar), new_base_name)
        print('%s --> %s' % (base_name, new_base_name))
        os.rename(tar, os.path.abspath(new_path))
        count += 1

    print('----------')
    print('总共处理了：%s' % (count))


main()
