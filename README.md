# cylview_pic_cutter
Cut cylview generated pictures to remove the white edges.

使用方法

自动裁剪白边或黑边

单张图片处理：
python auto_crop.py --input 图片路径.png --output 输出路径.png

批量处理文件夹：
python auto_crop.py --input 输入文件夹 --output 输出文件夹

裁剪黑边而不是白边：
python auto_crop.py --input 图片路径.png --black

调整阈值（默认240）：
python auto_crop.py --input 图片路径.png --threshold 220
