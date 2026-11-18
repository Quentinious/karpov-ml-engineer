"""Небольшие математические проверки исходного учебного алгоритма."""
import unittest

import numpy as np
import pandas as pd

from gradient_descent_mse import GradientDescentMse


class GradientDescentTests(unittest.TestCase):
    def test_gradient(self):
        model = GradientDescentMse(pd.DataFrame({'x': [1., 2.]}), [0., 0.])
        self.assertEqual(model.calculate_mse_loss(), 2.5)
        np.testing.assert_allclose(model.calculate_gradient(), [5.])

    def test_one_step(self):
        model = GradientDescentMse(pd.DataFrame({'x': [1., 2.]}), [0., 0.],
                                   learning_rate=0.1)
        model.iteration()
        np.testing.assert_allclose(model.beta, [0.5])
        self.assertEqual(model.calculate_mse_loss(), 0.625)

    def test_gradient_by_finite_differences(self):
        model = GradientDescentMse(pd.DataFrame({'x': [-1., 0., 2.]}), [1., 0., 3.])
        model.add_constant_feature()
        initial = np.array([0.3, -0.2])
        model.beta = initial.copy()
        gradient = model.calculate_gradient()
        epsilon = 1e-6
        for i in range(len(initial)):
            model.beta = initial.copy()
            model.beta[i] += epsilon
            plus = model.calculate_mse_loss()
            model.beta[i] -= 2 * epsilon
            minus = model.calculate_mse_loss()
            self.assertAlmostEqual(gradient[i], (plus - minus) / (2 * epsilon), places=6)

    def test_line_with_bias(self):
        X = pd.DataFrame({'x': [-2., -1., 0., 1., 2.]})
        before = X.copy()
        model = GradientDescentMse(X, 3 * X['x'] + 2, learning_rate=0.1,
                                   threshold=1e-16, max_iterations=1000)
        model.add_constant_feature()
        model.learn(show_progress=False)
        np.testing.assert_allclose(model.beta, [3., 2.], atol=1e-6, rtol=0)
        self.assertLess(model.calculate_mse_loss(), 1e-14)
        pd.testing.assert_frame_equal(X, before)

    def test_iteration_limit(self):
        model = GradientDescentMse(pd.DataFrame({'x': [1.]}), [0.],
                                   learning_rate=0.1, threshold=1e-30, max_iterations=2)
        model.learn(show_progress=False)
        self.assertEqual(list(model.iteration_loss_dict), [0, 1, 2])
        np.testing.assert_allclose(model.beta, [0.64])

    def test_oscillation_is_bounded(self):
        model = GradientDescentMse(pd.DataFrame({'x': [1.]}), [0.],
                                   learning_rate=1., max_iterations=3)
        model.learn(show_progress=False)
        self.assertLessEqual(len(model.iteration_loss_dict), 4)
        # Одинаковая MSE может остановить цикл без достижения минимума.
        self.assertEqual(model.calculate_mse_loss(), 1.)


if __name__ == '__main__':
    unittest.main()
