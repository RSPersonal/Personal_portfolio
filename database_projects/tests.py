import uuid

from django.test import TestCase
from .models import Portfolio, Positions
from datetime import datetime
from database_projects import services
from django.contrib.auth.models import User
from uuid import uuid4


class TestPortfolio(TestCase):  # pragma: no cover
    def setUp(self):  # pragma: no cover
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

    def test_get_portfolio(self):  # pragma: no cover
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


class TestServices(TestCase):  # pragma: no cover
    def setUp(self):  # pragma: no cover
        test_user = User.objects.create(first_name='TestUser', last_name='TestUserSurname', email='testuser@gmail.com')
        test_portfolio = Portfolio.objects.create(pk=uuid.uuid4(),
                                                  portfolio_name='TestPortfolio',
                                                  user=test_user,
                                                  data_for_chart_array=[],
                                                  labels_array=[],
                                                  created_on=datetime.now(),
                                                  total_amount_invested=0,
                                                  total_profit=0,
                                                  total_profit_percentage=0.0,
                                                  total_positions=0,
                                                  monthly_profit=[],
                                                  id_for_chart=''
                                                  )
        empty_test_portfolio = Portfolio.objects.create(pk=uuid.uuid4(),
                                                        portfolio_name='TestPortfolioEmpty',
                                                        user=test_user,
                                                        data_for_chart_array=[],
                                                        labels_array=[],
                                                        created_on=datetime.now(),
                                                        total_amount_invested=0,
                                                        total_profit=0,
                                                        total_profit_percentage=0.0,
                                                        total_positions=0,
                                                        monthly_profit=[],
                                                        id_for_chart=''
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
        self.empty_test_portfolio = empty_test_portfolio
        self.current_month = current_month = datetime.now()

    def test_check_active_positions(self):  # pragma: no cover
        result = services.check_if_active_positions(self.test_portfolio.id)
        self.assertEqual(result, True)

    def test_check_active_positions_not_found(self):  # pragma: no cover
        result = services.check_if_active_positions(uuid4())
        self.assertEqual(result, False)

    def test_get_all_position_in_portfolio(self):  # pragma: no cover
        result = services.get_all_positions_in_portfolio(self.test_portfolio.id)
        self.assertEqual(len(result), 2)

    def test_check_if_active_positions_and_calculate_current_profits(self):
        """
        @return: None
        """
        check_if_active_position = services.check_if_active_positions(self.test_portfolio.id)
        self.assertEqual(check_if_active_position, True)
        positions = services.get_all_positions_in_portfolio(self.test_portfolio.id)

        if positions:
            self.assertTrue(positions)

            calculated_positions_profit = services.calculate_position_and_position_profit(positions)
            self.assertTrue(calculated_positions_profit)
            self.assertEqual(calculated_positions_profit['calculated_total_amount_invested_in_portfolio'], 1600)
            self.assertEqual(calculated_positions_profit['calculated_total_positions'], 2)

            for position in calculated_positions_profit['calculated_positions']:
                self.assertTrue(position['symbol'])
                self.assertTrue(position['calculated_profit'])
                self.assertTrue(position['calculated_total_invested'])
                self.assertTrue(position['current_market_price_from_api_call'])

    def test_get_portfolio_id_without_hypen(self):
        clean_id = services.get_portfolio_id_without_hyphen(self.test_portfolio)
        self.assertEqual(clean_id, services.remove_hyphen_from_portfolio_id(self.test_portfolio.id))

    def test_save_new_portfolio_to_db(self):
        test_monthly_profit_array = services.get_monthly_profit_array_until_current_month(self.current_month)
        services.save_new_portfolio_to_db('test_portfolio_1',
                                          self.test_user.id,
                                          [],
                                          [],
                                          test_monthly_profit_array)
        self.assertEqual(Portfolio.objects.filter(portfolio_name='test_portfolio_1').exists(), True)

    def test_get_postal_code_range(self):
        postal_code_range = services.get_postal_code_range('8021', 1000)
        self.assertEqual(postal_code_range, ['8021', '8022'])

    def test_check_if_portfolio_is_empty(self):
        check_if_empty_portfolio = services.check_if_portfolio_is_empty(self.empty_test_portfolio)
        self.assertEqual(check_if_empty_portfolio, True)
