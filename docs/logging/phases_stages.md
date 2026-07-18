# Phases & Stages

Execution hierarchy of the ETL system:

`PIPELINE → PHASE → STAGE`

A `PIPELINE` is the full workflow. 
Each pipeline is divided into `PHASES`, and each phase contains multiple `STAGES` that perform specific tasks.

---

## Overview

- [`ETL`](../../data_pipeline/main.py)

  - [`EXTRACT`](../../data_pipeline/extract.py)
    - [`FETCH_WORKS`](../../etl/extract/fetch_works.py)
    - [`EXPORT_KEYS`](../../etl/extract/export_keys.py)
    - [`FETCH_WORKS_AUTHORS_SERIES`](../../etl/extract/fetch_works_authors_series.py)
    - [`EXPORT_AUTHOR_KEY_NAMES`](../../etl/extract/export_author_key_names.py)
    - [`FETCH_BOOKS_VIA_WORK_KEY`](../../etl/extract/fetch_books_via_work_key.py)
    - [`EXPORT_PUBLISHERS_SUBJECTS_PEOPLE_TIMES`](../../etl/extract/export_publishers_subjects_people_times.py)
    - [`FETCH_AUTHOR_STATISTICS`](../../etl/extract/fetch_author_statistics.py)
    - [`FETCH_WORKS_RATINGS`](../../etl/extract/fetch_works_ratings.py)
    
  - [`TRANSFORM`](../../data_pipeline/transform.py)
    - [`TRANSFORM_TO_AUTHORS_TABLES`](../../etl/transform/author_tables.py)
    - [`TRANSFORM_TO_EDITIONS_TABLES`](../../etl/transform/editions_tables.py)
    - [`TRANSFORM_TO_WORKS_TABLES`](../../etl/transform/works_tables.py)
    
  - [`LOAD`](../../data_pipeline/load.py)
    - [`CREATE_DATABASE`](../../etl/load/create_database.py)
    - [`CREATE_TABLES_AT_DATABASE`](../../etl/load/create_tables.py)
    - [`LOAD_TABLES_AT_DATABASE`](../../etl/load/load_tables.py)
    - [`CREATE_INDEXES_AT_DATABASE`](../../etl/load/create_indexes.py)

---

## Details

### `ETL`

| Phase       | Description                                                   |
|-------------|---------------------------------------------------------------|
| `EXTRACT`   | Retrieve raw metadata from the Open Library API               |
| `TRANSFORM` | Convert raw API responses into structured relational datasets |
| `LOAD`      | Load data into a relational database schema                   |

---

### `EXTRACT`

| Stage                                     | Description                                                                                                                                                                                                                                 |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FETCH_WORKS`                             | Retrieve work records (endpoint: [`SEARCH`](../open_library_api/entrypoints.md#search))                                                                                                                                                                  |
| `EXPORT_KEYS`                             | Export entity keys for downstream extraction                                                                                                                                                                                                |
| `FETCH_WORKS_AUTHORS_SERIES`              | Retrieve work, author, and series metadata (endpoint: [`WORKS`](../open_library_api/entrypoints.md#works), [`AUTHORS`](../open_library_api/entrypoints.md#authors-1), [`SERIES`](../open_library_api/entrypoints.md#series-1) via [`GET_MANY`](../open_library_api/entrypoints.md#get_many))    |
| `EXPORT_AUTHOR_KEY_NAMES`                 | Export author identifiers and names (endpoint: redirection via [`AUTHORS`](../open_library_api/entrypoints.md#authors-1))                                                                                                                                |
| `FETCH_BOOKS_VIA_WORK_KEY`                | Retrieve edition records for works (endpoint: [`SEARCH_EDITIONS_VIA_WORK_KEY`](../open_library_api/entrypoints.md#search_editions_via_work_key))                                                                                                         |
| `EXPORT_PUBLISHERS_SUBJECTS_PEOPLE_TIMES` | Export dimension entities from extracted records                                                                                                                                                                                            |
| `FETCH_AUTHOR_STATISTICS`                 | Retrieve author statistics  (endpoint: [`SEARCH_AUTHORS`](../open_library_api/entrypoints.md#search_authors))                                                                                                                                            |
| `FETCH_WORKS_RATINGS`                     | Retrieve work ratings (endpoint: [`WORKS_RATINGS`](../open_library_api/entrypoints.md#works_ratings))                                                                                                                                                    |

---

### `TRANSFORM`

| Stage                          | Description               | Tables                                                                                                                |
|--------------------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `TRANSFORM_TO_AUTHORS_TABLES`  | Build authors' tables     | `authors`, `authors_alternative_names`, `authors_statistics`, `authors_works`                                         |
| `TRANSFORM_TO_EDITIONS_TABLES` | Build editions' tables    | `editions`, `editions_contributors`, `editions_publishing`, `editions_details`                                        |
| `TRANSFORM_TO_WORKS_TABLES`    | Build works' tables       | `works`, `works_series`, `works_availability`, `works_subjects`, `works_people`, `works_places`, `works_time_periods` |

---

### `LOAD` 

| Stage                        | Description                                  |
|------------------------------|----------------------------------------------|
| `CREATE_DATABASE`            | Create target database                       |
| `CREATE_TABLES_AT_DATABASE`  | Create database schema                       |
| `LOAD_TABLES_AT_DATABASE`    | Load data into database tables               |
| `CREATE_INDEXES_AT_DATABASE` | Create database indexes (filter and trigram) |
