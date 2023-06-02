# GitHub to Sourcegraph Repository Metadata Synchronizer

The GitHub to Sourcegraph Repository Metadata Synchronizer is a Python script designed to streamline the synchronization of metadata from GitHub repositories to Sourcegraph instances. This script utilizes API clients for GitHub and Sourcegraph to retrieve GitHub metadata and synchronize it with corresponding Sourcegraph repositories.

With this script, you can effortlessly keep the metadata in your Sourcegraph repositories up to date with changes made in the associated GitHub repositories. It fetches existing metadata from GitHub, such as labels, descriptions, and other relevant information, and performs a one-way synchronization to ensure consistency between the platforms.

Key features of the GitHub to Sourcegraph Repository Metadata Synchronizer:

- Fetches metadata from GitHub repositories
- Performs one-way synchronization from GitHub to Sourcegraph
- Updates labels, descriptions, and other metadata in Sourcegraph repositories
- Supports synchronization for specific repositories or all repositories configured in Sourcegraph
- Easy integration with API tokens for authentication
- This tool simplifies the process of maintaining consistent metadata across platforms, specifically focusing on synchronizing from GitHub to Sourcegraph. It is ideal for scenarios where you want to ensure that Sourcegraph repositories reflect the most up-to-date metadata available in their corresponding GitHub repositories.

The GitHub to Sourcegraph Repository Metadata Synchronizer is a Python script designed to streamline the synchronization of metadata from GitHub repositories to Sourcegraph instances. This script utilizes API clients for GitHub and Sourcegraph to retrieve GitHub metadata and synchronize it with corresponding Sourcegraph repositories.

## Prerequisites

Before running the script, make sure you have the following:

- API tokens for GitHub and Sourcegraph. Set these tokens as environment variables:
  - `GITHUB_TOKEN` for the GitHub API token
  - `SOURCEGRAPH_TOKEN` for the Sourcegraph API token
- The Sourcegraph instance has the `repository-metadata` feature flag enabled in the `site-admin` settings. This flag allows the synchronization of repository metadata between GitHub and Sourcegraph.
- The user executing the script has the necessary permissions on the Sourcegraph instance to perform mutation queries. These permissions are required to update metadata on Sourcegraph repositories.
- If needed, modify the `github/input-query.gql` file to customize the GitHub repository metadata query. By default, the script syncs topics from GitHub to corresponding keys in Sourcegraph. Adjust the query as per your specific metadata requirements.

## Installation

1. Clone the repository:

```
git clone 
```

2. Navigate to the project directory:




- ensure repository-metadata feature flag is set to true in site-admin
- ensure the user has appropriate permissions on the sourcegraph instance to run mutation queries
- generate sourcegraph and github access tokens
- modify github/input-query.gql if needed based on github repo metadata query - by default it will sync the topics from github to keys in sourcegraph
- run: pip install requirements.txt.
- specify your GITHUB_TOKEN and SOURCEGRAPH_TOKEN as env variables.
- run: python main.py (default preview mode, no sync of metadata)
- run: python main.py --sync (first 10 repos metadata will be synced by default. TODO pagination)
- run: python main.py --sync --repositories <a1/b1,a2/b2,a3/b3> (comma separated owner/repo format)
- validate by running query repo:has.meta(key) - here key is the topic name from the github repo that has now been synced to sourcegraph
