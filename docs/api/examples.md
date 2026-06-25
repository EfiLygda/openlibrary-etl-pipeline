
# API Examples

---

## Table of Contents

<!-- TOC -->
* [API Examples](#api-examples)
  * [Table of Contents](#table-of-contents)
  * [Overview](#overview)
  * [Suggested Usage Flow](#suggested-usage-flow)
  * [Common Response Format](#common-response-format)
    * [Entities](#entities)
    * [Entity Response](#entity-response)
    * [Relationship/Search Response](#relationshipsearch-response)
    * [Navigation Links Response](#navigation-links-response)
<!-- TOC -->

---

## Overview

This project provides a REST-style API built with FastAPI that exposes structured access to works, authors, editions, ratings, availability, and related metadata stored in a relational database derived from Open Library data.

It follows a REST-style design with consistent response envelopes:

- `data`: actual payload
- `meta`: pagination / entity metadata
- `links`: navigation and related resources

---

## Suggested Usage Flow

**STEP 1**: Start with search:

    GET /search?q=...

Example:

    GET /search?q=pride+prejudice&limit=3&offset=0

Response:

    {
      "data": [
        {
          "work_key": "OL66554W",
          "title": "Pride and Prejudice",
          "authors": [
            {
              "author_key": "OL21594A",
              "author_name": "Jane Austen"
            }
          ]
        },
        {
          "work_key": "OL15165350W",
          "title": "Pride and Prejudice",
          "authors": [
            {
              "author_key": "OL21594A",
              "author_name": "Jane Austen"
            }
          ]
        },
        {
          "work_key": "OL66597W",
          "title": "Novels (Pride and Prejudice / Sense and Sensibility)",
          "authors": [
            {
              "author_key": "OL21594A",
              "author_name": "Jane Austen"
            }
          ]
        }
      ],
      "meta": {
        "total": 21,
        "limit": 3,
        "offset": 0
      },
      "links": {
        "self": "/search?q=pride+prejudice&limit=3&offset=0",
        "next": "/search?q=pride+prejudice&limit=3&offset=3",
        "prev": null
      }
    }

> **Notes**: 
> 1. `limit` and `offset` can be used for pagination
> 2. Results are sorted by text relevance
> 3. Some search-level filters are supported via `/search`:
>    - `GET /search?q=pride&year=1813`
>    - `GET /search?q=pride&lang=eng`
>    - `GET /search?q=pride&published_by=penguin`
>    - `GET /search?q=pride&year=1813&lang=eng&published_by=penguin` 
> 4. Filters operate at the **work level**, even when data originates from editions
 
**STEP 2**: Pick a general work:

    GET /works/{work_key}

Example:

    GET /works/OL66554W

Response:

    {
      "data": [
        {
          "work_key": "OL66554W",
          "title": "Pride and Prejudice",
          "subtitle": null,
          "description": "Pride and Prejudice is an 1813 novel...",
          "first_sentence": null,
          "edition_count": 4038,
          "first_publish_year": 1813,
          "first_publish_date": "1853"
        }
      ],
      "meta": {
        "type": "work"
      },
      "links": {
        "self": "/works/OL66554W"
      }
    }

**STEP 3**: Explore work relationships:

Editions example:
    
    GET /works/OL66554W/editions?limit=3&offset=0
    
Response:

    {
      "data": [
        {
          "edition_key": "OL36513440M",
          "title": "Pride and Prejudice Illustrated",
          "subtitle": null,
          "edition_name": null
        },
        {
          "edition_key": "OL36525319M",
          "title": "Pride and Prejudice Illustrated",
          "subtitle": null,
          "edition_name": null
        },
        {
          "edition_key": "OL49198652M",
          "title": "Pride and Prejudice (Heron Faux-Leather Literary Heritage Collection) by Jane Austen (November 1, 1978) Hardcover",
          "subtitle": null,
          "edition_name": null
        }
      ],
      "meta": {
        "total": 4038,
        "limit": 3,
        "offset": 0
      },
      "links": {
        "self": "/works/OL66554W/editions?limit=3&offset=0",
        "next": "/works/OL66554W/editions?limit=3&offset=3",
        "prev": null
      }
    }

Authors example:

    GET /works/OL66554W/authors

Response:

    {
      "data": [
        {
          "author_key": "OL21594A",
          "author_name": "Jane Austen",
          "birth_year": 1775,
          "death_year": 1817
        }
      ],
      "meta": {
        "total": 1,
        "limit": 20,
        "offset": 0
      },
      "links": {
        "self": "/works/OL66554W/authors",
        "next": null,
        "prev": null
      }
    }

Ratings example:

    GET /works/OL66554W/ratings

Response:

    {
      "data": [
        {
          "ratings_count_1": 17,
          "ratings_count_2": 18,
          "ratings_count_3": 46,
          "ratings_count_4": 99,
          "ratings_count_5": 212
        }
      ],
      "meta": {
        "type": "work"
      },
      "links": {
        "self": "/works/OL66554W/ratings"
      }
    }

Availability example:

    GET /works/OL66554W/availability

Response:

    {
      "data": [
        {
          "ebook_access": "public",
          "has_fulltext": true,
          "has_public_scan": true
        }
      ],
      "meta": {
        "type": "work"
      },
      "links": {
        "self": "/works/OL66554W/availability"
      }
    }

Overview example:

    GET /works/OL66554W/overview

Response:

    {
      "data": [
        {
          "subjects": [
            "Adaptations",
            "Amours",
            "Austen, jane, 1775-1817",
            "British and Irish fiction (fictional works by one author)",
            "Brothers and sisters",
            "Clases sociales",
            ...
          ],
          "people": [
            "Caroline Bingley",
            "Catherine Bennet",
            "Catherine de Bourgh",
            "Charles Bingley",
            "Charlotte Lucas",
            "Elizabeth Bennet",
            "Fitzwilliam Darcy",
            ...
          ],
          "places": [
            "Brighton",
            "Derbyshire",
            "England",
            "Great Britain",
            "Hertfordshire",
            ...
          ],
          "time_periods": [
            "1789-1820",
            "19th century",
            "Jin dai"
          ]
        }
      ],
      "meta": {
        "type": "work"
      },
      "links": {
        "self": "/works/OL66554W/overview"
      }
    }

> **Note**: You can refer to the API's documentation 
> - Swagger UI: `{BASE_URL}/docs`
> - ReDoc: `{BASE_URL}/redoc`
> 
> for more relationships and endpoints, or the `link/{key}` endpoint for navigation links.

---

## Common Response Format

### Entities

The three main entities included are `works` for general works, `authors` for the authors and `editions` for the editions associated with the works.

---

### Entity Response

For entity endpoints (`/works/{key}`, `/authors/{key}`, `/editions/{key}`) and 1-1 relationship endpoints (`/works/{key}/ratings`, `/works/{key}/availability`, etc.), responses are structured as:

    {
      "data": {},
      "meta": {
        "type": "work" | "author" | "edition"
      },
      "links": {
        "self": "string"
      }
    }

---

### Relationship Response

For 1-many relationship endpoints (`/works/{key}/authors`, `/authors/{key}/works`, `/editions/{key}/contributors`, etc.), responses are structured as:

    {
      "data": [],
      "meta": {
        "parent_type": "work" | "author" | "edition",
        "parent_key": "string",
        "child_type": "string",
        "total_children": 0,
        "limit": 20,
        "offset": 0
      },
      "links": {
        "self": "",
        "next": null,
        "prev": null
      }
    }

---

### Batch Response

For batch endpoints (`/works?keys=...`, `/authors?keys=...`, `/editions?keys=...`), responses are structured as:

    {
      "data": [],
      "meta": {
        "type": "work" | "author" | "edition",
        "keys": [],
        "total": 0,
        "limit": 20,
        "offset": 0
      },
      "links": {
        "self": "",
        "next": null,
        "prev": null
      }
    }

---

### Navigation Links Response

For entity navigation and relationship discovery:

    {
      "key": "string",
      "type": "work" | "author" | "edition" | null,
      "links": {
        "self": "string",
        ...
      }
    }

---