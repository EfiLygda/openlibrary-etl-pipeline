
# OpenLibrary API

*Source: https://openlibrary.org/developers/api*


## Table of Contents

<!-- TOC -->
* [OpenLibrary API](#openlibrary-api)
  * [Table of Contents](#table-of-contents)
  * [OpenLibrary Keys](#openlibrary-keys)
  * [API Endpoints](#api-endpoints-)
    * [General Works](#general-works)
      * [`SEARCH`](#search)
      * [`WORKS`](#works)
      * [`WORKS_RATINGS`](#works_ratings)
    * [Editions of Works](#editions-of-works)
      * [`BOOKS`](#books)
      * [`SEARCH_EDITIONS_VIA_WORK_KEY`](#search_editions_via_work_key)
    * [Authors](#authors)
      * [`AUTHORS`](#authors-1)
      * [`SEARCH_AUTHORS`](#search_authors)
      * [`SEARCH_AUTHORS_SUBJECT`](#search_authors_subject)
      * [`AUTHORS_ALL_WORKS`](#authors_all_works)
    * [Series](#series)
      * [`SERIES`](#series-1)
      * [`SERIES_WORKS`](#series_works)
    * [Subjects](#subjects)
      * [`SUBJECTS`](#subjects-1)
      * [`SEARCH_SUBJECTS`](#search_subjects)
      * [`PERSONS`](#persons)
      * [`TIMES`](#times)
    * [Publishing](#publishing)
      * [`PUBLISHERS`](#publishers)
    * [Batches](#batches)
      * [`GET_MANY`](#get_many)
<!-- TOC -->


## OpenLibrary Keys

Bellow are the patterns for the available keys in the API:

- `work`: OLxxxxW
- `author`: OLxxxxA
- `edition`: OLxxxxM
- `series`: OLxxxxL

Normalized keys:

- `work`: /works/OLxxxxW
- `author`: /authors/OLxxxxA
- `edition`: /books/OLxxxxM
- `series`: /series/OLxxxxL

> *Note*: `x` is a digit


## API Endpoints 

### General Works

#### `SEARCH`

https://openlibrary.org/search.json
    
 - *Description*: Returns general works, according to its parameters
 - *Parameters*: 
     * `q`: the query used for the API
     * `subject`: the general works' subject
     * `page`: the page number for the records returned via the API
     * `limit`: the maximum number of records to be returned via the API in a page

 - *Example*: Page 20 with maximum 100 records for romance fiction general works
https://openlibrary.org/search.json?subject=romance+fiction&page=20&limit=100

#### `WORKS`
https://openlibrary.org/works/{WORK_KEY}.json
 - *Description*: Returns a general works data
 - *Example*: https://openlibrary.org/works/OL77775W.json

#### `WORKS_RATINGS`
https://openlibrary.org/works/{WORK_KEY}/ratings.json
 - *Description*: Returns a general works ratings
 - *Example*: https://openlibrary.org/works/OL17824318W/ratings.json

### Editions of Works

#### `BOOKS`
https://openlibrary.org/books/{EDITION_KEY}.json

 - *Description*: Returns a specific editions data
 - *Example*: https://openlibrary.org/books/OL45650119M.json

#### `SEARCH_EDITIONS_VIA_WORK_KEY`
https://openlibrary.org/works/{WORK_KEY}/editions.json

 - *Description*: Returns maximum 50 editions of a general work using its work key (same fields as `EDITIONS`)
 - *Parameters*:
     * `offset`: used to move to next batch
 - *Example*: 
   * First 50 editions as returned: https://openlibrary.org/works/OL18020194W/editions.json

   * Next 50 editions: https://openlibrary.org/works/OL18020194W/editions.json?&offset=50


### Authors

#### `AUTHORS`
https://openlibrary.org/authors/{AUTHOR_KEY}.json

 - *Description*: Returns specific author's data
 - *Example*: https://openlibrary.org/authors/OL7412785A.json

#### `SEARCH_AUTHORS`
https://openlibrary.org/search/authors.json?q={AUTHOR_NAME}

 - *Description*: Contains enriched author data, searched by name
 - *Parameters*:
     * `q`: the query used for the author, here the name
     * `limit`: maximum number of authors in a page as returned via the API
 - *Example*: https://openlibrary.org/search/authors.json?q=kelly%20bowen

#### `SEARCH_AUTHORS_SUBJECT`
https://openlibrary.org/search/authors.json?q={GERNE}&limit=1

 - *Description*: Contains enriched author data, searched by genre
 - *Parameters*:
     * `q`: the query used for the author, here the genre
     * `limit`: maximum number of authors in a page as returned via the API
 - *Example*: This returns romance authors https://openlibrary.org/search/authors.json?q=romance

#### `AUTHORS_ALL_WORKS`
https://openlibrary.org/authors/{AUTHOR_KEY}/works.json

 - *Description*: Returns all general works of an author
 - *Example*: https://openlibrary.org/authors/OL7412785A/works.json


### Series

#### `SERIES`
https://openlibrary.org/series/{SERIES_KEY}.json

 - *Description*: Returns a book series data
 - *Example*: https://openlibrary.org/series/OL331100L.json

#### `SERIES_WORKS`
https://openlibrary.org/series/{SERIES_KEYS}/seeds.json

 - *Description*: Returns a book series' general works (all books in the series)
 - *Example*: https://openlibrary.org/series/OL331100L/seeds.json


### Subjects

#### `SUBJECTS`
https://openlibrary.org/subjects/{SUBJECT_NAME}.json

 - *Description*: Returns general works that are use the current subject
 - *Example*: https://openlibrary.org/subjects/romance.json

#### `SEARCH_SUBJECTS`
https://openlibrary.org/search/subjects.json

 - *Description*: Returns subject data
 - *Parameters*:
   * `q`: the query used for the API
 - *Example*: https://openlibrary.org/search/subjects.json?q=romance

#### `PERSONS`
https://openlibrary.org/subjects/person:{PERSON_NAME}.json

 - *Description*: Returns subject person data
 - *Example*: https://openlibrary.org/subjects/person:jesus_christ.json

#### `TIMES`
https://openlibrary.org/subjects/time:{TIME_PERIOD}.json

 - *Description*: Returns a subject time period's data
 - *Example*: https://openlibrary.org/subjects/time:20th_century.json


### Publishing

#### `PUBLISHERS`
https://openlibrary.org/publishers/{PUBLISHER_NAME}.json

 - *Description*: Returns a publisher's data
 - *Example*: https://openlibrary.org/publishers/HarperCollins_Publishers.json


### Batches

#### `GET_MANY`
https://openlibrary.org/api/get_many?keys=%5B%22{KEY_1}%22,%22{KEY_2}%22%5D

 - *Description*: Returns OpenLibrary record batches via their keys. Can be used for works, authors, editions and series at the same time, using their normalized keys
 - *Example*: https://openlibrary.org/api/get_many?keys=%5B%22/authors/OL7412785A%22,%22/authors/OL7300387A%22%5D
