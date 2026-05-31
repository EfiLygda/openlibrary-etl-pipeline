# Openlibrary ETL Pipeline

An end-to-end ETL pipeline that extracts data from the Open Library API, transforms it into structured datasets, and loads it into a relational database using a schema-driven design.

## Objectives

What the project is trying to achieve:

- Extract structured romance fiction data from OpenLibrary API endpoints
- Build a relational data model for general works, authors, editions and series
- Clean and transform raw JSON into normalized tables
- Load processed data into a PostgreSQL database
- Ensure reproducibility and modular ETL design

## Data Source

OpenLibrary API was used for data ingestion.
See `[etl/extract/docs](https://github.com/EfiLygda/openlibrary-etl-pipeline/blob/Romance_Works/etl/extract/docs/api_documentation.md)` for more information on API endpoints.
