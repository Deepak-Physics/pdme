#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "$(git status --porcelain)" ]; then
	branch_name=$(git symbolic-ref -q HEAD)
	branch_name=${branch_name##refs/heads/}
	branch_name=${branch_name:-HEAD}
	if [ $branch_name != "master" ]; then
		echo "The current branch is not master!"
		echo "I'd feel uncomfortable releasing from here..."
		exit 3
	fi

	release_needed=false
	if \
		{ git log "$( git describe --tags --abbrev=0 )..HEAD" --format='%s' | cut -d: -f1 | sort -u | sed -e 's/([^)]*)//' | grep -q -i -E '^feat|fix|perf|refactor|revert$' ; } || \
		{ git log "$( git describe --tags --abbrev=0 )..HEAD" --format='%s' | cut -d: -f1 | sort -u | sed -e 's/([^)]*)//' | grep -q -E '\!$' ; } || \
		{ git log "$( git describe --tags --abbrev=0 )..HEAD" --format='%b' | grep -q -E '^BREAKING CHANGE:' ; }
	then
		release_needed=true
	fi
	
	if ! [ "$release_needed" = true ]; then
		echo "No release needed..."
		exit 0
	fi

	# Working directory clean
	echo "Doing a dry run..."
	npx standard-version --dry-run
	read -p "Does that look good? [y/N] " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		# do dangerous stuff
		npx standard-version
		git push --follow-tags origin master
	else
		echo "okay, never mind then..."
		exit 2
	fi
else 
	echo "Can't create release, working tree unclean..."
	exit 1
fi
