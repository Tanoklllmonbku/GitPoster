# commands/status.py
def git_status_porcelain(cwd):
    return ["git", "status", "--porcelain", "-u"], cwd