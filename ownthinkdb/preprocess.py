# vi: set ft=python sts=4 ts=4 sw=4 et:

import time
from neo4j import GraphDatabase


def conn2db(uri='bolt://192.168.16.218:7687', user_name='neo4j', pwd='neo4j'):
    """Connect to neo4j database."""
    driver = GraphDatabase.driver(uri=uri, auth=(user_name, pwd))
    return driver.session()

def get_all_entities():
    """Get all entities from KB."""
    session = conn2db()
    begintime = time.time()
    #query = 'MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN collect(distinct n)'
    query = 'MATCH (n) RETURN n'
    ret = session.run(query)
    endtime = time.time()
    print('The query time is %.2f'%(endtime-begintime))

    with open('entities.txt', 'w') as f:
        for rec in ret:
            n = rec['n']['name']
            #if isinstance(n, str) and n[0]=='<':
            #    f.write(n[1:-1]+'\n')
            if isinstance(n, str):
                f.write(n+'\n')
            else:
                print(rec)


if __name__ == '__main__':
    #session = conn2db()
    #begintime = time.time()
    #query = 'MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN count(n.name) + count(r)'
    #ret = session.run(query)
    #endtime = time.time()
    #print('The query time is %.2f'%(endtime-begintime))
    #for rec in ret:
    #    print(rec['n']['name'])
    get_all_entities()

