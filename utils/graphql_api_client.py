from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class GraphQLAPIClient:
    def __init__(self, api_url, auth_header):
        self.api_url = api_url
        self.auth_header = auth_header

    def execute_query(self, query, variables):
        transport = RequestsHTTPTransport(url=self.api_url, headers=self.auth_header)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        response = client.execute(query, variable_values=variables)
        return response
