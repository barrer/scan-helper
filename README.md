## 扫描图片处理脚本
### java version
扫描仪、ABBYY等的参数设置可以参考：http://www.cnblogs.com/whycnblogs/category/1036599.html
```
用途：
识别所有图片（不包含"cover"目录），找出最大"宽、高"，然后应用到所有图片
"PATH"目录中子目录"cover"放封面，不处理为黑白，但与黑白保持相同的宽高（IS_BLACK_WHITE控制正文是否转成黑白：true或false）
"OUT_DIR"目录为输出目录，包含了彩色封面和黑白正文
步骤：
1. 扫描图片
2. ABBYY - 编辑图像 2.1 歪斜校正 - (所有页面) - (歪斜校正) 2.2 等级 - (输入级别: 69 1.00 223) - (输出级别: 0 255) - (所有页面) - (应用)
3. 文件 - 将页面保存为图像 - (保存类型: jpeg 彩色)
4. 执行 CommandLine 去除exif并统一宽度等（见：用途）
5. Adobe Acrobat Pro DC - 创建PDF 5.1 工具 - 合并文件 - 添加文件 - 选项(文件大小: 默认大小, 其它选项: 取消所有勾选) - 合并
6. PDF阅读器 - 网格视图 - 检查每页图像
```

在com目录同一级
编译
```javac com/scan/CommandLine.java```
运行
```java com.scan.CommandLine```
### python version

注意：  
`【修改】`标注的参数根据本机实际情况修改  
`max_process=进程数` 一定要根据自己机器的内存情况量力而行，**切莫**设置过大导致系统卡死  
`imagemagick 6.9.9` 请安装此版本，7.x版本有bug已反馈给作者

脚本列表：

`scan_helper_jpg.py`  
```
# 作用：
# imagemagick处理图片（统一所有图片的宽高分辨率、调整亮度对比度）
# 多进程处理
```

`scan_helper_png.py`  
```
# 作用：
# imagemagick处理png为黑白（统一所有图片的宽高分辨率、调整亮度对比度、改为黑白图片）
# 多进程处理
# ==========
# 操作步骤：
# 扫描
# ABBYY歪斜矫正
# ABBYY另存“TIFF彩色LZW压缩”
# “scan_png_monochrome.py”生成“monochrome”目录下黑白png
# 用无损压缩软件（ImageOptim、limitPNG等）压缩“monochrome”目录下的黑白png（可选操作）
# 用Adobe Acrobat DC 合并png为单个pdf
```

`scan_helper_rename.py`  
```
# 作用：
# 批量重命名文件
```

## component
本目录下是一些常用的脚本：  
`remove_image_exif.py` 删除图片的exif信息
