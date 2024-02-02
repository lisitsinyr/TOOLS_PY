@echo off
rem -------------------------------------------------------------------
rem lyrgit_pull.bat
rem ----------------------------------------------------------------------------
rem ***Получить изменения
rem ----------------------------------------------------------------------------
rem usage: git pull [<options>] [<repository> [<refspec>...]]
rem 
rem     -v, --[no-]verbose    be more verbose
rem     -q, --[no-]quiet      be more quiet
rem     --[no-]progress       force progress reporting
rem     --[no-]recurse-submodules[=<on-demand>]
rem                           control for recursive fetching of submodules
rem 
rem Options related to merging
rem     -r, --[no-]rebase[=(false|true|merges|interactive)]
rem                           incorporate changes by rebasing rather than merging
rem     -n                    do not show a diffstat at the end of the merge
rem     --[no-]stat           show a diffstat at the end of the merge
rem     --[no-]log[=<n>]      add (at most <n>) entries from shortlog to merge commit message
rem     --[no-]signoff[=...]  add a Signed-off-by trailer
rem     --[no-]squash         create a single commit instead of doing a merge
rem     --[no-]commit         perform a commit if the merge succeeds (default)
rem     --[no-]edit           edit message before committing
rem     --[no-]cleanup <mode> how to strip spaces and #comments from message
rem     --[no-]ff             allow fast-forward
rem     --ff-only             abort if fast-forward is not possible
rem     --[no-]verify         control use of pre-merge-commit and commit-msg hooks
rem     --[no-]verify-signatures
rem                           verify that the named commit has a valid GPG signature
rem     --[no-]autostash      automatically stash/stash pop before and after
rem     -s, --[no-]strategy <strategy>
rem                           merge strategy to use
rem     -X, --[no-]strategy-option <option=value>
rem                           option for selected merge strategy
rem     -S, --[no-]gpg-sign[=<key-id>]
rem                           GPG sign commit
rem     --[no-]allow-unrelated-histories
rem                           allow merging unrelated histories
rem 
rem Options related to fetching
rem     --[no-]all            fetch from all remotes
rem     -a, --[no-]append     append to .git/FETCH_HEAD instead of overwriting
rem     --[no-]upload-pack <path>
rem                           path to upload pack on remote end
rem     -f, --[no-]force      force overwrite of local branch
rem     -t, --[no-]tags       fetch all tags and associated objects
rem     -p, --[no-]prune      prune remote-tracking branches no longer on remote
rem     -j, --[no-]jobs[=<n>] number of submodules pulled in parallel
rem     --[no-]dry-run        dry run
rem     -k, --[no-]keep       keep downloaded pack
rem     --[no-]depth <depth>  deepen history of shallow clone
rem     --[no-]shallow-since <time>
rem                           deepen history of shallow repository based on time
rem     --[no-]shallow-exclude <revision>
rem                           deepen history of shallow clone, excluding rev
rem     --[no-]deepen <n>     deepen history of shallow clone
rem     --unshallow           convert to a complete repository
rem     --[no-]update-shallow accept refs that update .git/shallow
rem     --refmap <refmap>     specify fetch refmap
rem     -o, --[no-]server-option <server-specific>
rem                           option to transmit
rem     -4, --[no-]ipv4       use IPv4 addresses only
rem     -6, --[no-]ipv6       use IPv6 addresses only
rem     --[no-]negotiation-tip <revision>
rem                           report that we have only objects reachable from this object
rem     --[no-]show-forced-updates
rem                           check for forced-updates on all updated branches
rem     --[no-]set-upstream   set upstream for git pull/fetch
rem ----------------------------------------------------------------------------
chcp 1251

:begin
echo ---------------------------------------------------------------
echo git pull
echo ---------------------------------------------------------------
git pull

:Exit
