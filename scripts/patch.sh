#!/usr/bin/env bash
set -Eeuo pipefail

if [ -z "$(git status --porcelain)" ]; then 
	# Working directory clean
	branch_name=$(git symbolic-ref -q HEAD)
	branch_name=${branch_name##refs/heads/}
	branch_name=${branch_name:-HEAD}
	
	poetry version patch
	version=`sed 's/version = "\([0-9]*.[0-9]*.[0-9]*\)"/\1/p' -n <pyproject.toml`
	read -p "Create commit for version $version? " -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		# do dangerous stuff
		echo "Creating a new patch"
		git add pyproject.toml
		git commit -m "Created version $version"
		git tag -a "$version" -m "patch.sh created version $version"
		git push --tags
	else
		echo "Surrendering, clean up by reverting pyproject.toml..."
		exit 2
	fi
else 
	echo "Can't create patch version, working tree unclean..."
	exit 1
fi
