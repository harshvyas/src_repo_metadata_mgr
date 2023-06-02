from utils.graphql_api_client import GraphQLAPIClient
from gql import gql

class SourcegraphAPIClient:
    def __init__(self, sourcegraph_api_url, sourcegraph_token):
        self.api_url = sourcegraph_api_url
        self.auth_header = {'Authorization': f'token {sourcegraph_token}'}
        self.graphql_client = GraphQLAPIClient(self.api_url, self.auth_header)

    def get_repositories(self, batchSize):
        query = gql('''
            query getRepositories($batchSize: Int!){
                repositories(first: $batchSize){
                    nodes {
                        url
                        externalRepository {
                            serviceType
                        }
                    }
                }
            }
        ''')
        variables = {"batchSize": batchSize}
        response = self.graphql_client.execute_query(query, variables)
        return response
    
    def get_github_repositories(self,batchSize):
        repository_nodes = self.get_repositories(batchSize)['repositories']['nodes']
        github_repositories = [node['url'] for node in repository_nodes if node['externalRepository']['serviceType'] == 'github']
        return github_repositories

    def fetch_repository_metadata(self, code_host_name, owner_name, repository_name):
        query = gql('''
            query GetRepositoryMetadata($repositoryName: String!) {
                repository(name: $repositoryName) {
                    name
                    description
                    id
                    url
                    keyValuePairs {
                        key
                    }
                }
            }
        ''')

        repository_name = f"{code_host_name}/{owner_name}/{repository_name}"
        variables = {'repositoryName': repository_name}
        response = self.graphql_client.execute_query(query, variables)
        repository = response['repository']
        topics = [key['key'] for key in repository['keyValuePairs']]
        sourcegraph_repo_id = repository['id']
        return topics, sourcegraph_repo_id
    
    # Seems the src-cli still uses add-kvp instead of add-metadata. 
    # sourcegraph.com instance says addRepoKeyValuePair is going to be deprecated in favor of repo.metadata
    # however sourcegraph app still uses addRepoKeyValuePair
    # TODO review in future what is the standardized api for now using addRepoKeyValuePair as it works across both sourcegraph.com and sourcegraph app
    def add_repository_topic(self, repo_id, repo_metadata_key, repo_metadata_value):
        mutation = gql('''
            mutation addRepoKeyValuePair($repoID: ID!, $repo_metadata_key: String!) {
                addRepoKeyValuePair(repo: $repoID, key: $repo_metadata_key, value: null){
                    alwaysNil
                }
            }
        ''')
        variables = {'repoID': repo_id, 'repo_metadata_key': repo_metadata_key}
        self.graphql_client.execute_query(mutation, variables)
