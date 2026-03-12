TASK: Detect relations referencing missing nodes.

Steps:

1. scan relations.csv
2. find to_id values not present in nodes.csv
3. propose placeholder nodes
4. output CSV patch

Node template:

id,label,type,status
plant.example,Example Plant,plant,seed_unverified
