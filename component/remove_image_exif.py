# -*- coding: utf-8 -*-
# version: python 3
# ==========
# 作用：
# 删除图片的exif信息
# 当停止脚本后再次运行会删除最后生成的5个文件（按最修改时间排序），已经有的文件跳过。
# ==========
# 依赖项：
# pip3 install Pillow
# ==========
import sys, os

import time
from PIL import Image

path = '/Users/osx/Desktop/test'  # 处理目录【修改】
suffix = 'jpg'  # "处理目录"中的指定图片后缀【修改】

out_path = os.path.join(path, 'no-exif')  # 输出目录

# if os.path.exists(out_path):
#     print('输出目录已存在，请移走后再运行程序！')
#     sys.exit()

if not os.path.exists(out_path):
    os.makedirs(out_path)


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


def parse_image(in_image_file, out_image_file):
    """
    删除图片exif信息
    """

    # -----删除exif信息-----
    image_file = open(in_image_file, 'rb')
    image = Image.open(image_file)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(out_image_file)


def resume():
    """删除最后处理的5个图片（按最修改时间排序）"""

    file_list = get_file_list(out_path, suffix)
    new_file_list = sorted(file_list, key=os.path.getmtime, reverse=True)
    i = 0
    for new_tar in new_file_list:
        if i >= 5:
            break
        print("mtime: %s  delete: %s" % (time.strftime("%Y-%m-%d %H:%M:%S",
                                                       time.localtime(os.path.getmtime(new_tar))
                                                       ), new_tar))
        os.remove(new_tar)
        i += 1


def analyse(in_reverse):
    """打印最大、最小的5个文件"""

    file_list = get_file_list(out_path, suffix)
    new_file_list = sorted(file_list, key=os.path.getsize, reverse=in_reverse)
    i = 0
    for new_tar in new_file_list:
        if i >= 5:
            break
        print("size(Kilobyte): %s" % (round(os.path.getsize(new_tar) / float(1024))))
        i += 1


def main():
    """主方法／main方法"""

    count = 0
    file_list = get_file_list(path, suffix)
    for tar in file_list:
        tar_name = os.path.basename(tar)
        tar_out = os.path.join(out_path, tar_name)
        # 跳过已有文件
        if os.path.exists(tar_out):
            continue

        count += 1
        print('%s  %s' % (count, tar_name))
        parse_image(tar, tar_out)  # 处理图片

    print('----------')
    print('总共处理了：%s' % (count))


print('max --> min')
analyse(in_reverse=True)
print('----------')
print('min --> max')
analyse(in_reverse=False)
print('----------')
resume()
print('----------')
main()
