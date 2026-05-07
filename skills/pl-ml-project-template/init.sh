#!/usr/bin/env bash
echo "Creating project directory structure in current folder..."

# 创建目录
mkdir -p configs data/dataset model scripts train_log test_log figures

# 创建空文件
touch configs/default.yaml
touch configs/experiment1.yaml
touch configs/experiment2.yaml

touch data/__init__.py
touch data/data_interface.py
touch data/xxxdataset1.py
touch data/xxxdataset2.py

touch model/__init__.py
touch model/model_interface.py
touch model/xxxmodel1.py
touch model/xxxmodel2.py

touch scripts/train.sh
touch scripts/test.sh

touch utils.py
touch main.py
touch requirements.txt
touch README.md
touch .gitignore

echo
echo "Project structure created successfully!"
echo "Current directory: $(pwd)"
echo
echo "Next steps:"
echo "1. Edit requirements.txt to add your dependencies"
echo "2. Configure your .gitignore file"
echo "3. Start coding!"
