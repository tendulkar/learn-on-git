#!/usr/bin/env bash
export BRANCH="master"
if [ ! -z $1 ]; then
    export BRANCH=$1
fi

git add .
git commit
git pull origin $BRANCH
git push origin $BRANCH