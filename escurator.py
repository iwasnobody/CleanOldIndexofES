from elasticsearch import Elasticsearch
import curator

def lambda_handler(event, context):
    client = Elasticsearch(['http://elasticsearch.ivanyu.tech:80'])
    ilo = curator.IndexList(client)
    if ilo.indices == []:
        print "No indices available in ES"
    else:
        ilo.filter_by_regex(kind='prefix', value='cwl-')
        ilo.filter_by_age(source='creation_date', direction='older', unit='days', unit_count=1)
        if ilo.indices == []:
            print "No matched indices in ES"
        else:
            print "Find matched indices in ES:"
            print ilo.indices
            delete_indices = curator.DeleteIndices(ilo)
            delete_indices.do_action()
    return
