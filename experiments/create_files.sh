#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <destination_path> <name_template>"
    echo "Example: $0 experiments/data add_two_numbers"
    exit 1
fi

DEST_DIR=$1
BASE_NAME=$2

mkdir -p "$DEST_DIR"

for i in {1..10}
do
    INDEX=$(printf "%02d" $i)

    touch "${DEST_DIR}/${BASE_NAME}_${INDEX}.java"
done

echo "Success: files created in $DEST_DIR"