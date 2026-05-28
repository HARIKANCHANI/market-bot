"""
Verify Git Push - Check if all changes were committed and pushed successfully
"""

import subprocess
import sys

def run_git_command(cmd):
    """Run a git command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd="."
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1

print("="*80)
print("🔍 GIT PUSH VERIFICATION")
print("="*80)

# 1. Check current branch
print("\n1. Current Branch:")
stdout, stderr, code = run_git_command("git branch --show-current")
if code == 0:
    print(f"   ✅ Branch: {stdout}")
else:
    print(f"   ❌ Error: {stderr}")

# 2. Check last commit
print("\n2. Last Commit:")
stdout, stderr, code = run_git_command("git log --oneline -1")
if code == 0:
    print(f"   ✅ {stdout}")
else:
    print(f"   ❌ Error: {stderr}")

# 3. Check tags
print("\n3. Git Tags:")
stdout, stderr, code = run_git_command("git tag -l")
if code == 0 and stdout:
    tags = stdout.split('\n')
    for tag in tags:
        print(f"   ✅ {tag}")
else:
    print(f"   ⚠️  No tags found")

# 4. Check if tag v2.0.0 exists
print("\n4. Version 2.0.0 Tag:")
stdout, stderr, code = run_git_command("git tag -l v2.0.0")
if code == 0 and stdout:
    print(f"   ✅ Tag v2.0.0 exists")
else:
    print(f"   ❌ Tag v2.0.0 NOT found")

# 5. Check remote status
print("\n5. Remote Status:")
stdout, stderr, code = run_git_command("git status -sb")
if code == 0:
    print(f"   ✅ {stdout}")
else:
    print(f"   ❌ Error: {stderr}")

# 6. Check if working tree is clean
print("\n6. Working Tree Status:")
stdout, stderr, code = run_git_command("git status --porcelain")
if code == 0:
    if not stdout:
        print(f"   ✅ Working tree is clean (all changes committed)")
    else:
        print(f"   ⚠️  Uncommitted changes:")
        for line in stdout.split('\n'):
            print(f"      {line}")
else:
    print(f"   ❌ Error: {stderr}")

# 7. Check remote URL
print("\n7. Remote Repository:")
stdout, stderr, code = run_git_command("git remote get-url origin")
if code == 0:
    print(f"   ✅ {stdout}")
else:
    print(f"   ❌ Error: {stderr}")

# 8. Check if local is ahead/behind remote
print("\n8. Sync Status:")
stdout, stderr, code = run_git_command("git status -uno")
if code == 0:
    if "Your branch is up to date" in stdout:
        print(f"   ✅ Local branch is in sync with remote")
    elif "Your branch is ahead" in stdout:
        print(f"   ⚠️  Local branch is ahead of remote (push needed)")
    elif "Your branch is behind" in stdout:
        print(f"   ⚠️  Local branch is behind remote (pull needed)")
    else:
        print(f"   ℹ️  Status: {stdout.split('On branch')[1].split('\\n')[1] if 'On branch' in stdout else 'Unknown'}")
else:
    print(f"   ❌ Error: {stderr}")

print("\n" + "="*80)
print("✅ VERIFICATION COMPLETE")
print("="*80)
