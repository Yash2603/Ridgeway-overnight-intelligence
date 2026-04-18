# GitHub Push Guide

This workspace does not currently have:

- a GitHub remote configured
- a local `git user.name`
- a local `git user.email`

Because of that, the repository is ready to push, but cannot be pushed automatically until those are supplied.

## One-time setup

```powershell
git config user.name "Your Name"
git config user.email "you@example.com"
```

## Connect a new GitHub repo

Create an empty GitHub repo first, then run:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

## First push

```powershell
git add .
git commit -m "Build Ridgeway overnight intelligence submission"
git push -u origin main
```

## If you prefer SSH

```powershell
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Recommended repo contents for submission

- source code
- `README.md`
- `docs/ASSIGNMENT_WRITEUP.md`
- `docs/DEMO_SCRIPT.md`
- `docs/DEPLOYMENT.md`
- `docs/OPENAI_INTEGRATION.md`

## After push

Use the repository URL in your assignment submission along with:

- deployed frontend URL
- deployed backend URL
- deployed MCP URL
- demo video link
