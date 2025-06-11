import requests
import time
import numpy as np
from collections import OrderedDict


class RemoteEnv:
    """
    A class to represent a remote environment for evaluation.
    This class is designed to interact with a remote server that provides an environment for evaluation tasks.
    """

    def __init__(self, server_ip, port, task_id, camera_width=128, camera_height=128):
        self.server_ip = server_ip
        self.port = port
        self.base_url = f"http://{self.server_ip}:{self.port}"
        self.session = requests.Session()
        
        self.task_id = task_id
        self.camera_width = camera_width
        self.camera_height = camera_height
        
        response = self.session.post(
            f"{self.base_url}/create",
            json={
                "task_id": self.task_id,
                "camera_width": self.camera_width,
                "camera_height": self.camera_height
            }
        )
        if response.status_code != 200:
            raise Exception(f"Failed to create session: {response.text}")
        self.session_id = response.json().get("session_id")
        self.session.headers.update({"Session-ID": self.session_id})

    def dejsonify_observation(self, obs: dict):
        ret = OrderedDict()
        for k, v in obs.items():
            ret[k] = np.array(v) if "image" in k else v
        return ret

    def reset(self):
        """
        Resets the remote environment and returns the initial observation.

        :return: The initial observation from the remote environment.
        """
        response = self.session.post(f"{self.base_url}/reset")
        if response.status_code == 200:
            observation = response.json().get("observation")
            if observation is None:
                raise Exception("Reset did not return an observation.")
            return self.dejsonify_observation(observation)
        else:
            raise Exception(f"Failed to reset environment: {response.text}")

    def step(self, action):
        """
        Takes a step in the remote environment with the given action.

        :param action: The action to be taken in the environment.
        :return: A tuple containing the observation, reward, done status, and additional info.
        """
        response = self.session.post(f"{self.base_url}/step", json={"action": action})
        if response.status_code == 200:
            data = response.json()
            return self.dejsonify_observation(data["observation"]), data["reward"], data["done"], data["info"]
        else:
            raise Exception(f"Failed to step in environment: {response.text}")

    def close(self):
        """
        Closes the session with the remote environment.
        This method should be called when the environment is no longer needed.
        """
        response = self.session.post(f"{self.base_url}/close")
        if response.status_code != 200:
            raise Exception(f"Failed to close session: {response.text}")
        self.session.close()
        self.session = None

    def __del__(self):
        """
        Destructor to ensure the session is closed when the object is deleted.
        """
        if self.session is not None:
            self.close()


def main():
    """
    Main function to demonstrate the usage of the RemoteEnv class.
    This function initializes a RemoteEnv instance and performs a reset and step operation.
    """
    from libero.libero.utils.video_utils import VideoWriter

    # video_writer = VideoWriter(
    #     video_path="videos",
    #     save_video=True,
    #     single_video=True,
    #     fps=30,
    # )

    remote_env = RemoteEnv(server_ip="127.0.0.1", port=5000, task_id=0)
    try:
        tic = time.time()
        initial_observation = remote_env.reset()
        toc = time.time()
        print("Reset Time:", toc - tic)
        # print("Initial Observation:", initial_observation)
        print(initial_observation["agentview_image"].shape)

        # video_writer.reset()

        import cv2
        # cv2.imshow(
        #     "Observation",
        #     initial_observation["agentview_image"].astype(np.uint8)[::-1]
        # )
        # cv2.waitKey(0)

        for _ in range(60):
            action = [0.0] * 7  # Example action
            tic = time.time()
            observation, reward, done, info = remote_env.step(action)
            toc = time.time()
            time.sleep(0.1)
            print("Step Time:", toc - tic)
            # print("Step Result:", observation, reward, done, info)

            if done:
                break
            # video_writer.append_obs(observation, done)

            cv2.imshow(
                "Observation",
                observation["agentview_image"].astype(np.uint8)[::-1]
            )
            cv2.waitKey(10)

    except Exception as e:
        # print("An error occurred:", e)
        raise e
    finally:
        remote_env.close()
        # video_writer.save()


if __name__ == "__main__":
    main()