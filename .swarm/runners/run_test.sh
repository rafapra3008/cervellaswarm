#!/bin/bash
export CERVELLASWARM_WORKER=1
stdbuf -oL /Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude -p --append-system-prompt "$(cat .swarm/prompts/worker_test.txt)" "Test prompt" 2>&1 | tee "$LOG_FILE"
