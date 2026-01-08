#!/bin/bash
# Test 1: Monitor Output Realtime
SESSION="swarm_docs_1767874362"
LOG="docs/tests/hardtest_logs/test1_realtime.log"

echo "=== TEST 1: Output Realtime Base ===" > "$LOG"
echo "Start: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
echo "" >> "$LOG"

for i in {1..90}; do
  echo "=== Check $i/90 ($(date '+%H:%M:%S')) ===" >> "$LOG"
  tmux capture-pane -t "$SESSION" -p | tail -5 >> "$LOG"
  echo "" >> "$LOG"
  sleep 2
done

echo "=== END ===" >> "$LOG"
echo "End: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG"
