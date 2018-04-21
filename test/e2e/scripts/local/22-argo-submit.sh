#!/bin/bash

set -x

cd $(dirname $0)

# TODO run all workflows ?

ls -l ../../argo-workflows/agent.yaml || exit 2

./argo submit ../../argo-workflows/agent.yaml -w

exit 0
