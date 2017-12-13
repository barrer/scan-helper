# -*- coding: utf-8 -*-
# version: python 3
# ==========
# 作用：
# imagemagick处理图片（缩放）
# 多进程处理
# ==========
# 依赖项：
# https://github.com/ImageMagick/ImageMagick/issues/594
# brew install imagemagick@6
# ==========
import sys, os, time

from multiprocessing import Process, Queue

path = '/Users/osx/Desktop/test'  # 处理目录【修改】
suffix = 'tif'  # "处理目录"中的指定图片后缀【修改】
convert = '/usr/local/opt/imagemagick@6/bin/convert'  # imagemagick路径【修改】
# 最大进程数（同时处理图片个数）【修改】
max_process = 20

out_path = os.path.join(path, 'out')  # 输出目录

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
    imagemagick处理图片
    """

    # -----命令行处理图片-----

    colorspace = ' -colorspace %(value)s' % {'value': 'Gray'}  # Gray/RGB
    if True:  # 禁用灰度设置
        colorspace = ''

    depth = ' -depth 8'  # https://en.wikipedia.org/wiki/Color_depth
    if True:  # 禁用色彩深度
        depth = ''

    monochrome = ' -monochrome'  # https://en.wikipedia.org/wiki/Thresholding_(image_processing)

    out_image_file_jpg = '%s.png' % os.path.splitext(out_image_file)[0]

    in_image = ' "%s"' % in_image_file
    out_image = ' "%s"' % out_image_file_jpg
    shell = ('%(convert)s'
             '%(colorspace)s'
             '%(depth)s'
             '%(monochrome)s'
             '%(in_image)s%(out_image)s'
             % {'convert': convert,
                'colorspace': colorspace,
                'depth': depth,
                'monochrome': monochrome,
                'in_image': in_image, 'out_image': out_image})  # 覆盖图片

    # print(shell)
    os.system(shell)


def loop(queue, count, id):
    """进程执行方法体"""

    while not count.full():
        tar = queue.get()
        tar_name = os.path.basename(tar)
        tar_out = os.path.join(out_path, tar_name)
        # print(tar)
        parse_image(tar, tar_out)
        count.put(0)
        time.sleep(1)


def monitor(process_list, count):
    """停止监控进程"""

    while True:
        print('monitor %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if count.full():
            for process in process_list:
                process.terminate()
            print('停止 %s 个进程' % len(process_list))
            break
        time.sleep(5)


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
    tar_count = len(file_list)

    # 阻塞队列（控制进程数）
    queue_job = Queue(maxsize=max_process)  # 任务队列
    queue_count = Queue(maxsize=tar_count)  # 记录处理的个数
    process_list = []  # 进程实例

    # 启动处理进程
    for id in range(max_process):
        process_parse = Process(target=loop, args=(queue_job, queue_count, id), name=id)
        process_parse.start()
        # process_parse.join()
        process_list.append(process_parse)

    # 启动停止监控进程
    Process(target=monitor, args=(process_list, queue_count)).start()

    for tar in file_list:
        tar_name = os.path.basename(tar)
        count += 1
        print('%s  %s' % (count, tar_name))
        queue_job.put(tar)

    print('----------')
    print('总共处理了：%s' % (count))


print('max --> min')
analyse(in_reverse=True)
print('----------')
print('min --> max')
analyse(in_reverse=False)
print('----------')
main()
