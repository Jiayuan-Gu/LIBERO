import os
import re
import random
from pathlib import Path

try:
    from libero.libero import get_libero_path
except ImportError:
    print("警告：无法导入 libero。将假定 bddl_files 位于脚本当前目录的相对路径中。")
    print("如果脚本失败，请将此脚本放置在 libero 项目的根目录，或确保 libero 已安装。")
    # 提供一个备用函数
    def get_libero_path(subfolder):
        return Path(__file__).resolve().parent.parent / "libero" / subfolder

def perturb_bddl_suite(source_suite_name="libero_spatial", 
                         output_suite_name="libero_spatial_test", 
                         perturbation_strength=0.02):
    """
    读取指定libero套件中的所有BDDL文件，对其中的位置区域进行整体随机平移，
    并生成一个新的BDDL套件作为测试集。
    此版本确保了区域定义的有效性 (x_max >= x_min, y_max >= y_min)。

    Args:
        source_suite_name (str): 源BDDL套件的文件夹名称 (例如 'libero_spatial')。
        output_suite_name (str): 用于存放扰动后BDDL文件的文件夹名称。
        perturbation_strength (float): 扰动的最大幅度。区域将在x和y方向上
                                       在 [-strength, +strength] 范围内随机平移。
    """
    print("--- 开始生成扰动后的BDDL测试集 (V2 - 保证区域有效性) ---")
    
    # 1. 定位源文件和定义输出路径
    try:
        bddl_base_path = Path(get_libero_path("bddl_files"))
        source_dir = bddl_base_path / source_suite_name
        output_dir = bddl_base_path / output_suite_name
    except Exception as e:
        print(f"错误：无法获取libero路径。请确保libero库已正确安装。错误信息: {e}")
        return

    if not source_dir.is_dir():
        print(f"错误：找不到源文件夹 {source_dir}")
        print("请确认 'source_suite_name' 是否正确，以及libero数据集是否已下载。")
        return

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"源文件夹: {source_dir}")
    print(f"将生成测试集到: {output_dir}")
    print(f"平移扰动幅度: ±{perturbation_strength}")

    # 2. 定义用于匹配坐标的正则表达式
    coord_pattern = re.compile(
        r"\(\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s*\)"
    )

    # 3. 定义区域平移函数 (核心修改部分)
    def translate_region(match):
        """
        接收一个正则匹配对象，提取区域坐标，进行整体平移，
        并返回格式化后的新坐标字符串。
        """
        # 从匹配的组中提取出4个坐标值 (x_min, y_min, x_max, y_max)
        coords_str = match.groups()
        x_min, y_min, x_max, y_max = [float(c) for c in coords_str]
        
        # 生成x和y方向上的随机位移
        delta_x = random.uniform(-perturbation_strength, perturbation_strength)
        delta_y = random.uniform(-perturbation_strength, perturbation_strength)
        
        # 将位移应用到min和max坐标上，实现整体平移
        new_x_min = x_min + delta_x
        new_x_max = x_max + delta_x
        new_y_min = y_min + delta_y
        new_y_max = y_max + delta_y
            
        # 将扰动后的坐标格式化回字符串，保留4位小数
        new_coords_str = "({:.4f} {:.4f} {:.4f} {:.4f})".format(
            new_x_min, new_y_min, new_x_max, new_y_max
        )
        return new_coords_str

    # 4. 遍历源文件，执行扰动并保存
    source_files = list(source_dir.glob("*.bddl"))
    if not source_files:
        print(f"警告：在 {source_dir} 中没有找到任何 .bddl 文件。")
        return
        
    generated_count = 0
    for bddl_file_path in source_files:
        print(f"正在处理: {bddl_file_path.name}")
        
        # 读取原始BDDL内容
        original_content = bddl_file_path.read_text(encoding='utf-8')
        
        # 使用正则表达式和我们的平移函数来替换所有匹配的坐标区域
        perturbed_content = coord_pattern.sub(translate_region, original_content)
        
        # 定义新的文件名并保存
        output_file_path = output_dir / bddl_file_path.name
        output_file_path.write_text(perturbed_content, encoding='utf-8')
        generated_count += 1

    print("\n--- 操作完成 ---")
    print(f"成功生成了 {generated_count} 个扰动后的BDDL文件。")
    print(f"测试集已保存在: {output_dir}")

if __name__ == "__main__":
    perturb_bddl_suite(
        source_suite_name="libero_spatial",
        output_suite_name="libero_spatial_test",
        perturbation_strength=0.05
    )