"""
STEP 2: Create the tables at `romance_fiction` database

Details: Tables are created at this sequence:
1. authors
2. authors_alternative_names
3. authors_statistics
4. works
5. authors_works
6. works_series
7. works_availability
8. works_subjects
9. works_people
10. works_places
11. works_time_periods
12. editions
13. editions_contributors
14. editions_publishing
15. editions_contents
16. editions_details
"""

from utilities.database import DB_NAME, db_connection

# ---------------------------------------------------------------------------------------
# --- Set up Connection to Database ---

# Establish connection
connection = db_connection(database=DB_NAME)

# Set up cursor
cursor = connection.cursor()
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Drop the Tables (if they already exist)

drop_sequence = [
    'authors_alternative_names',
    'authors_statistics',
    'authors_works',

    'authors',

    'works_series',
    'works_availability',
    'works_subjects',
    'works_people',
    'works_places',
    'works_time_periods',

    'editions_contributors',
    'editions_publishing',
    'editions_contents',
    'editions_details',
    'editions',

    'works',
]

for table_name in drop_sequence:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# --- Create Tables ---

# Step 1: Create `authors` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors
    (
        author_key VARCHAR PRIMARY KEY,
        author_name VARCHAR,
        bio VARCHAR,
        birth_date VARCHAR,
        death_date VARCHAR,
        birth_year INT,
        death_year INT
    );
""")

# Step 2: Create `authors_alternative_names` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors_alternative_names
    (
        author_key VARCHAR NOT NULL,
        author_alternative_name VARCHAR NOT NULL,

        PRIMARY KEY (author_key, author_alternative_name),

        CONSTRAINT fk_authors_alternative_names_author_key
            FOREIGN KEY (author_key)
            REFERENCES authors(author_key)
    );
""")

# Step 3: Create `authors_statistics` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors_statistics
    (
        author_key VARCHAR PRIMARY KEY,
        top_work VARCHAR,
        work_count INT,
        ratings_count_1 INT,
        ratings_count_2 INT,
        ratings_count_3 INT,
        ratings_count_4 INT,
        ratings_count_5 INT,
        readinglog_count INT,
        want_to_read_count INT,
        currently_reading_count INT,
        already_read_count INT,

        CONSTRAINT fk_authors_statistics_author_key
            FOREIGN KEY (author_key)
            REFERENCES authors(author_key)
    );
""")

# Step 4: Create `works` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works
    (
        work_key VARCHAR PRIMARY KEY,
        title VARCHAR,
        subtitle VARCHAR,
        description TEXT,
        first_sentence TEXT,
        edition_count INT,
        first_publish_year INT,
        first_publish_date VARCHAR
    );
""")

# Step 5: Create `authors_works` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS authors_works
    (
        author_key VARCHAR NOT NULL,
        work_key VARCHAR NOT NULL,
        
        PRIMARY KEY (author_key, work_key),
        
        CONSTRAINT fk_authors_works_author_key
            FOREIGN KEY (author_key)
            REFERENCES authors(author_key),
        CONSTRAINT fk_authors_works_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 6: Create `works_series` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_series
    (
        work_key VARCHAR PRIMARY KEY,
        series_key VARCHAR,
        series_position VARCHAR,
        name VARCHAR,

        CONSTRAINT fk_works_series_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 7: Create `works_availability` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_availability
    (
        work_key VARCHAR PRIMARY KEY,
        ebook_access VARCHAR,
        has_fulltext BOOL,
        has_public_scan BOOL,

        CONSTRAINT fk_works_availability_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 8: Create `works_subjects` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_subjects
    (
        work_key VARCHAR NOT NULL,
        subject VARCHAR NOT NULL,
        
        PRIMARY KEY (work_key, subject),
        
        CONSTRAINT fk_works_subjects_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 9: Create `works_people` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_people
    (
        work_key VARCHAR NOT NULL,
        person VARCHAR NOT NULL,

        PRIMARY KEY (work_key, person),

        CONSTRAINT fk_works_people_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 10: Create `works_places` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_places
    (
        work_key VARCHAR NOT NULL,
        place VARCHAR NOT NULL,

        PRIMARY KEY (work_key, place),

        CONSTRAINT fk_works_places_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 11: Create `works_time_periods` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS works_time_periods
    (
        work_key VARCHAR NOT NULL,
        time_period VARCHAR NOT NULL,

        PRIMARY KEY (work_key, time_period),

        CONSTRAINT fk_works_time_periods_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 12: Create `editions` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS editions
    (
        edition_key VARCHAR PRIMARY KEY,
        work_key VARCHAR,
        title VARCHAR,
        subtitle VARCHAR,
        edition_name VARCHAR,

        CONSTRAINT fk_editions_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );
""")

# Step 13: Create `editions_contributors` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS editions_contributors
    (
        contribution_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        contributor_name VARCHAR,
        contributor_role VARCHAR,
        by_statement VARCHAR,
        translated_from VARCHAR,
        translation_of VARCHAR,
                
        CONSTRAINT fk_editions_contributors_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );
""")

# Step 14: Create `editions_publishing` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS editions_publishing
    (
        publishing_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        publish_date VARCHAR,
        publish_year INT,
        publisher VARCHAR,
        publish_place VARCHAR,
        publish_country VARCHAR,
        series VARCHAR,

        CONSTRAINT fk_editions_publishing_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );
""")

# Step 15: Create `editions_contents` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS editions_contents
    (
        edition_key VARCHAR PRIMARY KEY,
        description VARCHAR,
        notes VARCHAR,
        first_sentence VARCHAR,

        CONSTRAINT fk_editions_contents_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );
""")

# Step 16: Create `editions_details` table
cursor.execute("""
CREATE TABLE IF NOT EXISTS editions_details
    (
        details_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        number_of_pages INT,
        physical_format VARCHAR,
        physical_dimensions VARCHAR,
        weight VARCHAR,
        language VARCHAR,

        CONSTRAINT fk_editions_details_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );
""")

# Close the connection
connection.close()
