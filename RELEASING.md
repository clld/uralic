# Releasing clld/uralic


```shell
git clone --branch v2.0 --depth 1 https://github.com/cldf-datasets/uratyp
git clone --branch v3.0 --depth 1 https://github.com/glottography/rantanen2021uralic
git clone --branch v1.0.1 --depth 1 https://github.com/glottography/asher2007world
git clone --branch v5.3 --depth 1 https://github.com/glottolog/glottolog
git clone https://github.com/clld/uralic
cd uralic
pip install -e .[test]
```

Re-create the database:
```shell
clld initdb --cldf ../uratyp/cldf/StructureDataset-metadata.json --glottolog ../glottolog development.ini
```

Run tests
```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 uralic > uralic.sql.gz
```

