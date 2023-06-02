from utils.graphql_api_client import GraphQLAPIClient
from gql import gql

class GitHubAPIClient:
    def __init__(self, github_url, github_token):
        self.api_url = github_url
        self.auth_header = {'Authorization': f'Bearer {github_token}'}
        self.graphql_client = GraphQLAPIClient(self.api_url, self.auth_header)

    def fetch_repository_metadata(self, owner_name, repository_name, query_file):
        with open(query_file, 'r') as file:
            query = gql(file.read())
        variables = {'ownerName': owner_name, 'repositoryName': repository_name}
        response = self.graphql_client.execute_query(query, variables)
        return response