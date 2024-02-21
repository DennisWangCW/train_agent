import gymnasium as gym
import gym_uav
import argparse
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv, VecMonitor
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.logger import configure
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback, EvalCallback

def add_arguments(parser):
    parser.add_argument('--use_sparse_reward', default=False, help="whether use sparse reward", action='store_true')
    parser.add_argument('--use_curriculum_learning', default=False, help="whether use curriculum learning", action='store_true')
    return parser

def make_env(env_id: str, rank: int, args: argparse.Namespace, seed: int = 0):
    """
    Utility function for multiprocessed env.

    :param env_id: the environment ID
    :param num_env: the number of environments you wish to have in subprocesses
    :param seed: the inital seed for RNG
    :param rank: index of the subprocess
    """
    def _init():
        env = gym.make(env_id) #, render_mode="human")
        env.reset(seed=seed + rank, options=args)
        return env
    set_random_seed(seed)
    return _init

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser = add_arguments(parser)
    args = parser.parse_args()
    env_id = "uav-v1"
    num_cpu = 32  # Number of processes to use
    # Create the vectorized environment
    seed = 2
    vec_env = VecMonitor(SubprocVecEnv([make_env(env_id, i, args=args, seed=seed) for i in range(num_cpu)])) 

    tmp_path = "./logs/"
    new_logger = configure(tmp_path, ["stdout", "csv", "tensorboard"])

    # Save a checkpoint every 1000 steps
    checkpoint_callback = CheckpointCallback(
        save_freq=5000,
        save_path=tmp_path,
        name_prefix="rl_model",
        save_replay_buffer=True,
        save_vecnormalize=True,
    )
        
    # Use deterministic actions for evaluation
    eval_env = VecMonitor(SubprocVecEnv([make_env(env_id, i, args=args, seed=seed+1000) for i in range(8)])) #, info_keywords=('total_rew', 'distance_rew','action_pen', 'obstacle_pen', 'step_pen', 'goal_rew'))

    eval_callback = EvalCallback(eval_env, 
                                best_model_save_path=tmp_path,
                                log_path=tmp_path, eval_freq=500,
                                n_eval_episodes = 100,
                                deterministic=False, render=False)

    # save the configuration and other files
    model = PPO(
        policy=MlpPolicy,  # check activation function
        policy_kwargs=dict(
            net_arch=[dict(pi=[128,256,256,128], vf=[128,256,256,128])]),
        env=vec_env,
        clip_range=0.1,
        gamma=0.99,
        n_steps=512, # 512
        ent_coef=0.00,#1,
         learning_rate=3e-4,
        vf_coef=1.0, # 0.5,
        max_grad_norm=0.5,
        batch_size=128, # 64
         verbose=1,
    )

    model.set_logger(new_logger)
    model.learn(total_timesteps=int(6000000), callback=eval_callback)
    model.save(tmp_path)
