from database_projects.models import Portfolio, Positions
from typing import Any


def get_portfolio(pk: int) -> Any:
    """
    @param pk:
    @return: Object containing Portfolio or None
    """
    return Positions.objects.filter(portfolio=pk).exists()
