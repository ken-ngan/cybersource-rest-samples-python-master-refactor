# Git Push Steps - Quick Reference

## Initial Push (First Time Only)

```bash
# 1. Initialize repository (if not already done)
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: CyberSource REST samples refactored project"

# 4. Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 5. Push to GitHub
git branch -M main
git push -u origin main
```

## Subsequent Pushes (Daily Workflow)

After the initial setup, use these steps for every update:

### Step 1: Check Status
See what files have changed:
```bash
git status
```

### Step 2: Stage Changes
Add the files you want to commit:

**Option A: Add all changed files**
```bash
git add .
```

**Option B: Add specific files**
```bash
git add path/to/file1.py path/to/file2.py
```

**Option C: Add all files in a directory**
```bash
git add views/
```

### Step 3: Commit Changes
Create a commit with a descriptive message:
```bash
git commit -m "Brief description of your changes"
```

**Good commit messages examples:**
- `"Fix: Resolve card number missing in soap_validation"`
- `"Feature: Add URL switcher for localhost/ngrok"`
- `"Refactor: Improve PCI compliance for CVV handling"`
- `"Update: Fix authentication flow in REST API"`

### Step 4: Push to GitHub
Push your commits:
```bash
git push
```

**Note**: If you used `-u origin main` in the initial push, you can just use `git push`. Otherwise:
```bash
git push origin main
```

## Complete Example Workflow

```bash
# 1. Check what changed
git status

# 2. Add all changes
git add .

# 3. Commit with message
git commit -m "Fix: Update URL switcher logic"

# 4. Push to GitHub
git push
```

## Common Scenarios

### Push Changes to Existing Branch

```bash
git add .
git commit -m "Your commit message"
git push
```

### Create and Push New Branch

```bash
# Create new branch
git checkout -b feature/new-feature

# Make changes, then:
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

### Update Existing Branch

```bash
git add .
git commit -m "Update feature"
git push
```

### Push Specific Files Only

```bash
git add config.py main.py
git commit -m "Update configuration files"
git push
```

### Undo Last Commit (Before Push)

If you haven't pushed yet and want to undo:
```bash
git reset HEAD~1
```

**Caution**: Only do this if you haven't pushed yet!

## Quick One-Liner

For quick updates, you can combine steps:
```bash
git add . && git commit -m "Your message" && git push
```

## Troubleshooting

### "Your branch is ahead of origin/main"

This means you have local commits not yet pushed. Just run:
```bash
git push
```

### "Updates were rejected"

Someone else pushed changes. Pull first:
```bash
git pull
# Resolve any conflicts, then:
git push
```

### "Authentication failed"

Use Personal Access Token instead of password:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password

### Undo Changes (Before Commit)

```bash
# Discard changes in working directory
git checkout -- filename.py

# Discard all changes
git checkout -- .
```

## Best Practices

1. **Commit Often**: Make small, logical commits
2. **Write Clear Messages**: Describe what and why you changed
3. **Check Before Push**: Run `git status` to see what will be pushed
4. **Pull Before Push**: If working with others, `git pull` first
5. **Don't Commit Secrets**: Always check `.gitignore` includes `.env`

## Daily Workflow Summary

```bash
# Morning: Pull latest changes
git pull

# After making changes:
git add .
git commit -m "Description of changes"
git push

# End of day: Ensure everything is pushed
git status
git push
```
