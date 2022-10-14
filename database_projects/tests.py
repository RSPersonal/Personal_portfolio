import unittest
from django.test import TestCase
from .models import Portfolio, Positions
from datetime import datetime
from .services import get_all_positions_in_portfolio, check_if_active_positions
from django.contrib.auth.models import User
from uuid import uuid4


class TestPortfolio(TestCase):
    def setUp(self):
        """
        @return: None
        """
        test_user = User.objects.create(first_name='TestUser', last_name='TestUserSurname', email='testuser@gmail.com')
        Portfolio.objects.create(portfolio_name='TestPortfolio',
                                 user=test_user,
                                 data_for_chart_array=[],
                                 labels_array=[],
                                 created_on=datetime.now(),
                                 total_amount_invested=0,
                                 total_profit=0,
                                 total_profit_percentage=0.0,
                                 total_positions=0,
                                 monthly_profit=[]
                                 )

    def test_get_portfolio(self):
        """
        @return: None
        """
        fetched_portfolio = Portfolio.objects.get(portfolio_name='TestPortfolio')
        self.assertEqual(fetched_portfolio.portfolio_name, 'TestPortfolio')
        self.assertEqual(fetched_portfolio.data_for_chart_array, [])
        self.assertEqual(fetched_portfolio.labels_array, [])
        self.assertEqual(fetched_portfolio.total_amount_invested, 0)
        self.assertEqual(fetched_portfolio.total_profit, 0)
        self.assertEqual(fetched_portfolio.total_profit_percentage, 0.0)
        self.assertEqual(fetched_portfolio.total_positions, 0)
        self.assertEqual(fetched_portfolio.monthly_profit, [])


class TestServices(TestCase):
    def setUp(self):
        test_user = User.objects.create(first_name='TestUser', last_name='TestUserSurname', email='testuser@gmail.com')
        test_portfolio = Portfolio.objects.create(portfolio_name='TestPortfolio',
                                                  user=test_user,
                                                  data_for_chart_array=[],
                                                  labels_array=[],
                                                  created_on=datetime.now(),
                                                  total_amount_invested=0,
                                                  total_profit=0,
                                                  total_profit_percentage=0.0,
                                                  total_positions=0,
                                                  monthly_profit=[]
                                                  )
        Positions.objects.create(pk=uuid4(),
                                 ticker_name='AAPL',
                                 buy_price=80,
                                 current_market_price=95,
                                 market='NASDAQ',
                                 quantity=10,
                                 amount_invested=800,
                                 position_profit=150,
                                 position_profit_in_percentage=15,
                                 portfolio=test_portfolio,
                                 added_on=datetime.now()
                                 )
        Positions.objects.create(pk=uuid4(),
                                 ticker_name='AMD',
                                 buy_price=80,
                                 current_market_price=95,
                                 market='NASDAQ',
                                 quantity=10,
                                 amount_invested=800,
                                 position_profit=150,
                                 position_profit_in_percentage=15,
                                 portfolio=test_portfolio,
                                 added_on=datetime.now()
                                 )
        self.test_user = test_user
        self.test_portfolio = test_portfolio

    def test_check_active_positions(self):
        result = check_if_active_positions(self.test_portfolio.id)
        self.assertEqual(result, True)

    def test_get_all_position_in_portfolio(self):
        result = get_all_positions_in_portfolio(self.test_portfolio.id)
        self.assertEqual(len(result), 2)
