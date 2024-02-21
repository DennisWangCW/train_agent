import numpy as np 
import matplotlib.pyplot as plt 
import os
from matplotlib.ticker import ScalarFormatter

def load_data(paths, key, scale=1):
    paths = paths * 3
    paths = [os.path.join(paths[i], 'logs' + str(i+1)) for i in range(len(paths))]
    datas = []
    for path in paths:
        data_file = os.path.join(path, "evaluations.npz")
        data = np.mean(np.load(data_file)[key] / scale, axis=-1)
        datas.append(np.expand_dims(data,1))
    datas = np.concatenate(datas, axis=-1)
    datas_mean = np.mean(datas, axis=-1)
    datas_std = np.std(datas, axis=-1)
    
    return datas_mean, datas_std


if __name__ == "__main__":

    data_paths = ["../sparse"]
    original_mean, original_std = load_data(data_paths, key="success_rate")

    data_paths = ["../shaping"]
    shaping_mean, shaping_std = load_data(data_paths, key="successes")

    data_paths = ["../curriculum"]
    curriculum_mean, curriculum_std = load_data(data_paths, key="successes")

    data_paths = ["../shaping_curriculum"]
    shaping_curriculum_mean, shaping_curriculum_std = load_data(data_paths, key="success_rate")

    steps = np.linspace(0, 6000000, len(shaping_mean))

    plt.plot(steps, original_mean, linewidth=2.5, label='SparseReward')
    plt.fill_between(steps, original_mean - original_std, original_mean + original_std, alpha=0.2)#, label='Variance')

    plt.plot(steps, shaping_mean, linewidth=2.5, label="RewardShaping")
    plt.fill_between(steps, shaping_mean - shaping_std, shaping_mean + shaping_std, alpha=0.2)

    plt.plot(steps, curriculum_mean, linewidth=2.5, label='Curriculum')
    plt.fill_between(steps, curriculum_mean - curriculum_std, curriculum_mean + curriculum_std, alpha=0.2)
    plt.axvline(x=2.3e6, color='r', linestyle='--', label='课程学习截止点')

    plt.plot(steps, shaping_curriculum_mean, linewidth=2.5, label='课程学习+奖励塑形')
    plt.fill_between(steps, shaping_curriculum_mean - shaping_curriculum_std, shaping_curriculum_mean + shaping_curriculum_std, alpha=0.2)
    plt.axvline(x=2.3e6, color='r', linestyle='--', label='课程学习截止点')

    ax = plt.gca()
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.xaxis.get_major_formatter().set_powerlimits((0, 0))
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.xlabel('Training Steps', fontsize=14)
    plt.ylabel('Success Rates', fontsize=14)

    plt.legend(fontsize=14)

    plt.show()


    # ##############################################

    # data_paths = ["../shaping"]
    # obstacle_mean, obstacle_std = load_data(data_paths, key="obstacle_penalties", scale=50)
    # crash_mean, crash_std = load_data(data_paths, key="crash_penalties", scale=50)
    # distance_mean, distance_std = load_data(data_paths, key="distance_rewards", scale=50)
    # goal_mean, goal_std = load_data(data_paths, key="goal_rewards", scale=50)
    # total_mean, total_std = load_data(data_paths, key="total_rewards", scale=50)


    # plt.plot(steps, obstacle_mean, label=r'$\mathbb{E}[\sum{r_{obstacle}}]$')
    # plt.fill_between(steps, obstacle_mean - obstacle_std, obstacle_mean + obstacle_std, alpha=0.2)#, label='Variance')

    # plt.plot(steps, crash_mean, label=r'$\mathbb{E}[\sum{r_{crash}}]$')
    # plt.fill_between(steps, crash_mean - crash_std, crash_mean + crash_std, alpha=0.2)

    # plt.plot(steps, distance_mean, label=r'$\mathbb{E}[\sum{r_{target}}]$')
    # plt.fill_between(steps, distance_mean - distance_std, distance_mean + distance_std, alpha=0.2)

    # plt.plot(steps, goal_mean, label=r'$\mathbb{E}[\sum{r_{goal}}]$')
    # plt.fill_between(steps, goal_mean - goal_std, goal_mean + goal_std, alpha=0.2)

    # plt.plot(steps, total_mean, label=r'$\mathbb{E}[\sum{r}]$')
    # plt.fill_between(steps, total_std - goal_std, total_mean + total_std, alpha=0.2)

    # plt.title('不同成分累积奖励的期望值变化曲线')
    # plt.xlabel('训练步数')
    # plt.ylabel('奖励期望')

    # # 添加图例
    # plt.legend()

    # # 显示图形
    # plt.show()



