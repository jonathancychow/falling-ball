import pytest
import numpy as np

from ball.model.core.ball import Ball
from ball.model.core.environment import Environment
from ball.model.core.simulation import Simulation


@pytest.fixture
def sim_setup():
    ball = Ball(name='test_ball', mass=0.2, cda=0, radius=0)
    environment = Environment(gravity=9.81, air_density=1.2)
    simulation = Simulation(ball=ball, environment=environment)
    return simulation


def test_simulation_solve(sim_setup):
    v0 = 0.1
    t0 = 0
    s = np.arange(0, 100, 1)
    velocity, time = sim_setup.solve_velocity_and_time(s=s, v0=v0, t0=t0)
    assert len(velocity) == len(s)
    assert len(s) == len(time)
    assert all(velocity[i] <= velocity[i + 1] for i in range(len(velocity)-1))


if __name__ == '__main__':
    pytest.main()
