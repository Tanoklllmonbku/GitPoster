# commands/add.py
def git_add_files(files, cwd):
    return ["git", "add"] + files, cwd