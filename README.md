## 扫描图片处理脚本
注意：  
`【修改】`标注的参数根据本机实际情况修改  
`max_process=进程数` 一定要根据自己机器的内存情况量力而行，**切莫**设置过大导致系统卡死  
`imagemagick 6.9.9` 请安装此版本，7.x版本有bug已反馈给作者

扫描仪、ABBYY等的参数设置可以参考：http://www.cnblogs.com/whycnblogs/category/1036599.html

脚本列表：

`scan_helper_jpg.py`  
```
# 作用：
# 删除图片exif信息
# imagemagick处理图片
# 多进程处理
```

`scan_helper_png.py`  
```
# 作用：
# 删除图片exif信息
# imagemagick处理png为黑白
# 多进程处理
# ==========
# 操作步骤：
# 扫描
# ABBYY歪斜矫正
# ABBYY另存“JPEG彩色”
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