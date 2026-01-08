#!/bin/bash
# Test diretto stdbuf con claude
echo "Testing stdbuf con echo progressivo..."
for i in {1..5}; do
    echo "Output $i"
    sleep 1
done
