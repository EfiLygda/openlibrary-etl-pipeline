# Events

## Event Name Structure

The logging system is divided into four independent event families. 

Each family defines its own naming rules depending on the type of operation being tracked (execution flow, data processing, system operations, or data integrity).

All events follow structured naming conventions to ensure consistency, traceability, and easy log filtering.

---

## Table of Contents

<!-- TOC -->
* [Events](#events)
  * [Event Name Structure](#event-name-structure)
  * [Table of Contents](#table-of-contents)
  * [1. Pipeline Lifecycle Events](#1-pipeline-lifecycle-events)
  * [2. Entrypoint-based Data Processing Events](#2-entrypoint-based-data-processing-events)
    * [Attempt-level Execution Events (Retry Layer)](#attempt-level-execution-events-retry-layer)
  * [3. System Events (Database/Table Layer)](#3-system-events-databasetable-layer)
  * [4. Validation & Data Integrity Events](#4-validation--data-integrity-events)
    * [4.1 Validation results](#41-validation-results)
    * [4.2 Data integrity issues](#42-data-integrity-issues)
  * [5. Partial Failures (Extraction/Validation Issues)](#5-partial-failures-extractionvalidation-issues)
<!-- TOC -->

---

## 1. Pipeline Lifecycle Events

Used to track the execution flow of the ETL pipeline.

#### Naming convention
`<LEVEL>_<LIFECYCLE_EVENT>`

- `LEVEL`: execution level (`PIPELINE`, `PHASE`, `STAGE`)
- `LIFECYCLE_EVENT`: lifecycle event (`START`, `COMPLETE`)

#### Events

| Event | Description | Log Level |
|------|-------------|-----------|
| `PIPELINE_START` | Pipeline execution starts | `INFO` |
| `PIPELINE_COMPLETE` | Pipeline execution completes successfully | `INFO` |
| `PHASE_START` | A pipeline phase begins execution | `INFO` |
| `PHASE_COMPLETE` | A pipeline phase completes successfully | `INFO` |
| `STAGE_START` | A pipeline stage begins execution | `INFO` |
| `STAGE_COMPLETE` | A pipeline stage completes successfully | `INFO` |

---

## 2. Entrypoint-based Data Processing Events

Used for operations originating from API entrypoints or data retrieval steps such as search, batch fetching, and redirection.

#### Naming convention
`<ENTRYPOINT>[_GET_MANY]_<STATUS>`

- `ENTRYPOINT`: the originating operation (see [`entrypoints.md`](../open_library_api/entrypoints.md))
- `GET_MANY`: optional batching mode for bulk operations
- `STATUS`: `SUCCESS` or `FAILED`

#### Events

| Event                         | Description                                         | Log Level   | Key Fields                                                |
|-------------------------------|-----------------------------------------------------|-------------|-----------------------------------------------------------|
| `SEARCH_AUTHORS_SUCCESS`      | Author search completes successfully                | `INFO`      | `author`, `file`, `attempt`, `duration`                   |
| `SEARCH_AUTHORS_FAILED`       | Author search fails                                 | `ERROR`     | `author`, `file`, `attempt`, `error_type`, `duration`     |
| `AUTHORS_GET_MANY_SUCCESS`    | Batch retrieval of authors completes successfully   | `INFO`      | `batch`, `file`, `attempt`, `duration`                    |
| `AUTHORS_GET_MANY_FAILED`     | Batch retrieval of authors fails                    | `ERROR`     | `batch`, `file`, `attempt`, `error_type`, `duration`      |
| `WORKS_GET_MANY_SUCCESS`      | Batch retrieval of works completes successfully     | `INFO`      | `batch`, `file`, `attempt`, `duration`                    |
| `WORKS_GET_MANY_FAILED`       | Batch retrieval of works fails                      | `ERROR`     | `batch`, `file`, `attempt`, `error_type`, `duration`      |
| `BOOKS_GET_MANY_SUCCESS`      | Batch retrieval of books completes successfully     | `INFO`      | `batch`, `file`, `attempt`, `duration`                    |
| `BOOKS_GET_MANY_FAILED`       | Batch retrieval of books fails                      | `ERROR`     | `batch`, `file`, `attempt`, `error_type`, `duration`      |
| `WORKS_RATINGS_SUCCESS`       | Ratings retrieval for a work completes successfully | `INFO`      | `work`, `file`, `attempt`, `duration`                     |
| `WORKS_RATINGS_FAILED`        | Ratings retrieval for a work fails                  | `ERROR`     | `work`, `file`, `attempt`, `error_type`, `duration`       |
| `AUTHORS_REDIRECTION_SUCCESS` | Author redirection completes successfully           | `INFO`      | `from`, `to`, `file`, `attempt`, `duration`               |
| `AUTHORS_REDIRECTION_FAILED`  | Author redirection fails during resolution          | `ERROR`     | `from`, `to`, `file`, `attempt`, `error_type`, `duration` |


---

### Attempt-level Execution Events (Retry Layer)

Used for tracking individual retry attempts within an entrypoint operation.  
These events represent transient failures during execution retries and do NOT represent final outcomes.

#### Naming convention
`ATTEMPT_FAILED`

> `ATTEMPT_FAILED` always precedes either a `SUCCESS` or `FAILED` entrypoint event.

#### Events

| Event              | Description                                       | Log Level   | Key Fields              |
|--------------------|---------------------------------------------------|-------------|-------------------------|
| `ATTEMPT_FAILED`   | Single execution attempt failed during retry loop | `DEBUG`     | `attempt`, `error_type` |

#### Error Type Mapping

| Exception | error_type |
|----------|------------|
| `requests.exceptions.ReadTimeout` | `read_timeout` |
| `requests.exceptions.ConnectTimeout` | `connect_timeout` |
| `requests.exceptions.HTTPError` | `http_error` |
| `requests.exceptions.ConnectionError` | `connection_error` |
| `ValueError` | `no_data` |

---

## 3. System Events (Database/Table Layer)

Used for infrastructure-level operations such as database and table lifecycle management.

#### Naming convention
`<SYSTEM>_<ACTION>[_<STATUS>]`

- `SYSTEM`: infrastructure domain (`DATABASE`, `TABLE`)
- `ACTION`: operation performed (`CREATE`, `LOAD`, `EXISTS`)
- `STATUS`: result of operation when applicable (`SUCCESS`)

> **Note**: Some actions such as `EXISTS` represent state checks and do not require a status suffix.

#### Events

| Event                     | Description                        | Log Level  | Key Fields             |
|---------------------------|------------------------------------|------------|------------------------|
| `DATABASE_CREATE_SUCCESS` | A database is created successfully | `INFO`     | `database`             |
| `DATABASE_EXISTS`         | A database already exists          | `INFO`     | `database`             |
| `TABLE_EXISTS`            | A table already exists             | `INFO`     | `table`                |
| `TABLE_CREATE_REQUIRED`   | Table creation is required         | `INFO`     | `table`                |
| `TABLE_CREATE_SUCCESS`    | A table is created successfully    | `INFO`     | `table`                |
| `INDEX_EXISTS`            | Index already exists               | `INFO`     | `table`, `index`       |
| `INDEX_CREATE_REQUIRED`   | Index creation is required         | `INFO`     | `table`, `index`       |
| `INDEXES_CREATE_SUCCESS`  | Indexes are created successfully   | `INFO`     | `table`, `index`       |
| `TABLE_LOAD_SUCCESS`      | Table data is loaded successfully  | `INFO`     | `table`, `rows_loaded` |

---

## 4. Validation & Data Integrity Events

Used for validating correctness and consistency of data during ingestion and transformation.

---

### 4.1 Validation results

Validation checks ensure structural and referential correctness of data before further processing.

#### Naming convention
`<VALIDATION_SCOPE>_VALIDATION_<STATUS>`

- `VALIDATION_SCOPE`: domain or entity being validated (e.g., primary keys, work keys)
- `STATUS`: `SUCCESS` or `FAILED`

#### Events

| Event                                  | Description                                             | Log Level   | Key Fields             |
|----------------------------------------|---------------------------------------------------------|-------------|------------------------|
| `PRIMARY_KEY_VALIDATION_SUCCESS`       | Primary key uniqueness validation passes                | `INFO`      | `table`, `primary_key` |
| `PRIMARY_KEY_VALIDATION_FAILED`        | Primary key validation fails due to duplicates or nulls | `ERROR`     | `table`, `primary_key` |
| `WORKS_KEYS_VALIDATION_SUCCESS`        | Work key validation passes successfully                 | `INFO`      | `table`                |
| `WORKS_KEYS_VALIDATION_FAILED`         | Work key validation fails                               | `ERROR`     | `table`                |
| `AUTHOR_KEYS_VALIDATION_SUCCESS`       | Author key validation passes successfully               | `INFO`      | `table`                |
| `AUTHOR_KEYS_VALIDATION_FAILED`        | Author key validation fails                             | `ERROR`     | `table`                |
| `EDITION_KEYS_VALIDATION_SUCCESS`      | Edition key validation passes successfully              | `INFO`      | `table`                |
| `EDITION_KEYS_VALIDATION_FAILED`       | Edition key validation fails                            | `ERROR`     | `table`                |
| `AUTHOR_STATS_KEYS_VALIDATION_SUCCESS` | Author statistics key validation passes successfully    | `INFO`      | `table`                |
| `AUTHOR_STATS_KEYS_VALIDATION_FAILED`  | Author stats validation fails                           | `ERROR`     | `table`                |

---

### 4.2 Data integrity issues

Used when structural or semantic inconsistencies are detected in data.

#### Naming convention
`<ENTITY>_<ISSUE_TYPE>`

- `ENTITY`: domain object being evaluated (e.g., `AUTHOR`, `WORK`)
- `ISSUE_TYPE`: type of issue detected

#### Events

| Event                      | Description                                             | Log Level  | Key Fields                                         |
|----------------------------|---------------------------------------------------------|------------|----------------------------------------------------|
| `AUTHOR_NAME_CONFLICT`     | Multiple conflicting names detected for same author     | `WARNING`  | `author_key`, `old_name`, `new_name`, `resolution` |
| `WORK_DUPLICATE_FOUND`     | Duplicate work record detected                          | `WARNING`  | `work_key`                                         |
| `REDUNDANT_COLUMN_DROPPED` | Duplicate or redundant column removed during processing | `WARNING`  | `column`, `duplicate_of`                           |

---

## 5. Partial Failures (Extraction/Validation Issues)

Used when processing completes but with incomplete, inconsistent, or partially failed results.

#### Naming convention
`<PROCESS>_VALIDATION_<STATUS>`

- `PROCESS`: the operation or pipeline component being executed (e.g., `EDITION_KEYS`, `KEY_TYPE`, `DATABASE`)
- `VALIDATION`: fixed keyword indicating this belongs to partial validation/extraction checks
- `STATUS`: result of the operation (`INCOMPLETE`, `FAILED`, `NOT_FOUND`)

#### Events

| Event                                | Description                                | Log Level  | Key Fields                   |
|--------------------------------------|--------------------------------------------|------------|------------------------------|
| `EDITION_KEYS_EXTRACTION_INCOMPLETE` | Edition key extraction completes partially | `WARNING`  | `work_key`                   |
| `KEY_TYPE_PARSE_FAILED`              | Key file type cannot be determined         | `ERROR`    | `filename`, `expected_types` |
| `DATABASE_NOT_FOUND`                 | Expected database is missing               | `ERROR`    | `database`                   |