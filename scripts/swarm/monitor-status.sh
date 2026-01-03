#!/bin/bash
# Regina monitora stato tasks

TASKS_DIR=".swarm/tasks"

echo "=== STATO TASKS ==="
echo ""

for task_md in $TASKS_DIR/TASK_*.md; do
  [ -f "$task_md" ] || continue

  TASK_ID=$(basename "$task_md" .md)

  if [ -f "$TASKS_DIR/$TASK_ID.done" ]; then
    STATUS="✅ DONE"
  elif [ -f "$TASKS_DIR/$TASK_ID.error" ]; then
    STATUS="❌ ERROR"
  elif [ -f "$TASKS_DIR/$TASK_ID.working" ]; then
    STATUS="🔄 WORKING"
  elif [ -f "$TASKS_DIR/$TASK_ID.ready" ]; then
    STATUS="📋 READY"
  else
    STATUS="📝 CREATED"
  fi

  echo "$TASK_ID: $STATUS"
done

echo ""
echo "=== FINE ==="
