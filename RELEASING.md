# Releasing clld/uralic


```shell
git clone https://github.com/clld/uralic
cd uralic
pip install -e .[test]
```

Clone the data repositories
```shell
cd ..
git clone --depth 1 https://github.com/cldf-datasets/uratyp
git clone --depth 1 https://github.com/glottography/rantanen2021uralic
git clone --depth 1 https://github.com/glottography/asher2007world
cd uralic
```

Re-create the database:
```shell
clld initdb --cldf ../uratyp/cldf/StructureDataset-metadata.json --glottolog ~/projects/glottolog/glottolog development.ini
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
pg_dump -xO uralic > uralic.sql
zip uralic.sql.zip uralic.sql
rm uralic.sql
```

