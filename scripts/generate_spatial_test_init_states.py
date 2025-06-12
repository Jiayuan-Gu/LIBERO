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
    save initial states to .pruned_init files
    """  

    os.makedirs(os.path.dirname(save_path), exist_ok=True)  
      

    torch.save(init_states, save_path)  
    print(f"save to: {save_path}")  
  
def generate_all_spatial_test_init_states():  

 
    bddl_base_path = get_libero_path("bddl_files")  
    init_states_base_path = get_libero_path("init_states")  
  
    all_tasks = [  
        # libero_spatial
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
          
        # added tasks
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
      

    target_init_states_dir = os.path.join(init_states_base_path, "libero_spatial_test")  
    os.makedirs(target_init_states_dir, exist_ok=True)  
      
    successful_tasks = 0  
    failed_tasks = []  
      
    for i, task_name in enumerate(all_tasks):  
        print(f"\nprocessing {i+1}/{len(all_tasks)}: {task_name}")  
          
 
        if i < 10: 
            bddl_file_path = os.path.join(bddl_base_path, "libero_spatial", f"{task_name}.bddl")  

            source_init_path = os.path.join(init_states_base_path, "libero_spatial", f"{task_name}.pruned_init")  
            target_init_path = os.path.join(target_init_states_dir, f"{task_name}.pruned_init")  
              
            if os.path.exists(source_init_path):  
                import shutil  
                shutil.copy2(source_init_path, target_init_path)  
                print(f"copied original tasks: {task_name}")  
                successful_tasks += 1  
                continue  
        else:  
            bddl_file_path = os.path.join(bddl_base_path, "libero_spatial_test", f"{task_name}.bddl")  
          

        if not os.path.exists(bddl_file_path):  
            print(f"error: no BDDL files: {bddl_file_path}")  
            failed_tasks.append(task_name)  
            continue  
          
        try:  
            # generate initial states
            init_states = generate_init_states_for_task(bddl_file_path, task_name, num_states=50)  
              
            if len(init_states) == 0:  
                print(f"error: cannot generate any initial states for {task_name}")  
                failed_tasks.append(task_name)  
                continue  
              
            # save initial states
            save_path = os.path.join(target_init_states_dir, f"{task_name}.pruned_init")  
            save_init_states(init_states, save_path)  
              
            successful_tasks += 1  
              
        except Exception as e:  
            failed_tasks.append(task_name)  
            continue  
      
 
    print(f"\n=== FINISH GENERATING ===")  
    print(f"success for: {successful_tasks}/{len(all_tasks)} tasks")  
    print(f"{len(failed_tasks)} tasks failed ")  
      
    if failed_tasks:  
        print("List of failed tasks:")  
        for task in failed_tasks:  
            print(f"  - {task}")  
      
    print(f"\nsave at: {target_init_states_dir}")  
  
def main():  

    print("state to generate for libero_spatial_test benchmark...")  
    generate_all_spatial_test_init_states()  
    print("FINISH")  
  
if __name__ == "__main__":  
    main()