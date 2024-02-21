# UAV Navigation Policy Training

This repository contains the code necessary for training a control policy for navigating a UAV (Unmanned Aerial Vehicle) in complex environments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a `Linux` or `Windows` machine.
- You have installed `Python 3`.

### Installation

Follow these steps to get your development environment set up:

1. **Install the Simplified UAV Simulator**

```bash
git clone [Simplified UAV Simulator Repository URL]
cd [Simplified UAV Simulator Directory]
pip3 install -e .
```

2. **Install Reinforcement Learning Repo**

```bash
git clone [Reinforcement Learning Repository URL]
cd [Reinforcement Learning Directory]
pip3 install -e .
```

3. **Training a Navigation Policy**

```bash
git clone [Navigation Policy Repository URL]
cd [Navigation Policy Directory]
```

### Training the Policy

To train a navigation policy in the simplified UAV environment using the PPO algorithm, follow these steps:

#### Sparse Reward Without Curriculum Learning

```bash
python3 train.py --use_sparse_reward
```

#### Reward Shaping Without Curriculum Learning

```bash
python3 train.py
```

#### Sparse Reward With Curriculum Learning

```bash
python3 train.py --use_sparse_reward --use_curriculum_learning
```

#### Reward Shaping With Curriculum Learning

```bash
python3 train.py --use_curriculum_learning
```

## Contributing

We welcome contributions. Please feel free to reach out if you have any suggestions, bug reports, or contributions. 

## License

This project is licensed under the [MIT License] - see the LICENSE.md file for details.
```

请记得替换`[Simplified UAV Simulator Repository URL]`, `[Simplified UAV Simulator Directory]`, `[Reinforcement Learning Repository URL]`, `[Reinforcement Learning Directory]`, 和 `[Navigation Policy Repository URL]`, `[Navigation Policy Directory]`为实际的URL和目录名称。

保存这段文本为`README.md`文件后，您的项目说明就已经准备好了。