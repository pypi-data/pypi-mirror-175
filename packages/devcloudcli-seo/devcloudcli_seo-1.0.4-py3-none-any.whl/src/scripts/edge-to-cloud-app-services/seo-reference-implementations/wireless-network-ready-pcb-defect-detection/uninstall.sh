#!/bin/bash
#Copyright (C) 2018-2021 Intel Corporation
#SPDX-License-Identifier: Apache-2.0

RI_PATH="$HOME/*/workload"

cd $RI_PATH
RI_ID=$($HOME/.local/bin/edgesoftware list | awk '{print $2}' | awk 'FNR==4 {print}')
if [[ $RI_ID ]]; then
    $HOME/.local/bin/edgesoftware uninstall -a 
else
    echo "No RI is installed"
fi

if [[ (-f $RI_PATH/edgesoftware_configuration.xml) ]]; then
    sudo rm -rf $RI_PATH/edgesoftware_configuration.xml
fi

if [[ (-d /var/log/esb-cli) ]]; then
    sudo rm -rf /var/log/esb-cli
fi
