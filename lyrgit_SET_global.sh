#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_SET_global.sh
# ----------------------------------------------------------------------------
# ***SET_global
# ----------------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' SET_global'
echo '---------------------------------------------'
git config --global user.name "lisitsinyr"

git config --global user.email "lisitsinyr@gmail.com"

git config --list > ~/DATA/GIT/GIT_CONFIG_set_list_global

#:Exit
