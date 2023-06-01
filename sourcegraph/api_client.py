from utils.graphql_api_client import GraphQLAPIClient
from gql import gql


class SourcegraphAPIClient:
    def __init__(self, sourcegraph_api_url, sourcegraph_token):
        self.api_url = sourcegraph_api_url
        self.auth_header = {'Authorization': f'token {sourcegraph_token}'}

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
        client = GraphQLAPIClient(self.api_url, self.auth_header)
        response = client.execute_query(query, variables)
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
        client = GraphQLAPIClient(self.api_url, self.auth_header)
        response = client.execute_query(query, variables)
        repository = response['repository']
        topics = [key['key'] for key in repository['keyValuePairs']]
        sourcegraph_repo_id = repository['id']
        return topics, sourcegraph_repo_id
    
    def add_repository_topic(self, repo_id, topic_name):
        mutation = gql('''
            mutation AddRepositoryMetadata($repoID: ID!, $topicName: String!) {
                addRepoKeyValuePair(repo: $repoID, key: $topicName){
                    alwaysNil
                }
            }
        ''')
        variables = {'repoID': repo_id, 'topicName': topic_name}
        client = GraphQLAPIClient(self.api_url, self.auth_header)
        client.execute_query(mutation, variables)
