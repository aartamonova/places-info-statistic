import unittest

from alchemy_mock.mocking import UnifiedAlchemyMagicMock, AlchemyMagicMock

from statistic.statistic_model import Action


class TestStatistic(unittest.TestCase):
    def test_get_none(self):
        session = UnifiedAlchemyMagicMock()
        result = session.query(Action).all()
        return self.assertEqual(len(result), 0)

    def test_get_attribute_error(self):
        session = AlchemyMagicMock()
        with self.assertRaises(AttributeError):
            session.query(Action).filter(Action.foo == 1).all()

    def test_get_all(self):
        session = UnifiedAlchemyMagicMock()
        session.add(Action(id=1, type='tag', login='user', description='123',
                           result='ok', timestamp='123'))
        result = session.query(Action).all()
        return self.assertEqual(len(result), 1)
