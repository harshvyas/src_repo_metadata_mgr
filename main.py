import os
import click
from github.api_client import GitHubAPIClient
from sourcegraph.api_client import SourcegraphAPIClient
from repository_metadata_manager.metadata_retriever import MetadataRetriever
from repository_metadata_manager.metadata_synchronizer import MetadataSynchronizer

def get_environment_variable(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set.")
    return value

@click.command(help="""
- By default synchronizes the first 10 search results for the string sourcegraph in any public github repository to sourcegraph.
- Passing specific string will narrow synchronization to the first 10 search results in any public github repository to sourcegraph.
- Use --repos owner1/repo1,owner2/repo2 to explicity synchronize specific repos
""")
@click.argument('search_string', default='sourcegraph')
@click.option('--sync','-s', is_flag=True, help='Execute the synchronization')
@click.option('--repos', '-r', help='Comma-separated list of github repositories to sync in format ownername/reponame e.g. sourcegraph/sourcegraph,sourcegraph/src-cli')
def main(search_string, sync, repos):
    try:
        print("...")
        # Retrieve API tokens and owner name from environment variables
        github_token = get_environment_variable('GITHUB_TOKEN')
        github_api_url = 'https://api.github.com/graphql'
        github_query_file = "github/input-query.gql"
        sourcegraph_token = get_environment_variable('SOURCEGRAPH_TOKEN')
        #sourcegraph_api_url = 'http://127.0.0.1:3080/.api/graphql'
        sourcegraph_api_url = 'https://sourcegraph.com/.api/graphql'

        # Create instances of API clients and metadata retrievers
        github_client = GitHubAPIClient(github_api_url, github_token)
        sourcegraph_client = SourcegraphAPIClient(sourcegraph_api_url, sourcegraph_token)

        # Step 2: Fetch GitHub repositories that are configured in Sourcegraph 
        if repos:
            #Specific repos
            sourcegraph_github_repositories = [f"github.com/{repo.strip()}" for repo in repos.split(',')] if ',' in repos else [f"github.com/{repos.strip()}"]
        else:
            search_string = f"repo:github.com/* {search_string} count:10"
            sourcegraph_github_repositories = sourcegraph_client.get_github_repositories(search_string)

        # Loop through each
        for sourcegraph_github_repo in sourcegraph_github_repositories:
            code_host_name, owner_name, repository_name = sourcegraph_github_repo.split("/")
            print(f"For {sourcegraph_github_repo}:")

            # Step 3: Fetch Existing Metadata from GitHub and Sourcegraph
            metadata_retriever = MetadataRetriever(github_client, sourcegraph_client)
            github_data = metadata_retriever.fetch_github_metadata(owner_name, repository_name, github_query_file)
            sourcegraph_data = metadata_retriever.fetch_sourcegraph_metadata(code_host_name, owner_name, repository_name)

            # Step 4: Sync Metadata from GitHub to Sourcegraph
            synchronizer = MetadataSynchronizer(sourcegraph_client)
            synchronizer.sync_metadata(github_data, sourcegraph_data, sync=sync)
            print("-----")
    except Exception as e:
        print('An error occurred:', str(e))

if __name__ == "__main__":
    main()