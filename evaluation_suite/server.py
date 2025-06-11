import os
from typing import Dict
from collections import OrderedDict
import numpy as np
from flask import Flask, jsonify, request

from libero.libero import get_libero_path
from libero.libero.benchmark import Benchmark, get_benchmark
from libero.libero.envs import OffScreenRenderEnv

app = Flask(__name__)


class Session:
    def __init__(self, benchmark: Benchmark, task_id: int, env_kwargs: dict):
        self.benchmark = benchmark
        self.task_id = task_id
        self.env_kwargs = env_kwargs

        self.env = OffScreenRenderEnv(**env_kwargs)

sessions: Dict[str, Session] = {}


def jsonify_observation(obs):
    res = OrderedDict()
    for k, v in obs.items():
        if isinstance(v, np.ndarray):
            res[k] = v.tolist() if v.ndim > 0 else v.item()
        elif isinstance(obs, np.bool_):
            res[k] = bool(v)
        else:
            res[k] = v
    return res


@app.route('/create', methods=['POST'])
def create_session():
    client_ip = request.remote_addr
    session_id = client_ip
    if session_id in sessions:
        return jsonify({"error": "Session already exists for this IP"}), 400
    
    data = request.json

    # Parse the request data
    benchmark_name = data.get('benchmark_name', "libero_spatial")
    if benchmark_name not in ["libero_spatial"]:
        return jsonify({"error": "Unsupported benchmark"}), 400
    task_id = data.get('task_id')
    if task_id is None:
        return jsonify({"error": "task_id is required"}), 400
    camera_width = data.get('camera_width', 128)
    camera_height = data.get('camera_height', 128)
    if camera_width > 512 or camera_height > 512:
        return jsonify({"error": "camera_width and camera_height must be <= 512"}), 400
    
    benchmark: Benchmark = get_benchmark(benchmark_name)()
    task = benchmark.get_task(task_id) 

    # Prepare environment arguments
    task_bddl_file = os.path.join(get_libero_path("bddl_files"), task.problem_folder, task.bddl_file)
    env_args = {
        "bddl_file_name": task_bddl_file,
        "camera_heights": camera_height,
        "camera_widths": camera_width,
    }
    
    sessions[session_id] = Session(benchmark, task_id, env_args)
    
    print(f"Session created for {client_ip} with session ID {session_id}")
    return jsonify({"session_id": session_id, "task_name": task.name}), 200


@app.route('/close', methods=['POST'])
def close_session():
    session_id = request.headers.get('Session-ID')
    if session_id and session_id in sessions:
        session = sessions.pop(session_id)
        session.env.close()
        print(f"Session {session_id} closed")
        return jsonify({"message": "Session closed"}), 200
    else:
        return jsonify({"error": "Session not found"}), 404

    
@app.route('/reset', methods=['POST'])
def reset():
    session_id = request.headers.get('Session-ID')
    if session_id and session_id in sessions:
        session = sessions[session_id]
    else:
        return  jsonify({"error": "Session not found"}), 404
    
    benchmark = session.benchmark
    task_id = session.task_id
    task = benchmark.get_task(task_id)
    env = session.env

    env.reset()
    # TODO: make sure how the seed should be set
    env.seed(0)

    init_states = benchmark.get_task_init_states(task_id)
    print(init_states.shape)
    obs = env.set_init_state(init_states[0])
    description = task.language

    return jsonify({
        "observation": jsonify_observation(obs),
        "description": description,
    })

@app.route('/step', methods=['POST'])
def step():
    session_id = request.headers.get('Session-ID')
    if session_id and session_id in sessions:
        session = sessions[session_id]
    else:
        return jsonify({"error": "Session not found"}), 404
    
    env = session.env
    
    data = request.json
    action = data.get('action')
    if action is None:
        return jsonify({"error": "action is required"}), 400
    
    if not isinstance(action, (list, np.ndarray)):
        return jsonify({"error": "action must be a list or numpy array"}), 400
    action = np.array(action)
    if action.ndim != 1 or action.shape[0] != 7:
        return jsonify({"error": "action must be a 1D array of shape (7,)"}), 400

    observation, reward, done, info = env.step(action)

    observation = jsonify_observation(observation)
    reward = float(reward)
    done = bool(done)
    if isinstance(info, dict):
        info = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in info.items()}
    
    return jsonify({
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": info
    })
    

if __name__ == '__main__':
    app.run()