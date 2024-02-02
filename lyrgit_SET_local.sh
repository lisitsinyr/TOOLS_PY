#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_SET_local.sh
# ----------------------------------------------------------------------------
# ***SET_local
# ----------------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' SET_local'
echo '---------------------------------------------'
git config --global user.name "lisitsinyr"

git config --global user.email "lisitsinyr@gmail.com"

git config --list > ~/DATA/GIT/GIT_CONFIG_set_list_local

#:Exit
