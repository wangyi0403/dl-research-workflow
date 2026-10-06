# GPU Environment Setup Checklist

For remote GPU server setup via SSH. Follow order; verify each step before proceeding.

## Phase 1: Connection

```bash
# 1. Verify the host key, then verify SSH connectivity
ssh -p PORT user@host "hostname && nvidia-smi"

# 2. Check GPU availability
ssh -p PORT user@host "nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv"
```

**Red flags**: No GPU visible, GPU memory < required, other users' processes consuming >80% VRAM.

## Phase 2: Environment

```bash
# 3. Check Python version
ssh -p PORT user@host "python --version && which python"

# 4. Create conda env (or use existing)
ssh -p PORT user@host "conda create -n exp_env python=3.10 -y"

# 5. Configure pip mirror (for speed in China)
ssh -p PORT user@host "pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"

# 6. Install PyTorch (match CUDA version from nvidia-smi)
# CUDA 12.1:
ssh -p PORT user@host "conda run -n exp_env pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121"
# CUDA 11.8:
ssh -p PORT user@host "conda run -n exp_env pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"

# 7. Install project dependencies
ssh -p PORT user@host "conda run -n exp_env pip install -r requirements.txt"
```

## Phase 3: Code Sync

```bash
# 8. Sync code (exclude large files)
rsync -avz --exclude 'data/' --exclude '*.pth' --exclude '*.ckpt' \
      --exclude '__pycache__' --exclude '.git' \
      -e "ssh -p PORT" ./ user@host:/path/to/project/

# 9. Sync data separately
rsync -avz -e "ssh -p PORT" ./data/ user@host:/path/to/project/data/
```

## Phase 4: Verification

```bash
# 10. Run minimal test
ssh -p PORT user@host "cd /path/to/project && conda run -n exp_env python -c '
import torch
print(f\"CUDA available: {torch.cuda.is_available()}\")
print(f\"GPU count: {torch.cuda.device_count()}\")
print(f\"GPU name: {torch.cuda.get_device_name(0)}\")
print(f\"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\")
x = torch.randn(100, 100).cuda()
y = x @ x.T
print(f\"Test op OK: {y.shape}\")
'"

# 11. Run a single training step
ssh -p PORT user@host "cd /path/to/project && conda run -n exp_env python train.py --epochs 1 --steps 10"
```

## Phase 5: Launch Experiment

```bash
# 12. Start in screen/tmux (persist after SSH disconnect)
ssh -p PORT user@host "cd /path/to/project && screen -dmS exp_main conda run -n exp_env python train.py"

# 13. Verify process started
ssh -p PORT user@host "screen -ls && nvidia-smi"

# 14. Tail log
ssh -p PORT user@host "tail -f /path/to/project/logs/train.log"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `conda: command not found` | `source ~/miniconda3/etc/profile.d/conda.sh` or use absolute path |
| `pip install` timeout | Use mirror (step 5) or `--default-timeout=100` |
| `CUDA_HOME` not set | `export CUDA_HOME=/usr/local/cuda` |
| `libcudnn.so` not found | `export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH` |
| SSH drops on long idle | Add `ServerAliveInterval 60` to `~/.ssh/config` |
| Disk space full | Check `df -h`; clean pip cache (`pip cache purge`) |

## Minimal Acceptable Test

Before leaving experiment unattended, verify:
- [ ] One full epoch completes without error
- [ ] Loss is decreasing (not NaN, not constant)
- [ ] GPU utilization > 80% (check with `nvidia-smi`)
- [ ] Log file is being written
- [ ] screen/tmux session is detached (not killed on SSH disconnect)
