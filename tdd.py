import argparse
import os
import pathlib
import time


parser = argparse.ArgumentParser(
    description="Automatically run a command when changes have been detected in the targeted directories"
)
parser.add_argument(
    "--cmd",
    default="pytest -x -q --no-header",
    help="This will be executed when changes are detected in the targeted directories",
)
parser.add_argument(
    "dirs",
    nargs="*",
    help="The directories to watch for changes in. Relative to CWD.",
)
parser.add_argument(
    "--ft",
    nargs="*",
    help="The filetypes to watch for changes in.",
    default=[".py"],
)

args = parser.parse_args()
if len(args.dirs) == 0:
    print("ERROR: No directories specified.")
    parser.print_help()
    exit()

CLEAR = "cls" if os.name == "nt" else "clear"
DIRS = [pathlib.Path.cwd() / dirname for dirname in args.dirs]
REINDEXING_POLL_RATE = 5
MODIFYING_POLL_RATE = 0.25
registry = dict()


def main():
    index_dirs()
    next_reindex = time.time() + REINDEXING_POLL_RATE
    next_mod_check = time.time() + MODIFYING_POLL_RATE
    execute()

    while True:
        # expecting keyboard interupt to stop
        t = time.time()
        if t > next_reindex:
            if index_dirs():
                execute()
            next_reindex = time.time() + REINDEXING_POLL_RATE
        elif t > next_mod_check:
            if check_for_modifications():
                execute()
            next_mod_check = time.time() + MODIFYING_POLL_RATE
        time.sleep(0.05)


def index_dirs():
    files = crawl_dirs(
        DIRS,
        lambda p: any(p.name.endswith(ext) for ext in args.ft),
    )
    result = False
    if len(files) != len(registry):
        result = True
    for path in files:
        mod_time = path.stat().st_mtime
        if path not in registry:
            result = True
        elif registry[path] != mod_time:
            result = True
        else:
            continue
        registry[path] = mod_time
    return result


def check_for_modifications():
    result = False
    for path, prev_mod in registry.copy().items():
        if not path.exists():
            result = True
            del registry[path]
            continue
        mod_time = path.stat().st_mtime
        if mod_time != prev_mod:
            result = True
            registry[path] = mod_time
    return result


def execute():
    os.system(CLEAR)
    os.system(args.cmd)


def crawl_dirs(dirs, predicate=None, files=None):
    if files is None:
        files = []
    for d in dirs:
        for p in d.iterdir():
            if p.is_dir():
                crawl_dirs([p], predicate, files)
            elif predicate is not None:
                if predicate(p):
                    files.append(p)
            else:
                files.append(p)
    return files


if __name__ == "__main__":
    main()
