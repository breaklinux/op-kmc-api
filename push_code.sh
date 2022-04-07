#!/bin/bash
find .  -name __pycache__ |xargs rm -rf
messgae=$1
git add --all
git commit -m "$messgae"
git push 

