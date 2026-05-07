---
name: auto-monitor
description: Background experiment monitor — generates native bash script, launches via Bash(run_in_background=True). Adaptive polling, keyword detection, stale/error/done states, zero main-thread context. Triggers on "monitor", "watch experiment", "后台监控", or after any long-running job.
argument-hint: [optional: duration=30m|2h|8h]
allowed-tools: Bash(*), Write
---

# Auto-Monitor Experiment

Generate and launch a **native bash monitoring script** in the background.

**Why native script, not a sub-agent?** Sub-agents (Agent tool) cannot maintain reliable long sleep loops — bash tool caps at 600s timeout per call, and agent turns are limited. A native script launched via `Bash(run_in_background=True)` runs as an OS process with no such constraints.

---

## Step 1: Extract Monitoring Context

Read the **current conversation**. Do NOT ask the user unless SSH info is completely absent and experiment is remote.

Extract these fields:

| Field | How to find | Example |
|-------|-------------|---------|
| `ssh_prefix` | Recent SSH commands in conversation | `ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -p 12345 root@server` or empty if local |
| `check_cmd` | 1–3 commands that reveal experiment state | `tail -20 /root/train.log` (will be prefixed with ssh_prefix if remote) |
| `done_pattern` | Infer from experiment type | See pattern design rules below |
| `error_pattern` | Infer from experiment type | See pattern design rules below |
| `expected_duration` | From $ARGUMENTS, or infer from epoch count × time per epoch | `30m`, `2h`, `8h` |

If remote: every check command must include the full SSH prefix with `-o ConnectTimeout=10 -o ServerAliveInterval=30`.

If local on Windows: use Git Bash compatible commands (`tail`, `grep` work in Git Bash).

### Pattern Design Rules (CRITICAL — avoid false positives)

**ERROR_PATTERN must be precise.** Training logs routinely contain words like `error` in metric names (`mean_squared_error`, `error_rate=0.05`, `bit_error_ratio`). A naive `error` pattern causes constant false alarms.

**Rules for building ERROR_PATTERN:**
1. NEVER use bare `error` — always use context-specific patterns
2. Use multi-word patterns that only appear in actual crashes:
   - `RuntimeError|Traceback|CUDA out of memory|KeyboardInterrupt`
   - `killed|OOM|Segmentation fault|SIGKILL|SIGTERM`
   - `nan loss|loss.*nan|NaN`
   - `FAILED|FATAL|Abort`
3. If the user's framework has custom error formats, add them (e.g., PyTorch Lightning's `Error` with capital E at line start)
4. Read 10 lines of the existing log (if available) to check for false-positive-prone words before finalizing the pattern

**Good example:** `'Traceback|RuntimeError|CUDA out of memory|killed|OOM|Segmentation fault|FATAL|loss.*nan|NaN'`
**Bad example:** `'error|fail|exception'` ← matches `error_rate`, `failover`, `exception_handler`

**DONE_PATTERN:** Less prone to false positives, but still be specific:
- `'Training finished|Training completed|training done|All experiments completed|Checkpoint.*final'`
- NOT bare `done` (matches `undone`, `done_count=5`)

### Adaptive Interval Calculation (CRITICAL — not a fixed schedule)

**DO NOT use a fixed interval profile.** Calculate intervals based on expected experiment duration.

**Formula:**
```
expected_minutes = parse duration (e.g., "2h" → 120, "30m" → 30, "8h" → 480)

interval_schedule:
  check 0:   0 seconds (immediate)
  check 1:   min(expected_minutes * 0.05, 5) minutes     ← ~5% of total, cap 5min
  check 2:   min(expected_minutes * 0.1, 10) minutes     ← ~10%
  check 3-5: min(expected_minutes * 0.15, 30) minutes    ← ~15%
  check 6+:  min(expected_minutes * 0.2, 60) minutes     ← ~20%, cap 1hr

max_checks = max(10, expected_minutes / interval_last * 1.5)
```

**Examples:**

| Expected duration | Check 0 | Check 1 | Check 2 | Check 3-5 | Check 6+ | Max checks |
|-------------------|---------|---------|---------|-----------|----------|------------|
| 30 min | 0 | 90s | 180s | 270s | 360s | 15 |
| 2 hours | 0 | 5min | 10min | 18min | 24min | 15 |
| 8 hours | 0 | 5min | 10min | 30min | 60min | 20 |
| 24 hours | 0 | 5min | 10min | 30min | 60min | 30 |

**If duration is unknown:** default to 2 hours. If the experiment mentions epoch count and time per epoch, calculate: `duration = epochs × time_per_epoch`.

---

## Step 2: Generate Monitoring Script

Build a complete bash script from the template below. Replace all `__PLACEHOLDER__` values.

**Portability rules:**
- Array last-element: use `${arr[$((${#arr[@]}-1))]}` NOT `${arr[-1]}` (bash 3.2 compat)
- Hash for stale detection: use `cksum` (POSIX) NOT `md5sum` (missing on macOS)
- Python command: try `python` first, then `python3` (Windows uses `python`)
- Temp dir: use `${TMPDIR:-/tmp}`
- Notification binary: search multiple platform-specific paths
- check_cmd MUST use `tail -N` (default N=20) to limit output size — never read full log

### Script Template

```bash
#!/usr/bin/env bash
# Auto-generated experiment monitor.
set -uo pipefail

# ══════════ CONFIG ══════════
MAX_CHECKS=__MAX_CHECKS__
DONE_PATTERN='__DONE_PATTERN__'
ERROR_PATTERN='__ERROR_PATTERN__'

# Adaptive intervals (seconds), calculated from expected duration.
INTERVALS=(__INTERVALS__)

get_interval() {
  local i=$1 len=${#INTERVALS[@]}
  if [ "$i" -ge "$len" ]; then
    echo "${INTERVALS[$((len-1))]}"
  else
    echo "${INTERVALS[$i]}"
  fi
}

# ══════════ CHECK FUNCTION ══════════
# MUST use tail -N to limit output size. Never read full log.
run_check() {
  __CHECK_COMMANDS__
}

# ══════════ NOTIFICATION ══════════
notify() {
  local title="$1" body="$2"
  local p
  for p in \
    "${HOME}/.claude/claude-notifications-go/claude-notifier" \
    "${USERPROFILE:-__NONE__}/.claude/claude-notifications-go/claude-notifier.exe" \
    "${APPDATA:-__NONE__}/claude-notifications-go/claude-notifier.exe"; do
    if [ -f "$p" ] && [ -x "$p" ] 2>/dev/null; then
      "$p" notify --title "$title" --body "$body" 2>/dev/null && return 0
    fi
  done
  return 1
}

# ══════════ STATE ══════════
prev_hash=""
stale_count=0
check_fail_count=0
check_count=0
start_time=$(date +%s)

# ══════════ MAIN LOOP ══════════
while [ "$check_count" -lt "$MAX_CHECKS" ]; do
  interval=$(get_interval "$check_count")
  [ "$interval" -gt 0 ] && sleep "$interval"

  output=$(run_check 2>&1)
  rc=$?

  if [ $rc -ne 0 ]; then
    check_fail_count=$((check_fail_count + 1))
    if [ $check_fail_count -ge 3 ]; then
      output="CHECK_CMD_FAILED: $check_fail_count consecutive failures (exit=$rc). Last: $output"
    else
      check_count=$((check_count + 1))
      continue
    fi
  else
    check_fail_count=0
  fi

  check_count=$((check_count + 1))
  elapsed=$(( ($(date +%s) - start_time) / 60 ))

  # ── Keyword analysis ──
  status="RUNNING"
  if echo "$output" | grep -qiE "$ERROR_PATTERN"; then
    status="ERROR"
  elif echo "$output" | grep -qiE "$DONE_PATTERN"; then
    status="FINISHED"
  fi

  # ── Stale detection ──
  cur_hash=$(echo "$output" | cksum | cut -d' ' -f1)
  if [ "$cur_hash" = "$prev_hash" ]; then
    stale_count=$((stale_count + 1))
    if [ "$stale_count" -ge 3 ] && [ "$status" = "RUNNING" ]; then
      status="STALE"
    fi
  else
    stale_count=0
  fi
  prev_hash="$cur_hash"

  # ── Terminal state ──
  if [ "$status" != "RUNNING" ]; then
    notify "Experiment $status" "checks=$check_count elapsed=${elapsed}min" || true
    echo ""
    echo "========================================"
    echo "MONITOR_DONE: $status"
    echo "Checks: $check_count | Elapsed: ~${elapsed} min"
    echo "========================================"
    echo "$output" | tail -30
    echo "========================================"
    exit 0
  fi
done

elapsed=$(( ($(date +%s) - start_time) / 60 ))
notify "Monitor TIMEOUT" "Max $MAX_CHECKS checks in ${elapsed}min" || true
echo ""
echo "========================================"
echo "MONITOR_DONE: TIMEOUT"
echo "Checks: $MAX_CHECKS | Elapsed: ~${elapsed} min"
echo "========================================"
echo "$output" | tail -30
echo "========================================"
```

### Optional: API analysis mode

If `MONITOR_API_KEY` env var is set, replace the keyword analysis block with an API call. This is for cases where keyword matching is insufficient (complex log formats, ambiguous output).

The API receives only the last 20 lines (from `tail -20`), not the full log. Token cost per check is negligible (~100 tokens).

```bash
  # ── API analysis (replaces keyword block) ──
  PYTHON_CMD=$(command -v python 2>/dev/null || command -v python3 2>/dev/null || echo python)
  api_status=$("$PYTHON_CMD" -c "
import requests, os, sys
try:
    r = requests.post(
        os.environ.get('MONITOR_API_BASE', 'https://api.deepseek.com/v1') + '/chat/completions',
        headers={'Authorization': 'Bearer ' + os.environ['MONITOR_API_KEY'],
                 'Content-Type': 'application/json'},
        json={'model': os.environ.get('MONITOR_MODEL', 'deepseek-chat'),
              'messages': [{'role':'user',
                            'content': 'Analyze experiment log. Reply ONE word only: RUNNING or FINISHED or ERROR\n\n' + sys.stdin.read()}],
              'max_tokens': 10},
        timeout=30)
    w = r.json()['choices'][0]['message']['content'].strip().split()[0].upper()
    print(w if w in ('RUNNING','FINISHED','ERROR') else 'RUNNING')
except Exception:
    print('RUNNING')
" <<< "$output" 2>/dev/null)
  status="${api_status:-RUNNING}"
```

---

## Step 3: Write Script and Launch

1. Determine a temp path:
```bash
echo "${TMPDIR:-/tmp}/auto_monitor_$(date +%s).sh"
```

2. Write the generated script using the Write tool.

3. (Optional) Validate before launch:
```bash
bash scripts/validate.sh /path/to/script.sh
```

4. Launch in background:
```
Bash(command="chmod +x /path/to/script.sh && bash /path/to/script.sh", run_in_background=True)
```

Claude Code will automatically notify the main thread when the script exits.

---

## Step 4: Confirm to User

```
后台监控已启动。
- 预估时长：{expected_duration}
- 轮询间隔：立即 → {interval_1} → {interval_2} → ... → {interval_max}（基于预估时长自适应）
- 分析方式：关键词匹配（精确模式，避免 error_rate 等假阳性）
- 上限：{max_checks} 次检查
- 脚本：{script_path}

实验完成/出错/停滞时自动通知。
```

---

## Rules

- **Infer, don't ask** — extract SSH, log paths, conditions from conversation context
- **Immediate first check** — INTERVALS[0]=0, catches startup failures instantly
- **Native script only** — NEVER use Agent tool for the monitoring loop
- **Precise patterns** — NEVER use bare `error`/`fail`/`done`; always use multi-word or context-specific patterns
- **Limit log reading** — check_cmd MUST use `tail -N` (N=20 default), never read full log
- **Adaptive intervals** — calculate from expected duration, not fixed profiles
- **SSH resilience** — always add `-o ConnectTimeout=10 -o ServerAliveInterval=30`
- **Check failure tolerance** — 1-2 consecutive failures: skip and retry; 3+: report ERROR
- **Cross-platform** — use POSIX-compatible commands (cksum, not md5sum)
- **One monitor per invocation** — multiple experiments need separate calls
- **Safety limit** — script always exits (max_checks enforced)
