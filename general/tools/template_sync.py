"""Keep a project's shared files in step with the project-template repo.

    python general/tools/template_sync.py status      # which shared files differ from the template
    python general/tools/template_sync.py pull        # take the template's newest shared files (never touches project/)
    python general/tools/template_sync.py push-hint   # list files you changed here that should go back to the template

Needs a git remote called "template" pointing at project-template (the setup-project skill adds it):
    git remote add template https://github.com/<you>/project-template.git
Nothing is committed: review the changes, run the tests, then commit when you are ready.
"""
import argparse
import subprocess
import sys

SHARED = ["general", ".claude/skills", "tests/test_design_system.py", "tests/test_onshape_images.py", "tests/fixtures",
          "tests/test_template_tools.py", ".github/workflows/tests.yml", "CLAUDE.md", "requirements.txt", ".gitignore"]


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout.strip()


def changed_files(ref):
    return [f for f in git("diff", "--name-only", ref, "--", *SHARED).splitlines() if f]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["status", "pull", "push-hint"])
    ap.add_argument("--branch", default="main")
    a = ap.parse_args(argv)
    if "template" not in git("remote").split():
        sys.exit("No 'template' remote. Add it: git remote add template <project-template URL>")
    git("fetch", "template", a.branch)
    ref = f"template/{a.branch}"
    if a.action == "status":
        diff = changed_files(ref)
        print("\n".join(diff) if diff else "Shared files match the template.")
    elif a.action == "pull":
        if git("status", "--porcelain", "--", *SHARED):
            sys.exit("You have uncommitted changes in shared files. Commit or stash them first (push-hint lists them).")
        before = changed_files(ref)
        present = [p for p in SHARED if git("ls-tree", "--name-only", ref, p, check=False)]
        git("checkout", ref, "--", *present)
        print("Updated from the template:" if before else "Already up to date.")
        for f in before:
            print("  ", f)
        print("Run: python -m pytest tests -q   then commit when you are happy.")
    else:
        diff = changed_files(ref)
        print("These shared files differ from the template. Copy the improvements into a clone of project-template,"
              " commit there, then pull into each project:" if diff else "Nothing to send back.")
        for f in diff:
            print("  ", f)


if __name__ == "__main__":
    main()
