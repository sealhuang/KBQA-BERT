# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import csv


def collect_relations(file_name='ownthink_v2.csv'):
    """Get all unique relations."""
    rel_dict = {}

    # output relation file
    csvf_relation = open("relation_dict.csv", "w", newline='', encoding='utf-8')
    w_relation = csv.writer(csvf_relation)
    w_relation.writerow(("name", "count"))

    # load data
    with open(file_name, encoding='utf-8') as csv_info:
        # pop out the header row
        csv_info.readline()
        csv_reader = csv.reader(x.replace('\0', '') for x in csv_info)
        for line in csv_reader:
            tmp = [item.strip() for item in line]
            _tmp = [item for item in tmp if item]
            if not len(_tmp)==3:
                print(tmp)
                continue
            rel = tmp[1]
            if not rel in rel_dict:
                rel_dict[rel] = 1
            else:
                rel_dict[rel] += 1

    # save file
    for r in rel_dict:
        w_relation.writerow((r, rel_dict[r]))
    csvf_relation.close()

def collect_mentions(file_name='ownthink_v2.csv'):
    """Get all unique mentions."""
    mention_dict = {}

    # output file
    csvf = open("mention_dict.csv", "w", newline='', encoding='utf-8')
    writer = csv.writer(csvf)
    writer.writerow(("entity", "mention"))

    # load data
    with open(file_name, encoding='utf-8') as csv_info:
        # pop out the header row
        csv_info.readline()
        csv_reader = csv.reader(x.replace('\0', '') for x in csv_info)
        for line in csv_reader:
            tmp = [item.strip() for item in line]
            _tmp = [item for item in tmp if item]
            if not len(_tmp)==3:
                print(tmp)
                continue
            rel = tmp[1]
            if rel=='歧义关系':
                if not tmp[2] in mention_dict:
                    mention_dict[tmp[2]] = [tmp[0]]
                elif tmp[0] in mention_dict[tmp[2]]:
                    print('%s-%s has been detected'%(tmp[0], tmp[2]))
                else:
                    mention_dict[tmp[2]].append(tmp[0])

    # save file
    for e in mention_dict:
        s = [e]
        for item in mention_dict[e]:
            s.append(item)
        writer.writerow(tuple(s))
    csvf.close()

def check_entity_exists():
    """Check the existence of the entity in the mention-entity pairs."""
    # get all entities which have mentions
    entities = []
    with open('mention_dict.csv', encoding='utf-8') as csv_info:
        # pop out the header row
        csv_info.readline()
        csv_reader = csv.reader(csv_info)
        for line in csv_reader:
            tmp = [item.strip() for item in line]
            entities.append(tmp[0])

    # check the existence of the entity in triples
    with open('./ownthink_v2.csv', encoding='utf-8') as csv_info:
        # pop out the header row
        csv_info.readline()
        csv_reader = csv.reader(x.replace('\0', '') for x in csv_info)
        for line in csv_reader:
            tmp = [item.strip() for item in line]
            _tmp = [item for item in tmp if item]
            if not len(_tmp)==3:
                #print(tmp)
                continue
            if not tmp[1]=='歧义关系' and not tmp[0] in entities:
                print(tmp)

def prepare4neo4j(file_name='ownthink_v2.csv'):
    """Encode each triple in text into neo4j-required format."""
    # entity dict
    entity_dict = {}
    entity_count = 0

    # mention dict
    mention_dict = {}
    mention_count = 0

    # property dict
    property_dict = {}
    property_count = 0

    # output entity file
    csvf_entity = open("entity.csv", "w", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    w_entity.writerow(("entity:ID", "name", ":LABEL"))

    # output relation file
    csvf_relation = open("relation.csv", "w", newline='', encoding='utf-8')
    w_relation = csv.writer(csvf_relation)
    w_relation.writerow((":START_ID", "name", ":END_ID", ":TYPE"))

    # load data
    with open(file_name, 'r', encoding='utf-8') as csv_info:
        # pop out the header row
        csv_info.readline()
        csv_reader = csv.reader(x.replace('\0', '') for x in csv_info)
        for line in csv_reader:
            tmp = [item.strip().replace('\n', ' ') for item in line]
            _tmp = [item for item in tmp if item]
            if not len(_tmp)==3:
                print(tmp)
                continue
            n1 = tmp[0]
            rel = tmp[1]
            n2 = tmp[2]
            if rel=='歧义关系':
                if not n2 in entity_dict:
                    entity_count += 1
                    entity_dict[n2] = 'e'+str(entity_count)
                if not n1 in mention_dict:
                    mention_count += 1
                    mention_dict[n1] = 'm'+str(mention_count)
                w_relation.writerow((
                    mention_dict[n1],
                    rel,
                    entity_dict[n2],
                    "MENTION",
                ))
            else:
                if not n1 in entity_dict:
                    entity_count += 1
                    entity_dict[n1] = 'e'+str(entity_count)
                if not n2 in property_dict:
                    property_count += 1
                    property_dict[n2] = 'p'+str(property_count)
                w_relation.writerow((
                    entity_dict[n1],
                    rel,
                    property_dict[n2],
                    'RELATION',
                ))

    # save relations
    csvf_relation.close()

    # save entities and mentions
    for e in entity_dict:
        w_entity.writerow((entity_dict[e], e, "ENTITY"))
    for m in mention_dict:
        w_entity.writerow((mention_dict[m], m, "MENTION"))
    for p in property_dict:
        w_entity.writerow((property_dict[p], p, "PROPERTY"))
    csvf_entity.close()


if __name__ == '__main__':
    #collect_relations()
    #collect_mentions()
    #check_entity_exists()
    prepare4neo4j()

