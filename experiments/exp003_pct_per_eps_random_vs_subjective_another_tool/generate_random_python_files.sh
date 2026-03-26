#!/usr/bin/env bash
# Generate random Python source files using pysource-codegen.
#
# Example:
#   ./generate_random_python_files.sh 50 experiments/exp003_.../data/random_python

set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <count> <output-dir>" >&2
    exit 1
fi

COUNT="$1"
OUTPUT_DIR="$2"

if ! command -v pysource-codegen &> /dev/null; then
    echo "Error: pysource-codegen not found. Install it with: pip install pysource-codegen" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

for i in $(seq 1 "$COUNT"); do
    seed=$((i - 1))
    pysource-codegen --seed "$seed" > "$OUTPUT_DIR/${i}-seed_${seed}.py"
done

echo "Generated $COUNT Python files in $OUTPUT_DIR"
