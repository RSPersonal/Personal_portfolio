from database_projects.models import Portfolio, Positions
from typing import Any


def check_if_active_positions(portfolio_id: int) -> bool:
    """
    @param portfolio_id:
    @return: Object containing Portfolio or None
    """
    if Positions.objects.filter(portfolio=portfolio_id).exists():
        return True
    return False


def get_all_positions_in_portfolio(portfolio_id: int) -> Any:
    """
    @param portfolio_id:
    @return: Query object with all positions
    """
    return Positions.objects.filter(portfolio=portfolio_id).order_by('added_on')
