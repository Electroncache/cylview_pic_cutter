## cylview_pic_cutter
#Cut cylview generated pictures to remove the white or black edges.

#使用方法

单张图片处理：
`python auto_crop.py --input input_file.png --output output_file.png`

批量处理文件夹：
`python auto_crop.py --input input_path --output output_path`

裁剪黑边而不是白边：
`python auto_crop.py --input input_path.png --black`

调整阈值（默认240）：
`python auto_crop.py --input input_path.png --threshold 220`
