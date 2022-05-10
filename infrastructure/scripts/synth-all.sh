#!/bin/bash

stacks=(
    tglanz-web-server-stack
    tglanz-web-server-stack-v2
    tglanz-eks-stack
    tglanz-eks-stack-v2
)

function synth_stack() {
    stack=$1
    target_path="cdk.out/$stack.yaml"
    echo "$stack: Synthesizing"
    cdk synth --app "python app.py" $stack > $target_path
    echo "$stack: Template at $target_path"
}

for stack in ${stacks[@]}; do 
    synth_stack $stack &
done

wait
