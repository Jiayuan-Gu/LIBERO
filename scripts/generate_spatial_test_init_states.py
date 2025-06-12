"""  
为libero_spatial_test benchmark生成初始状态文件(.pruned_init)  
"""  
import os  
import torch  
import numpy as np  
from libero.libero.envs import OffScreenRenderEnv  
from libero.libero import get_libero_path  
  
def generate_init_states_for_task(bddl_file_path, task_name, num_states=50):  
      
    env_args = {  
        "bddl_file_name": bddl_file_path,  
        "camera_heights": 256,  
        "camera_widths": 256,  
        "has_renderer": False,  
        "has_offscreen_renderer": True,  
    }  
      
    env = OffScreenRenderEnv(**env_args)  
      
    init_states = []  
    successful_resets = 0  
    max_attempts = num_states * 3 
      
    for attempt in range(max_attempts):  
        try:  
 
            obs = env.reset()  
              

            state_flattened = env.get_sim_state()  
            init_states.append(state_flattened)  
            successful_resets += 1  
              
            if successful_resets >= num_states:  
                break  
                  
        except Exception as e:  
            print(f"failed to reset (try {attempt + 1}): {e}")  
            continue  
      
    env.close()  
      
    if successful_resets < num_states:  
        print(f"warning: only generated {successful_resets}/{num_states} initial states")  
      
    return init_states  
  
def save_init_states(init_states, save_path):  
    """  
    保存初始状态到.pruned_init文件  
      
    Args:  
        init_states: 初始状态列表  
        save_path: 保存路径  
    """  
    # 确保目录存在  
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  
      
    # 使用torch.save保存，这是LIBERO的标准格式  
    torch.save(init_states, save_path)  
    print(f"初始状态已保存到: {save_path}")  
  
def generate_all_spatial_test_init_states():  
    """  
    为所有libero_spatial_test任务生成初始状态文件  
    """  
    # 获取路径  
    bddl_base_path = get_libero_path("bddl_files")  
    init_states_base_path = get_libero_path("init_states")  
      
    # 定义所有任务（原有10个 + 新增10个）  
    all_tasks = [  
        # 原有的10个libero_spatial任务  
        "pick_up_the_black_bowl_between_the_plate_and_the_ramekin_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_next_to_the_ramekin_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_from_table_center_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_on_the_cookie_box_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_in_the_top_drawer_of_the_wooden_cabinet_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_on_the_ramekin_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_next_to_the_cookie_box_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_on_the_stove_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_next_to_the_plate_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_on_the_wooden_cabinet_and_place_it_on_the_plate",  
          
        # 新增的10个任务  
        "pick_up_the_black_bowl_from_left_corner_and_place_it_on_the_right_plate",  
        "pick_up_the_black_bowl_behind_the_ramekin_and_place_it_on_the_front_plate",  
        "pick_up_the_black_bowl_from_far_left_and_place_it_on_the_center_plate",  
        "pick_up_the_black_bowl_near_the_cabinet_edge_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_from_table_corner_and_place_it_on_the_opposite_plate",  
        "pick_up_the_black_bowl_beside_the_wooden_cabinet_and_place_it_on_the_plate",  
        "pick_up_the_black_bowl_from_right_side_and_place_it_on_the_left_plate",  
        "pick_up_the_black_bowl_in_front_of_ramekin_and_place_it_on_the_back_plate",  
        "pick_up_the_black_bowl_from_near_edge_and_place_it_on_the_central_plate",  
        "pick_up_the_black_bowl_adjacent_to_cabinet_and_place_it_on_the_distant_plate",  
    ]  
      
    # 创建目标目录  
    target_init_states_dir = os.path.join(init_states_base_path, "libero_spatial_test")  
    os.makedirs(target_init_states_dir, exist_ok=True)  
      
    successful_tasks = 0  
    failed_tasks = []  
      
    for i, task_name in enumerate(all_tasks):  
        print(f"\n处理任务 {i+1}/{len(all_tasks)}: {task_name}")  
          
        # 构建BDDL文件路径  
        if i < 10:  # 原有任务，从libero_spatial复制  
            bddl_file_path = os.path.join(bddl_base_path, "libero_spatial", f"{task_name}.bddl")  
            # 对于原有任务，直接复制现有的init文件  
            source_init_path = os.path.join(init_states_base_path, "libero_spatial", f"{task_name}.pruned_init")  
            target_init_path = os.path.join(target_init_states_dir, f"{task_name}.pruned_init")  
              
            if os.path.exists(source_init_path):  
                import shutil  
                shutil.copy2(source_init_path, target_init_path)  
                print(f"已复制现有初始状态文件: {task_name}")  
                successful_tasks += 1  
                continue  
        else:  # 新任务，需要生成  
            bddl_file_path = os.path.join(bddl_base_path, "libero_spatial_test", f"{task_name}.bddl")  
          
        # 检查BDDL文件是否存在  
        if not os.path.exists(bddl_file_path):  
            print(f"错误: BDDL文件不存在: {bddl_file_path}")  
            failed_tasks.append(task_name)  
            continue  
          
        try:  
            # 生成初始状态  
            init_states = generate_init_states_for_task(bddl_file_path, task_name, num_states=50)  
              
            if len(init_states) == 0:  
                print(f"错误: 无法为任务 {task_name} 生成任何初始状态")  
                failed_tasks.append(task_name)  
                continue  
              
            # 保存初始状态  
            save_path = os.path.join(target_init_states_dir, f"{task_name}.pruned_init")  
            save_init_states(init_states, save_path)  
              
            successful_tasks += 1  
              
        except Exception as e:  
            print(f"错误: 处理任务 {task_name} 时出现异常: {e}")  
            failed_tasks.append(task_name)  
            continue  
      
    # 输出总结  
    print(f"\n=== 生成完成 ===")  
    print(f"成功处理: {successful_tasks}/{len(all_tasks)} 个任务")  
    print(f"失败任务: {len(failed_tasks)} 个")  
      
    if failed_tasks:  
        print("失败的任务列表:")  
        for task in failed_tasks:  
            print(f"  - {task}")  
      
    print(f"\n初始状态文件保存在: {target_init_states_dir}")  
  
def main():  
    """主函数"""  
    print("开始为libero_spatial_test benchmark生成初始状态文件...")  
    generate_all_spatial_test_init_states()  
    print("初始状态文件生成完成!")  
  
if __name__ == "__main__":  
    main()