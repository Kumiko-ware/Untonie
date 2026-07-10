import yaml

yaml_db = open('../Music/db.yaml','r')
title_db = yaml.safe_load(yaml_db);

print(title_db)
