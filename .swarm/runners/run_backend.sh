#!/bin/bash
cd /Users/rafapra/Developer/CervellaSwarm
claude --append-system-prompt "$(cat /Users/rafapra/Developer/CervellaSwarm/.swarm/prompts/worker_backend.txt)"
