#!/bin/bash
# -------------------------------------------------------------------
# lyrgit_push_main.sh
# ----------------------------------------------------------------------------
# ***Отправить изменения
# ----------------------------------------------------------------------------
# usage: git push [<options>] [<repository> [<refspec>...]]
# 
#     -v, --verbose         be more verbose
#     -q, --quiet           be more quiet
#     --repo <repository>   repository
#     --all                 push all refs
#     --mirror              mirror all refs
#     -d, --delete          delete refs
#     --tags                push tags (can't be used with --all or --mirror)
#     -n, --dry-run         dry run
#     --porcelain           machine-readable output
#     -f, --force           force updates
#     --force-with-lease[=<refname>:<expect>]
#                           require old value of ref to be at this value
#     --force-if-includes   require #ote updates to be integrated locally
#     --recurse-submodules (check|on-demand|no)
#                           control recursive pushing of submodules
#     --thin                use thin pack
#     --receive-pack <receive-pack>
#                           receive pack program
#     --exec <receive-pack>
#                           receive pack program
#     -u, --set-upstream    set upstream for git pull/status
#     --progress            force progress reporting
#     --prune               prune locally #oved refs
#     --no-verify           bypass pre-push hook
#     --follow-tags         push missing but relevant tags
#     --signed[=(yes|no|if-asked)]
#                           GPG sign the push
#     --atomic              request atomic transaction on #ote side
#     -o, --push-option <server-specific>
#                           option to transmit
#     -4, --ipv4            use IPv4 addresses only
#     -6, --ipv6            use IPv6 addresses only
# -------------------------------------------------------------------

#:begin
echo '---------------------------------------------'
echo ' Отправить изменения'
echo '     git add --all'
echo '     git commit -m "$Comment"'
echo '     git push -u origin main'
echo '---------------------------------------------'
echo 'Check 1 parametr'
if [ -n "$1" ]; then
    Comment="$1"
else
    Comment=""
    read -p "Comment: " Comment
fi

if [ -z "$Comment" ]; then
    echo 'Parametr $Comment not specified'
    set Comment='Git Bash commit update'
fi

if [ ! -z "$Comment" ]; then
    echo $Comment
    git add --all
    git commit -m "$Comment"
    git push -u origin main
fi

#:Exit
