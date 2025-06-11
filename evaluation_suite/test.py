from libero.libero import benchmark
from libero.libero.envs import OffScreenRenderEnv
from libero.libero import get_libero_path
import os

benchmark_dict = benchmark.get_benchmark_dict()
task_suite_name = "libero_spatial" # can also choose libero_spatial, libero_object, etc.
task_suite = benchmark_dict[task_suite_name]()

# retrieve a specific task
task_id = 0
task = task_suite.get_task(task_id)
task_name = task.name
task_description = task.language
task_bddl_file = os.path.join(get_libero_path("bddl_files"), task.problem_folder, task.bddl_file)
print(f"[info] retrieving task {task_id} from suite {task_suite_name}, the " + \
      f"language instruction is {task_description}, and the bddl file is {task_bddl_file}")

# step over the environment
env_args = {
    "bddl_file_name": task_bddl_file,
    "camera_heights": 128,
    "camera_widths": 128
}
env = OffScreenRenderEnv(**env_args)
env.seed(0)
env.reset()
init_states = task_suite.get_task_init_states(task_id) # for benchmarking purpose, we fix the a set of initial states
init_state_id = 0
env.set_init_state(init_states[init_state_id])

dummy_action = [0.] * 7
for step in range(10):
    obs, reward, done, info = env.step(dummy_action)
    import cv2
    import numpy as np
    cv2.imshow(
        "Observation",
        obs["agentview_image"].astype(np.uint8)[::-1]
    )
    cv2.waitKey(0)
env.close()