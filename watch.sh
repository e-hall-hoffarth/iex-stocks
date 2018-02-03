#!/bin/bash

DIR='data/out/'

watch -n2 "echo "Number of files: " && ls $DIR | wc -l && echo "Most recently created: " && ls -t $DIR | head -10 && echo "Size of directory: " && du -h $DIR"
