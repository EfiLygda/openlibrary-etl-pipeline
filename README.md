# OpenLibrary ETL Pipeline

An end-to-end ETL pipeline that extracts data from the Open Library API, transforms it into structured datasets, and loads it into a relational database using a schema-driven design.

## Table of Contents

<!-- TOC -->
* [OpenLibrary ETL Pipeline](#openlibrary-etl-pipeline)
  * [Table of Contents](#table-of-contents)
  * [Overview](#overview)
    * [Pipeline Steps](#pipeline-steps)
    * [Project Structure](#project-structure)
  * [Tech Stack](#tech-stack)
    * [Python Requirements](#python-requirements)
  * [How to Run](#how-to-run)
  * [Data](#data)
    * [Source](#source)
    * [Database Schema](#database-schema)
    * [Output](#output)
<!-- TOC -->

## Overview

What the project is trying to achieve:

- Extract structured romance fiction data from OpenLibrary API endpoints
- Build a relational data model for general works, authors, editions and series
- Clean and transform raw JSON into normalized tables
- Load processed data into a PostgreSQL database
- Ensure reproducibility and modular ETL design

### Pipeline Steps

1. `Extract`: fetch data from OpenLibrary API Store raw JSON in data/raw/
2. `Transform`: normalize nested JSON Apply data types and validation rules Generate structured tables
3. `Load`: create PostgreSQL database Create tables from SQL schema files Load processed CSVs into database

### Project Structure
    etl/
    database/
    data/
    utilities/
    config/
    main.py

## Tech Stack
    
    OpenLibrary API
    Python
    Pandas
    PostgreSQL


### Python Requirements

    greenlet==3.3.2
    numpy==2.4.4
    pandas==3.0.2
    PyMySQL==1.1.2
    python-dateutil==2.9.0.post0
    six==1.17.0
    SQLAlchemy==2.0.48
    typing_extensions==4.15.0
    tzdata==2025.3

## How to Run

    python main.py

## Data

### Source

OpenLibrary API was used for data ingestion.
See [api_documentation.md](https://github.com/EfiLygda/openlibrary-etl-pipeline/blob/Romance_Works/etl/extract/docs/api_documentation.md) for more information on API endpoints.

### Database Schema

![MainDiagram.svg](database/docs/MainDiagram.svg)

### Output

| Table    | Rows | Description        |
| -------- | ---- | ------------------ |
| authors  | ...  | author metadata    |
| works    | ...  | book works         |
| editions | ...  | edition-level info |



