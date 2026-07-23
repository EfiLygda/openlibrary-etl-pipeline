# Pipelines, Phases & Stages
Execution hierarchy of the application workflows:

`APPLICATION → PIPELINE → <PHASE> → STAGE`

A `PIPELINE` represents a complete workflow within the application.

A pipeline may be divided into logical `PHASES`, where each phase groups related stages together.  

A `STAGE` is the smallest execution unit and represents a specific task or operation.


> **Note**: `PHASES` are optional since simple pipelines can execute directly as `PIPELINE → STAGE`.

---

## Overview

- [`SETUP_PROJECT`](../../setup/setup_project.py)

  - [`SETUP_DIRECTORIES`](../../setup/create_directories.py)
  - [`RESET_DATABASE`](../../setup/reset_database.py)


- [`ETL`](../../data_pipeline/pipeline.py)

  - [`EXTRACT`](../../data_pipeline/extract.py)
    - [`FETCH_WORKS`](../../data_pipeline/etl/extract/fetch_works.py)
    - [`EXPORT_KEYS`](../../data_pipeline/etl/extract/export_keys.py)
    - [`FETCH_WORKS_AUTHORS_SERIES`](../../data_pipeline/etl/extract/fetch_works_authors_series.py)
    - [`EXPORT_AUTHOR_KEY_NAMES`](../../data_pipeline/etl/extract/export_author_key_names.py)
    - [`FETCH_BOOKS_VIA_WORK_KEY`](../../data_pipeline/etl/extract/fetch_books_via_work_key.py)
    - [`EXPORT_PUBLISHERS_SUBJECTS_PEOPLE_TIMES`](../../data_pipeline/etl/extract/export_publishers_subjects_people_times.py)
    - [`FETCH_AUTHOR_STATISTICS`](../../data_pipeline/etl/extract/fetch_author_statistics.py)
    - [`FETCH_WORKS_RATINGS`](../../data_pipeline/etl/extract/fetch_works_ratings.py)
    
  - [`TRANSFORM`](../../data_pipeline/transform.py)
    - [`TRANSFORM_TO_AUTHORS_TABLES`](../../data_pipeline/etl/transform/author_tables.py)
    - [`TRANSFORM_TO_EDITIONS_TABLES`](../../data_pipeline/etl/transform/editions_tables.py)
    - [`TRANSFORM_TO_WORKS_TABLES`](../../data_pipeline/etl/transform/works_tables.py)
    
  - [`LOAD`](../../data_pipeline/load.py)
    - [`CREATE_DATABASE`](../../data_pipeline/etl/load/create_database.py)
    - [`CREATE_ETL_SCHEMA`](../../data_pipeline/etl/load/create_schema.py)
    - [`CREATE_ETL_TABLES`](../../data_pipeline/etl/load/create_tables.py)
    - [`LOAD_ETL_TABLES`](../../data_pipeline/etl/load/load_tables.py)
    - [`CREATE_ETL_INDEXES`](../../data_pipeline/etl/load/create_indexes.py)


- [`SIMULATE_LIBRARY`](../../library/library_simulation.py)

  - [`RESET_KAFKA_TOPIC`](../../library/setup/reset_kafka_topic.py)
  - [`CREATE_LIBRARY_SCHEMA`](../../library/setup/create_schema.py)
  - [`CREATE_LIBRARY_TABLES`](../../library/setup/create_tables.py)
  - [`INITIALIZE_REDIS_STATE`](../../library/setup/init_redis_state.py)
  - [`SIMULATE_EVENTS`](../../library/setup/start_library.py)
  
    - [`PRODUCE_EVENTS`](../../library/producer/producer.py)
    - [`SYSTEM_CONSUMER`](../../library/consumers/system/consumer.py)
---

## Details

### `SETUP_PROJECT`

| Stage               | Description                                                                  |
|---------------------|------------------------------------------------------------------------------|
| `SETUP_DIRECTORIES` | Create the required project directory structure if it does not already exist |
| `RESET_DATABASE`    | Remove existing library database objects to provide a clean starting state   |

---

### `ETL`

| Phase       | Description                                                   |
|-------------|---------------------------------------------------------------|
| `EXTRACT`   | Retrieve raw metadata from the Open Library API               |
| `TRANSFORM` | Convert raw API responses into structured relational datasets |
| `LOAD`      | Load data into a relational database schema                   |

---

#### `EXTRACT`

| Stage                                     | Description                                                                                                                                                                                                                                                                                  |
|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `FETCH_WORKS`                             | Retrieve work records (endpoint: [`SEARCH`](../open_library_api/entrypoints.md#search))                                                                                                                                                                                                      |
| `EXPORT_KEYS`                             | Export entity keys for downstream extraction                                                                                                                                                                                                                                                 |
| `FETCH_WORKS_AUTHORS_SERIES`              | Retrieve work, author, and series metadata (endpoint: [`WORKS`](../open_library_api/entrypoints.md#works), [`AUTHORS`](../open_library_api/entrypoints.md#authors-1), [`SERIES`](../open_library_api/entrypoints.md#series-1) via [`GET_MANY`](../open_library_api/entrypoints.md#get_many)) |
| `EXPORT_AUTHOR_KEY_NAMES`                 | Export author identifiers and names (endpoint: redirection via [`AUTHORS`](../open_library_api/entrypoints.md#authors-1))                                                                                                                                                                    |
| `FETCH_BOOKS_VIA_WORK_KEY`                | Retrieve edition records for works (endpoint: [`SEARCH_EDITIONS_VIA_WORK_KEY`](../open_library_api/entrypoints.md#search_editions_via_work_key))                                                                                                                                             |
| `EXPORT_PUBLISHERS_SUBJECTS_PEOPLE_TIMES` | Export dimension entities from extracted records                                                                                                                                                                                                                                             |
| `FETCH_AUTHOR_STATISTICS`                 | Retrieve author statistics  (endpoint: [`SEARCH_AUTHORS`](../open_library_api/entrypoints.md#search_authors))                                                                                                                                                                                |
| `FETCH_WORKS_RATINGS`                     | Retrieve work ratings (endpoint: [`WORKS_RATINGS`](../open_library_api/entrypoints.md#works_ratings))                                                                                                                                                                                        |

---

#### `TRANSFORM`

| Stage                          | Description               | Tables                                                                                                                |
|--------------------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `TRANSFORM_TO_AUTHORS_TABLES`  | Build authors' tables     | `authors`, `authors_alternative_names`, `authors_statistics`, `authors_works`                                         |
| `TRANSFORM_TO_EDITIONS_TABLES` | Build editions' tables    | `editions`, `editions_contributors`, `editions_publishing`, `editions_details`                                        |
| `TRANSFORM_TO_WORKS_TABLES`    | Build works' tables       | `works`, `works_series`, `works_availability`, `works_subjects`, `works_people`, `works_places`, `works_time_periods` |

---

#### `LOAD` 

| Stage                | Description                                            |
|----------------------|--------------------------------------------------------|
| `CREATE_DATABASE`    | Create the target database                             |
| `CREATE_ETL_SCHEMA`  | Create the schema used by the ETL pipeline (`catalog`) |
| `CREATE_ETL_TABLES`  | Create relational tables required by the ETL schema    |
| `LOAD_ETL_TABLES`    | Load transformed datasets into ETL tables              |
| `CREATE_ETL_INDEXES` | Create database indexes for query optimization         |

---

### `SIMULATE_LIBRARY`

| Stage                    | Description                                                  |
|--------------------------|--------------------------------------------------------------|
| `RESET_KAFKA_TOPIC`      | Remove and recreate the Kafka topic used for library events  |
| `CREATE_LIBRARY_SCHEMA`  | Create the schema used by the library simulation (`library`) |
| `CREATE_LIBRARY_TABLES`  | Create relational tables required by the library schema      |
| `INITIALIZE_REDIS_STATE` | Build and store the initial simulation state in Redis        |
| `SIMULATE_EVENTS`        | Execute the producer and consumers event workflow            |

#### `SIMULATE_EVENTS`

| Stage             | Description                                                                                        |
|-------------------|----------------------------------------------------------------------------------------------------|
| `PRODUCE_EVENTS`  | Generate, validate, and publish accepted library events to Kafka                                   |
| `SYSTEM_CONSUMER` | Consume Kafka events, update Redis live state, and persist changes to the library system database. |
