export BRANCH=master
if [ -z "$1" ]; then
   export BRANCH=$1
fi

git add .;
git commit
git push origin $BRANCH
