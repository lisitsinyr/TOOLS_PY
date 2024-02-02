#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_remote_v.sh
# ----------------------------------------------------------------------------
# 6.Сотрудничать [***]
# ----------------------------------------------------------------------------
# Верифицируем что удаленный репозитарий связан с нашим
# ----------------------------------------------------------------------------
# usage: git #ote [-v | --verbose]
#    or: git #ote add [-t <branch>] [-m <master>] [-f] [--tags | --no-tags] [--mirror=<fetch|push>] <name> <url>
#    or: git #ote rename [--[no-]progress] <old> <new>
#    or: git #ote #ove <name>
#    or: git #ote set-head <name> (-a | --auto | -d | --delete | <branch>)
#    or: git #ote [-v | --verbose] show [-n] <name>
#    or: git #ote prune [-n | --dry-run] <name>
#    or: git #ote [-v | --verbose] update [-p | --prune] [(<group> | <#ote>)...]
#    or: git #ote set-branches [--add] <name> <branch>...
#    or: git #ote get-url [--push] [--all] <name>
#    or: git #ote set-url [--push] <name> <newurl> [<oldurl>]
#    or: git #ote set-url --add <name> <newurl>
#    or: git #ote set-url --delete <name> <url>
# 
#     -v, --verbose         be verbose; must be placed before a subcommand
# -------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' git remote -v'
echo '---------------------------------------------'
git remote -v
