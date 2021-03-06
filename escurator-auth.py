from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import curator
import os
import warnings

warnings.filterwarnings("ignore") #ignore warnings the generated when verify_certs=False

def lambda_handler(event, context):
    host = 'elasticsearch2.XXX.rocks'
    
    awsauth = AWS4Auth(os.environ['AK'], os.environ['SK'], 'us-east-1', 'es')

    client = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=False, #use custom domain name will fail on verify certs
        connection_class=RequestsHttpConnection
    )

    ilo = curator.IndexList(client)
    if ilo.indices == []:
        print "No indices available in ES"
    else:
        ilo.filter_by_regex(kind='prefix', value='cflogs-')
        ilo.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=1)
        if ilo.indices == []:
            print "No matched indices in ES"
        else:
            print "Find matched indices in ES:"
            print ilo.indices
            delete_indices = curator.DeleteIndices(ilo)
            delete_indices.do_action()
    return
