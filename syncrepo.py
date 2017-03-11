import argparse
import json
import os
import sys
import subprocess
import git
import requests

# Create arguments for CLI
parser = argparse.ArgumentParser()
parser.add_argument('--no-skip-forks', '-ns',
                    help='Skips if the current repository is a fork', action="store_true")
parser.add_argument('--directory', '-d',
                    help='Set location for sync. If not set, cwd is used')
parser.add_argument('---lang-dir', '-ld',
                    help='Segregate git project folders by language (May or may not work with existing projects)', action="store_true")
parser.add_argument('--commit-all', '-c',
                    help='Commit everything to the current git repository', action="store_true")
checkArgs = parser.parse_args()
skipForks = not checkArgs.no_skip_forks
currDir = checkArgs.directory
langDir = checkArgs.lang_dir
commitAll = checkArgs.commit_all


# Check if current folder is a git folder
def checkGit(path):
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


# Clone current repository if it doesn't exist
def cloneRepo(remoteURL, workDir):
    os.system('git -C ' + workDir + ' clone ' + remoteURL + ' &> /dev/null')


# Sync local repostories and commit if argument is passed
def gitSync(repoURL, workDir):
    print("Sycing repo", repoURL)
    gitURL = repoURL.replace(".git", "").split("github.com/")
    path = gitURL[1]
    user, repo = path.split("/")
    workDir += repo
    # Pull first
    print(workDir)
    os.system('git -C ' + workDir + ' pull origin master ')  # &> /dev/null')
    # Check if argument to commit has been passed
    if commitAll:
        with open('commit.txt', 'r') as commit:
            commitMessage = commit.read().strip('\n')
        if not commitMessage:
            commitMessage = input('No commit message found for repository',
                                  repoURL, '\nPlease enter a commit message: ')
        os.system(
            'git add --all && git commit -m "{}" &> /dev/null'.format(commitMessage))
        os.system('git push origin master')
        print('Updated repository', repoURL)
    print("Sync complete")


# Remote sync fork repositories
def gitSyncFork(repoURL, workDir):
    print("Syncing fork", repoURL)
    gitURL = repoURL.replace(".git", "").split("github.com/")
    path = gitURL[1]
    user, repo = path.split("/")
    workDir += repo
    print(os.getcwd())
    print("Updating fork from parent source", "\n")
    url = "https://api.github.com/repos/{}/{}".format(user, repo)
    req = requests.get(url)
    res = json.loads(req.content)
    for getURL in res:
        parentURL = res["parent"]["git_url"]
    os.system('git -C ' + workDir + '/ remote add upstream ' +
              parentURL + '&> /dev/null')
    print("Checking remotes...", "\n")
    os.system('git -C ' + workDir + '/ remote -v &> /dev/null')
    print("Fetching upstream...", "\n")
    os.system('git -C ' + workDir + '/ fetch upstream &> /dev/null')
    print("Merging upstream and master", "\n")
    os.system('git -C ' + workDir + '/ merge upstream/master &> /dev/null')
    print("Fork updated.")



# Check, create and sync repo
def syncRepo(repoURL, language, path, isFork):
    global cloneAll
    notFound = 0
    CURRENT_REPO_CMD = ['git', 'config', '--get', 'remote.origin.url']
    workDir = path
    if langDir:
        if language is None:
            language = "Other"
        if not os.path.isdir(path + language):
            os.makedirs(path + language)
        workDir += language
    if cloneAll:    # Since no directory existed in previous iteration, we'll clone all the repos
        cloneRepo(repoURL, workDir)
    elif not os.listdir(workDir):
        clone = input(
            'No directories exist. Do you want to clone all the repositories? (Yes) ')
        if not clone:
            clone = 'yes'
        if clone.lower() == 'yes':
            cloneAll = 1
            cloneRepo(repoURL, workDir)
        else:
            print("No repositories to be synced, terminating")
            sys.exit()
    else:
        # Check every file in the directory
        for directory in os.listdir(workDir):
            # Check if the current value of directory is a directory
            if os.path.isdir(os.path.join(workDir, directory)):
                ifGit = checkGit(os.path.join(workDir, directory))
                if ifGit:   # Current directory is a git directory
                    getremoteURL = subprocess.Popen('git -C ' + os.path.join(
                        workDir, directory) + ' config --get remote.origin.url', stdout=subprocess.PIPE, shell=True)
                    remoteURL = getremoteURL.stdout.read().decode('utf-8')
                    if repoURL == remoteURL.strip('\n'):
                        notFound = 0
                        if skipForks:   # --no-skip-forks is not passed
                            if not isFork:  # Skip forks
                                gitSync(repoURL, workDir)
                        else:
                            if isFork:  # Update both local and remote forks
                                gitSyncFork(repoURL, workDir)
                            else:       # Not a fork, so we'll sync
                                gitSync(repoURL, workDir)
                        break
                    else:
                        notFound = 1
        if notFound:
            if skipForks:
                if not isFork:
                    clone = input("Git repository for " + repoURL +
                                  " not found. Do you want to clone the repo? (Yes) ")
                    if not clone:
                        clone = "yes"
                    if clone.lower() == 'yes':
                        cloneRepo(repoURL, workDir)
                    else:
                        print('Skipping the current repository')
            else:
                clone = input("Git repository for " + repoURL +
                              " not found. Do you want to clone the repo? (Yes) ")
                if not clone:
                    clone = "yes"
                if clone.lower() == 'yes':
                    cloneRepo(repoURL, workDir)
                else:
                    print('Skipping the current repository')


def main():
    global cloneAll, currDir, getURL
    cloneAll = 0
    urlList = []
    langList = []
    forkList = []
    if not commitAll:
        print('New updates to the repositories will not be pushed. Use --commit-all to push updates', "")
    if skipForks:
        print('Forks will not be synced. Use --no-skip-forks to sync forks', "")
    if langDir:
        print('Repositories will be segregated by languages', "")
    user = input("Enter the username for which you'd like to sync: ")
    try:
        getReq = requests.get(
            "https://api.github.com/users/{}/repos".format(user))
    except Exception as e:
        print('Error retreiving data. The errors are: \n', e.message)
    if currDir:
        if not os.path.isdir(currDir):
            print("No such directory exists, using current directory.")
            os.makedirs("GitSync")
            currDir = "GitSync/"
    else:
        if not os.path.isdir("GitSync"):
            os.makedirs("GitSync")
        currDir = "GitSync/"
    getJSON = json.loads(getReq.content)
    for getURL in getJSON:
        syncRepo(getURL["clone_url"], getURL[
                 "language"], currDir, getURL["fork"])
    print('Done.')
    sys.exit()

if __name__ == '__main__':
    main()
