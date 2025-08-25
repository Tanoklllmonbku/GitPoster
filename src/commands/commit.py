# commands/commit.py
def git_commit(message, cwd):
    return ["git", "commit", "-m", message], cwd