# GitHub to Sourcegraph Repo Metadata Synchronizer

The GitHub to Sourcegraph Repository Metadata Synchronizer is a Python script designed to streamline the synchronization of repository metadata from GitHub to Sourcegraph instances. This script utilizes API clients for GitHub and Sourcegraph to retrieve GitHub repository metadata and synchronize it with corresponding Sourcegraph repositories.

With this script, you can effortlessly keep the metadata in your Sourcegraph repositories up to date with changes made in the associated GitHub repositories. It fetches existing metadata from GitHub, such as repository topics and performs a one-way synchronization to ensure consistency between the platforms.

## Problem

![Problem Statement](https://raw.githubusercontent.com/harshvyas/src_repo_metadata_mgr/main/screenshots/problemstatement.png)

## Execution    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/harshvyas/src_repo_metadata_mgr/blob/main/src_repo_metadata_mgr.ipynb)

![Execution](https://raw.githubusercontent.com/harshvyas/src_repo_metadata_mgr/main/screenshots/execution.png)

## Desired Result

![Desired Result](https://raw.githubusercontent.com/harshvyas/src_repo_metadata_mgr/main/screenshots/desiredresult.png)

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
git clone https://github.com/harshvyas/src_repo_metadata_mgr.git
```

2. Navigate to the project directory:

```
cd src_repo_metadata_mgr 
```
3. Install python dependencies

```
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```
python main.py [--sync] [--repos REPOSITORIES]
```

- `--sync` or `-s`: Execute the synchronization (optional).
- `--repos REPOSITORIES` or `-r REPOSITORIES`: Comma-separated list of GitHub repositories to sync. Use the format `ownername/reponame`. For example: `sourcegraph/sourcegraph,sourcegraph/src-cli` (optional).


## Examples

1. Sync all repositories configured in Sourcegraph:

```
python main.py --sync
```

2. Sync specific repositories:

```
python main.py --sync --repos sourcegraph/sourcegraph,sourcegraph/src-cli
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please [open an issue](https://github.com/your-username/your-repository/issues) or submit a pull request.

## Acknowledgements

- [GitHub API](https://docs.github.com/en/rest)
- [Sourcegraph API](https://docs.sourcegraph.com/api/)