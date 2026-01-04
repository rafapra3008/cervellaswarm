#!/bin/bash
cd /Users/rafapra/Developer/CervellaSwarm
/Users/rafapra/.nvm/versions/node/v24.11.0/bin/claude --append-system-prompt "$(cat /Users/rafapra/Developer/CervellaSwarm/.swarm/prompts/worker_guardiana-qualita.txt)" "Controlla .swarm/tasks/ per task assegnati a te e inizia a lavorare. Se non ci sono task, aspetta istruzioni."
