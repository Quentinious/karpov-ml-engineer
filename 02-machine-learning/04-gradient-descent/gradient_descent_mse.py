"""Учебная MSE-регрессия: исходные формулы и градиент по признакам.

Восстановлен простой цикл с конечным лимитом шагов; см. ../REVIEW.md.
"""

from typing import Dict, List

import pandas as pd
import numpy as np
from tqdm import tqdm



class GradientDescentMse:
    """
    Класс для реализации градиентного спуска в задаче линейной регрессии
    с минимизацией среднеквадратичной ошибки (MSE).
    """

    def __init__(
        self,
        samples: pd.DataFrame,
        targets: pd.DataFrame,
        learning_rate: float = 1e-3,
        threshold: float = 1e-6,
        copy: bool = True,
        *,
        max_iterations: int = 10000,
    ):
        """Сохраняет выборку и параметры; начальные веса равны единице.

        targets: один таргет на строку, форма (n,) или (n, 1).
        Строки сопоставляются по позиции. copy=True защищает исходный DataFrame.
        """
        if samples.empty:
            raise ValueError("Матрица признаков 'samples' не должна быть пустой.")
        targets_array = np.asarray(targets)
        if not (targets_array.ndim == 1 or
                (targets_array.ndim == 2 and targets_array.shape[1] == 1)):
            raise ValueError("targets должен иметь форму (n,) или (n, 1).")
        if targets_array.size == 0 or samples.shape[0] != targets_array.shape[0]:
            raise ValueError("Количество строк samples и targets должно совпадать и быть ненулевым.")
        if not (np.isfinite(samples.to_numpy()).all() and np.isfinite(targets_array).all()):
            raise ValueError("samples и targets не должны содержать NaN или inf.")
        if not np.isfinite(learning_rate) or learning_rate <= 0:
            raise ValueError("learning_rate должен быть положительным конечным числом.")
        if not np.isfinite(threshold) or threshold <= 0:
            raise ValueError("threshold должен быть положительным конечным числом.")
        if not isinstance(max_iterations, int) or isinstance(max_iterations, bool) or max_iterations <= 0:
            raise ValueError("max_iterations должен быть положительным целым числом.")

        if copy:
            self.samples = samples.copy()
        else:
            self.samples = samples

        self.targets = targets_array.flatten()
        self.learning_rate = learning_rate
        self.threshold = threshold
        self.max_iterations = max_iterations
        self.beta = np.ones(self.samples.shape[1])
        self.iteration_loss_dict = {}

    def calculate_gradient(self) -> np.ndarray:
        """
        Вычисляет градиент функции потерь (MSE) по каждому признаку.
        """
        # Переводим всё в простые массивы NumPy, чтобы не запутаться
        X = self.samples.values
        y = self.targets # делаем y плоским вектором

        # 1. Считаем предсказания (скалярное произведение строк на веса)
        predictions = X.dot(self.beta)

        # 2. Считаем ошибки для каждого объекта
        errors = predictions - y

        # 3. Создаем пустой массив под градиенты
        gradients = np.zeros_like(self.beta)

        # 4. В цикле считаем градиент для каждого признака
        for i in range(X.shape[1]):
            # Берем i-й столбец признаков
            feature_column = X[:, i]

            # Градиент признака — это среднее значение от (2 * ошибка * признак)
            gradients[i] = np.mean(2 * errors * feature_column)

        return gradients

    def __str__(self) -> str:
        """
        Возвращает строковое представление текущего состояния модели.

        Returns:
            str:
                Строка с информацией о размере входных данных, параметрах обучения,
                начальных коэффициентах модели и количестве сохранённых итераций.
        """
        return (
            f"GradientDescentMse(\n"
            f"  samples_shape={self.samples.shape},\n"
            f"  targets_shape={self.targets.shape},\n"
            f"  learning_rate={self.learning_rate},\n"
            f"  threshold={self.threshold},\n"
            f"  beta={self.beta},\n"
            f"  iteration_loss_dict={self.iteration_loss_dict}\n)"
        )

    def learn(self, show_progress: bool = True):
        """Обучает до малого изменения MSE либо до max_iterations.

        Малое изменение ошибки — критерий остановки упражнения, а не гарантия
        нахождения минимума. История начинается заново, текущие веса сохраняются.
        """
        self.iteration_loss_dict = {}
        curr_loss = self.calculate_mse_loss()
        if not np.isfinite(curr_loss):
            raise FloatingPointError("Начальная MSE не является конечным числом.")
        self.iteration_loss_dict[0] = curr_loss
        step_id = 1
        progress = tqdm(
            desc="Обучение модели",
            unit="ит",
            dynamic_ncols=True,
            disable=not show_progress,
        )
        try:
            while step_id <= self.max_iterations:
                with np.errstate(over="raise", invalid="raise"):
                    self.iteration()
                    new_loss = self.calculate_mse_loss()
                if not np.isfinite(self.beta).all() or not np.isfinite(new_loss):
                    raise FloatingPointError("При обучении получены NaN или inf.")
                self.iteration_loss_dict[step_id] = new_loss
                progress.set_postfix(loss=new_loss)
                progress.update(1)

                if abs(curr_loss - new_loss) < self.threshold:
                    break
                curr_loss = new_loss
                step_id += 1
        finally:
            progress.close()

    def iteration(self):
        """
        Выполняет один шаг градиентного спуска.

        Использует текущий вектор градиента и learning_rate для обновления beta.
        """
        # Вычисляем градиент по всем признакам
        grad = self.calculate_gradient()

        # Обновляем коэффициенты по формуле градиентного спуска: β = β - learning_rate * grad
        self.beta = self.beta - self.learning_rate * grad

    def calculate_mse_loss(self) -> float:
        """
        Вычисляет среднеквадратичную ошибку (MSE) текущей модели.

        Ошибка рассчитывается как среднее значение квадратов разностей между
        предсказанными и истинными значениями.

        Returns:
            float: Текущее значение функции потерь MSE.
        """
        # Считаем предсказания модели: X * β
        predictions = self.samples.dot(self.beta)

        # self.targets = self.targets.flatten()
        # self.targets = np.asarray(self.targets).flatten()
        # Вычисляем среднеквадратичную ошибку:
        # MSE = mean((y_pred - y_true)^2)
        mse = np.mean(np.square(predictions - self.targets))
        return mse

    def add_constant_feature(self):
        """
        Добавляет в матрицу признаков столбец 'constant' со значением 1, если он ещё не добавлен.

        Это нужно для учёта свободного члена в линейной регрессии.
        Также вектор коэффициентов beta расширяется одним значением 1 для нового признака.
        """

        if 'constant' not in self.samples.columns:
            # Добавляем в DataFrame новый столбец 'constant', заполненный единицами
            self.samples['constant'] = 1

            # Расширяем вектор весов beta на один элемент (1.0) для нового признака
            self.beta = np.append(self.beta, 1.0)

    @staticmethod
    def run_gradient_descent_experiments(
            samples: pd.DataFrame,
            targets: pd.DataFrame,
            threshold_list: List[float],
            lr_list: List[float],
            show_progress: bool = False,
    ) -> Dict:
        """Незавершённая часть исходной работы: перебор параметров."""
        raise NotImplementedError("Перебор параметров в исходном решении не завершён.")


if __name__ == "__main__":
    X = pd.DataFrame([[1, 2], [3, 4], [5, 6]])
    y = pd.DataFrame([1, 2, 3])

    model = GradientDescentMse(X, y)
    print(model)
    # model.add_constant_feature()  # В исходном примере bias не включён.
    model.learn()
    print("Обученные коэффициенты beta:", model.beta)
    print("MSE:", model.calculate_mse_loss())
