# commands/remote.py
def git_remote_add_origin(url: str, cwd):
    return ["git", "remote", "add", "origin", url], cwd