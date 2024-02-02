#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_SET_current.sh
# ----------------------------------------------------------------------------
# ***SET_current
# ----------------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' SET_current'
echo '---------------------------------------------'
git config user.name "lisitsinyr"

git config user.email "lisitsinyr@gmail.com"

git config --list > ~/DATA/GIT/GIT_CONFIG_set_list_current

#:Exit
