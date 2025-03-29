from PIL import Image
import numpy as np
import os

def auto_crop(image_path, output_path=None, threshold=240, is_black_border=False):
    """
    自动裁剪图片的白边或黑边
    
    参数:
    image_path: 输入图片路径
    output_path: 输出图片路径，如果为None则生成新的文件名
    threshold: 像素值阈值，大于此值被视为白色（或小于此值被视为黑色）
    is_black_border: 是否裁剪黑边（True）或白边（False）
    
    返回:
    裁剪后的图片对象
    """
    # 打开图片
    img = Image.open(image_path)
    
    # 转换为numpy数组进行处理
    img_array = np.array(img)
    
    # 如果是RGBA图像，只处理RGB部分
    if len(img_array.shape) == 3 and img_array.shape[2] >= 3:
        rgb_array = img_array[:,:,:3]
    else:
        # 处理灰度图像
        rgb_array = img_array
        if len(rgb_array.shape) == 2:
            rgb_array = np.expand_dims(rgb_array, axis=2)
    
    # 计算每个像素的平均值
    if rgb_array.shape[2] == 1:
        gray_array = rgb_array[:,:,0]
    else:
        gray_array = np.mean(rgb_array, axis=2)
    
    # 根据是裁剪黑边还是白边，调整mask计算方式
    if is_black_border:
        mask = gray_array < threshold  # 黑边
    else:
        mask = gray_array > threshold  # 白边
    
    # 找到非边界的行和列
    mask_i = np.any(~mask, axis=1)
    mask_j = np.any(~mask, axis=0)
    
    # 计算裁剪区域
    crop_i = np.where(mask_i)[0]
    crop_j = np.where(mask_j)[0]
    
    if len(crop_i) == 0 or len(crop_j) == 0:
        print(f"警告: 未检测到有效内容，返回原图")
        if output_path is None:
            base_name, ext = os.path.splitext(image_path)
            output_path = f"{base_name}_cropped{ext}"
        img.save(output_path)
        return img
    
    # 获取裁剪区域的边界
    i_min, i_max = crop_i[0], crop_i[-1]
    j_min, j_max = crop_j[0], crop_j[-1]
    
    # 裁剪图片
    cropped_img = img.crop((j_min, i_min, j_max + 1, i_max + 1))
    
    # 保存图片
    if output_path is None:
        base_name, ext = os.path.splitext(image_path)
        output_path = f"{base_name}_cropped{ext}"
    
    cropped_img.save(output_path)
    print(f"已保存裁剪后的图片至: {output_path}")
    
    return cropped_img

def batch_process(folder_path, output_folder=None, threshold=240, is_black_border=False):
    """
    批量处理文件夹中的图片
    
    参数:
    folder_path: 输入图片文件夹路径
    output_folder: 输出图片文件夹路径
    threshold: 像素值阈值
    is_black_border: 是否裁剪黑边（True）或白边（False）
    """
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在!")
        return
    
    if output_folder is None:
        output_folder = os.path.join(folder_path, "cropped")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 支持的图片格式
    img_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    # 遍历文件夹中的图片
    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        if ext in img_extensions:
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_cropped" + ext)
            
            try:
                print(f"处理图片: {filename}")
                auto_crop(input_path, output_path, threshold, is_black_border)
            except Exception as e:
                print(f"处理图片 {filename} 时发生错误: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='自动裁剪图片的白边或黑边')
    parser.add_argument('--input', required=True, help='输入图片或文件夹路径')
    parser.add_argument('--output', default=None, help='输出图片或文件夹路径')
    parser.add_argument('--threshold', type=int, default=240, help='像素阈值 (0-255)')
    parser.add_argument('--black', action='store_true', help='裁剪黑边而不是白边')
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        batch_process(args.input, args.output, args.threshold, args.black)
    else:
        auto_crop(args.input, args.output, args.threshold, args.black)
