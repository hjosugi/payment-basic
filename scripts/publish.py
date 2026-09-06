"""Create four new repositories. Preview by default; never overwrite a remote."""
import argparse
from pathlib import Path
import re
import shlex
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--owner", default="hjosugi")
parser.add_argument("--visibility", choices=["private", "public"], default="private")
parser.add_argument("--execute", action="store_true")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z0-9-]+", args.owner):
    parser.error("invalid GitHub owner")
root = Path(__file__).resolve().parents[2]
names = ["payment-basic", "payment-basic-ts", "payment-basic-go", "payment-basic-java"]
for name in names:
    if not (root / name / "README.md").is_file():
        raise SystemExit("Extract all four repository directories before publishing")

commands = [["gh", "repo", "create", args.owner + "/" + name, "--" + args.visibility,
             "--source", str(root / name), "--remote", "origin", "--push"] for name in names]
if not args.execute:
    for command in commands: print(shlex.join(command))
    print("Preview only. Add --execute to create and push the repositories.")
    raise SystemExit(0)
for tool in ("git", "gh"):
    if not shutil.which(tool): raise SystemExit("Install " + tool + " first")
subprocess.run(["gh", "auth", "status"], check=True)

# Refuse every existing repository before creating any new one.
for name in names:
    result = subprocess.run(["gh", "repo", "view", args.owner + "/" + name, "--json", "name"], capture_output=True, text=True)
    if result.returncode == 0:
        raise SystemExit("Remote already exists: " + args.owner + "/" + name + ". No remote was changed.")
    local = root / name
    if (local / ".git").exists():
        remotes = subprocess.check_output(["git", "remote"], cwd=local, text=True)
        if remotes.strip(): raise SystemExit("Local remotes already exist: " + name)

# Prepare every local commit before creating remote repositories.
for name in names:
    local = root / name
    if not (local / ".git").exists(): subprocess.run(["git", "init", "-b", "main"], cwd=local, check=True)
    subprocess.run(["git", "add", "."], cwd=local, check=True)
    subprocess.run(["git", "-c", "user.name=Payment Basic Generator", "-c", "user.email=generator@users.noreply.github.com",
                    "commit", "--allow-empty", "-m", "Implement resilient payment learning project"], cwd=local, check=True)
for command in commands:
    subprocess.run(command, check=True)
print("Created and pushed all four repositories.")
