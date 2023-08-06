"""
    Initialization functions
"""
import warnings
import logging

from sqlalchemy.exc import SAWarning

from endi_base.models.base import DBSESSION
from endi_base.models.base import DBBASE


def initialize_sql(engine):
    """
    Initialize the database engine
    """
    logger = logging.getLogger(__name__)
    logger.debug("Setting the metadatas")
    DBSESSION.configure(bind=engine)
    DBBASE.metadata.bind = engine
    return DBSESSION


def configure_warnings():
    """
    Python warning system setup

    Turns the sqla warning about implicit cartesian product into an exception,
    to be sure not to miss'em.

    If cartesian product is intentional, make it explicit.
    https://docs.sqlalchemy.org/en/14/changelog/migration_14.html#change-4737
    """
    warnings.filterwarnings(
        "error",
        category=SAWarning,
        # module='sqlalchemy.orm.relationships'
        module="sqlalchemy.sql.compiler",
        message=".*cartesian.*",
    )
