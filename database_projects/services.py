from database_projects.models import Portfolio, Positions
from typing import Any


def check_if_active_positions(portfolio_id: int) -> Any:
    """
    @param portfolio_id:
    @param pk:
    @return: Object containing Portfolio or None
    """
    return Positions.objects.filter(portfolio=portfolio_id).exists()


def get_all_positions_in_portfolio(portfolio_id: int) -> Any:
    """
    @param portfolio_id:
    @return: Query object with all positions
    """
    return Positions.objects.filter(portfolio=portfolio_id).order_by('added_on')
