import pytest

from cycling.model.core.ball import Ball


@pytest.fixture
def setup_ball():
    name = 'test_bike'
    mass = 0
    cda = 0
    radius = 1
    ball = Ball(name=name, mass=mass, cda=cda, radius=radius)
    return ball


def test_bike_representation(setup_ball):
    assert setup_ball.__repr__() == '<Ball: {}>'.format(setup_ball.name)
