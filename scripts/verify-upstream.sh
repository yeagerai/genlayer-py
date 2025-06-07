#!/bin/bash
set -euo pipefail

# Script to verify upstream branch has not changed
# This ensures we're releasing from the expected commit

WORKFLOW_SHA="${1:-$GITHUB_SHA}"

if [ -z "$WORKFLOW_SHA" ]; then
    echo "::error::Workflow SHA not provided and GITHUB_SHA not set"
    exit 1
fi

echo "Verifying upstream has not changed from SHA: $WORKFLOW_SHA"

# Force release branch to be at workflow sha
echo "Resetting to workflow SHA..."
git reset --hard "$WORKFLOW_SHA"

# Determine upstream branch name
UPSTREAM_BRANCH_NAME="$(git rev-parse --abbrev-ref @{upstream} 2>/dev/null || git rev-parse --abbrev-ref origin/$(git rev-parse --abbrev-ref HEAD) 2>/dev/null)"

echo "Upstream branch name: $UPSTREAM_BRANCH_NAME"

if [ -z "$UPSTREAM_BRANCH_NAME" ]; then
    echo "::error::Unable to determine upstream branch name!"
    echo "::error::This may indicate the branch is not tracking an upstream remote"
    echo "::error::Current git status:"
    git status -sb | head -n 1 || echo "::error::Failed to get git status"
    exit 1
fi

# Extract remote name for better error handling
REMOTE_NAME="${UPSTREAM_BRANCH_NAME%%/*}"
echo "Remote name: $REMOTE_NAME"

# Fetch upstream with enhanced error handling
echo "Fetching upstream from remote '$REMOTE_NAME'..."
if ! git fetch "$REMOTE_NAME" 2>&1; then
    echo "::error::Failed to fetch from remote '$REMOTE_NAME'"
    echo "::error::This could be due to:"
    echo "::error::  - Network connectivity issues"
    echo "::error::  - Authentication problems"
    echo "::error::  - Remote repository access issues"
    echo "::error::  - Invalid remote configuration"
    echo "::error::Available remotes:"
    git remote -v || echo "::error::Failed to list remotes"
    exit 1
fi

# Verify upstream branch SHA with enhanced error handling
echo "Resolving upstream branch SHA..."
if ! UPSTREAM_SHA="$(git rev-parse "$UPSTREAM_BRANCH_NAME" 2>/dev/null)"; then
    echo "::error::Unable to determine upstream branch SHA for '$UPSTREAM_BRANCH_NAME'"
    echo "::error::This could indicate:"
    echo "::error::  - The upstream branch does not exist"
    echo "::error::  - The branch reference is invalid"
    echo "::error::  - Recent changes to the upstream repository structure"
    echo "::error::Available remote branches:"
    git branch -r | grep "^[[:space:]]*$REMOTE_NAME/" || echo "::error::No remote branches found for '$REMOTE_NAME'"
    exit 1
fi

# Validate SHA format
if ! echo "$UPSTREAM_SHA" | grep -qE '^[a-f0-9]{40}$'; then
    echo "::error::Invalid SHA format received: '$UPSTREAM_SHA'"
    echo "::error::Expected 40-character hexadecimal string"
    exit 1
fi

HEAD_SHA="$(git rev-parse HEAD)"

echo "HEAD SHA: $HEAD_SHA"
echo "UPSTREAM SHA: $UPSTREAM_SHA"

if [ "$HEAD_SHA" != "$UPSTREAM_SHA" ]; then
    echo "::error::[HEAD SHA] $HEAD_SHA != $UPSTREAM_SHA [UPSTREAM SHA]"
    echo "::error::Upstream has changed, aborting release..."
    echo "::error::This means new commits have been pushed to '$UPSTREAM_BRANCH_NAME' since this workflow started"
    echo "::error::Please restart the release workflow to include the latest changes"
    
    # Show the commits that differ
    echo "::error::Commits in upstream not in HEAD:"
    if ! git log --oneline "$HEAD_SHA..$UPSTREAM_SHA" 2>/dev/null; then
        echo "::error::Unable to show commit differences"
    fi
    exit 1
fi

echo "✅ Verified upstream branch has not changed, continuing with release..." 