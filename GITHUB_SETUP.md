# Step-by-Step Guide: Push Project to GitHub

This guide will walk you through pushing your project to GitHub from scratch.

## Prerequisites

1. **Git installed** on your system
   - Check: `git --version`
   - If not installed: Download from [git-scm.com](https://git-scm.com/downloads)

2. **GitHub account** created
   - Sign up at [github.com](https://github.com) if you don't have one

3. **GitHub authentication** set up
   - Personal Access Token (recommended) or SSH key
   - See: [GitHub Docs - Authentication](https://docs.github.com/en/authentication)

## Step-by-Step Instructions

### Step 1: Initialize Git Repository

Open terminal in your project directory and run:

```bash
cd /Users/ccngan/cybersource-rest-samples-python-master-refactor
git init
```

This creates a new Git repository in your project folder.

### Step 2: Verify .gitignore File

Make sure your `.gitignore` file is properly configured to exclude sensitive files:

```bash
cat .gitignore
```

**Important**: Ensure these are in `.gitignore`:
- `.env` (contains sensitive credentials)
- `__pycache__/`
- `*.pyc`
- `.venv/` or `venv/`
- `*.p12` (certificate files)
- Any other sensitive files

### Step 3: Add Files to Git

Add all files to Git staging area:

```bash
git add .
```

**Note**: Files in `.gitignore` will be automatically excluded.

### Step 4: Create Initial Commit

Commit your files:

```bash
git commit -m "Initial commit: CyberSource REST samples refactored project"
```

### Step 5: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the repository details:
   - **Repository name**: `cybersource-rest-samples-python-refactor` (or your preferred name)
   - **Description**: "Refactored CyberSource REST API samples with security improvements"
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 6: Add GitHub Remote

After creating the repository, GitHub will show you commands. Use the HTTPS URL:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Replace:
- `YOUR_USERNAME` with your GitHub username
- `YOUR_REPO_NAME` with your repository name

**Example**:
```bash
git remote add origin https://github.com/johndoe/cybersource-rest-samples-python-refactor.git
```

### Step 7: Verify Remote

Check that the remote was added correctly:

```bash
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (fetch)
origin  https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git (push)
```

### Step 8: Push to GitHub

Push your code to GitHub:

```bash
git branch -M main
git push -u origin main
```

**Note**: If you're using a Personal Access Token, you'll be prompted for:
- **Username**: Your GitHub username
- **Password**: Your Personal Access Token (not your GitHub password)

### Step 9: Verify on GitHub

1. Go to your repository on GitHub
2. You should see all your files
3. Verify that `.env` and other sensitive files are **NOT** visible

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

**Option 2: Use SSH**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Then use SSH URL instead:
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

### "Repository not found" Error

- Check that the repository name and username are correct
- Verify you have access to the repository
- Make sure the repository exists on GitHub

### "Permission denied" Error

- Verify your GitHub credentials
- Check that your Personal Access Token has `repo` scope
- Try using SSH instead of HTTPS

## Quick Reference Commands

```bash
# Initialize repository
git init

# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Add remote (first time only)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main

# Future updates
git add .
git commit -m "Update description"
git push
```

## Security Checklist

Before pushing, ensure:

- [ ] `.env` file is in `.gitignore`
- [ ] No API keys or secrets in code files
- [ ] No `.p12` certificate files committed
- [ ] No hardcoded credentials in source code
- [ ] Sensitive data is in environment variables only

## Next Steps

After pushing to GitHub:

1. **Add a README.md** (if you want to update the existing one)
2. **Set up GitHub Actions** for CI/CD (optional)
3. **Add collaborators** if working in a team
4. **Create branches** for feature development
5. **Set up branch protection rules** for main branch

## Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [GitHub Authentication](https://docs.github.com/en/authentication)
- [Git Best Practices](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
