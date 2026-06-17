"""
Module for the type aliases of API types (deprecated)

Note:
    1. typing.Optional[X] is Union[X,None] == X | None
"""

from typing import TypeVar, TypeAlias

from .groups import WorkGroup, AuthorGroup, EditionGroup
from .summaries import AuthorSummary, EditionSummary, WorkSummary

from .extensions import (
    WorkSeries,
    WorkAvailability,
    WorkOverview,
    WorkRatings,

    AuthorStatistics,

    EditionDetails,
    EditionContents,
    EditionContributor,
    EditionPublishing
)


# Define a flexible variable type to be used as generic placeholder
T = TypeVar('T')


# --------------------------------------------------------------------
# Aliasing Types
# --------------------------------------------------------------------
# Note: Avoid nesting in routers

# - WORKS -
WorksAuthors: TypeAlias = WorkGroup[AuthorSummary]
WorksEditions: TypeAlias = WorkGroup[EditionSummary]
WorksSeries: TypeAlias = WorkGroup[WorkSeries]
WorksAvailability: TypeAlias = WorkGroup[WorkAvailability]
WorksOverview: TypeAlias = WorkGroup[WorkOverview]
WorksRatings: TypeAlias = WorkGroup[WorkRatings]

# - AUTHORS -
AuthorsWorks: TypeAlias = AuthorGroup[WorkSummary]
AuthorsStatistics: TypeAlias = AuthorGroup[AuthorStatistics]
AuthorsAlternativeNames: TypeAlias = AuthorGroup[str]
AuthorsEditions: TypeAlias = AuthorGroup[EditionSummary]

# - EDITIONS -
EditionsDetails: TypeAlias = EditionGroup[EditionDetails]
EditionsContents: TypeAlias = EditionGroup[EditionContents]
EditionsPublishing: TypeAlias = EditionGroup[EditionPublishing]
EditionsContributors: TypeAlias = EditionGroup[EditionContributor]
