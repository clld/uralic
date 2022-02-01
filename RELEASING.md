# Releasing clld/uralic

* data is located at [cldf-datasets/uratyp](https://github.com/cldf-datasets/uratyp).  

* create the database (with data repo in `./uratyp/`)
  ```
  clld initdb --cldf ../uratyp/cldf/StructureDataset-metadata.json --glottolog ~/projects/glottolog/glottolog development.ini
  ```

* run tests
  ```
  pytest
  ```

* deploy
  ```
  (appconfig)$ fab deploy:production
  ```
