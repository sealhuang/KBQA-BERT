# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import csv


def prepare4neo4j(file_name='ownthink_v2.csv'):
    """Encode each triple in text into neo4j-required format."""
    # entity dict
    entity_count = 0
    entity_dict = {}
    from_entity_list = []

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
        for line in csv_info:
            tmp = line.strip().split(',')
            tmp = [item.strip() for item in tmp]
            tmp = [item for item in tmp if item]
            if len(tmp)<3 or (tmp[1]==''):
                print(tmp)
                continue
            entity_n = tmp[0]
            entity_b = ','.join(tmp[2:])
            rel = tmp[1]
            if not entity_n in entity_dict:
                entity_count += 1
                entity_dict[entity_n] = 'e'+str(entity_count)
            if not entity_b in entity_dict:
                entity_count += 1
                entity_dict[entity_b] = 'e'+str(entity_count)
            w_relation.writerow((entity_dict[entity_n], rel, entity_dict[entity_b], 'RELATION'))

    csvf_relation.close()

    # save file
    for e in entity_dict:
        w_entity.writerow((entity_dict[e], e, "ENTITY"))
    csvf_entity.close()

