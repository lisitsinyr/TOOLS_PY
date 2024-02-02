#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_checkout_..sh
# ----------------------------------------------------------------------------
# Переключится на ветку (branch)
# ----------------------------------------------------------------------------
# usage: git checkout [<options>] <branch>
#    or: git checkout [<options>] [<branch>] -- <file>...
# 
#     -b <branch>           create and checkout a new branch
#     -B <branch>           create/reset and checkout a branch
#     -l                    create reflog for new branch
#     --[no-]guess          second guess 'git checkout <no-such-branch>' (default)
#     --[no-]overlay        use overlay mode (default)
#     -q, --[no-]quiet      suppress progress reporting
#     --[no-]recurse-submodules[=<checkout>]
#                           control recursive updating of submodules
#     --[no-]progress       force progress reporting
#     -m, --[no-]merge      perform a 3-way merge with the new branch
#     --[no-]conflict <style>
#                           conflict style (merge, diff3, or zdiff3)
#     -d, --[no-]detach     detach HEAD at named commit
#     -t, --[no-]track[=(direct|inherit)]
#                           set branch tracking configuration
#     -f, --[no-]force      force checkout (throw away local modifications)
#     --[no-]orphan <new-branch>
#                           new unparented branch
#     --[no-]overwrite-ignore
#                           update ignored files (default)
#     --[no-]ignore-other-worktrees
#                           do not check if another worktree is holding the given ref
#     -2, --ours            checkout our version for unmerged files
#     -3, --theirs          checkout their version for unmerged files
#     -p, --[no-]patch      select hunks interactively
#     --[no-]ignore-skip-worktree-bits
#                           do not limit pathspecs to sparse entries only
#     --[no-]pathspec-from-file <file>
#                           read pathspec from file
#     --[no-]pathspec-file-nul
#                           with --pathspec-from-file, pathspec elements are separated with NUL character
# ----------------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' git checkout .'
echo '---------------------------------------------'
git checkout .

#:exit
