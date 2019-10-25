import os

def clear_cwd_cache():
    dirs_to_skip = ['.git', 'venv']

    for root, dirs, files in os.walk(os.getcwd()):
        root_split = root.split('/')
        dir = root_split[-1]

        if any(dir_to_skip in root_split for dir_to_skip in dirs_to_skip):
            continue

        if dir == 'cache':
            for file in files:
                os.remove(f"{root}/{file}")
            for dir in dirs:
                os.remove(f"{root}/{dir}")

    print('cache is now empty')
