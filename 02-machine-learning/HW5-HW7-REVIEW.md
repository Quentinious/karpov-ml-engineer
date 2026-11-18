# HW5–HW7: сверка с локальными разборами

Проверялись именно Разбор_5.ipynb, Разбор_6.ipynb и Разбор_7.ipynb из Downloads.
Они использовались только для чтения и не перенесены в репозиторий.
Индивидуальное авторство исходного заполненного кода независимо не установлено: REVIEW.
CORRECT ниже означает корректность реализации упражнения, а не подтверждение результатов на полном Taxi.

## Выбор исходных версий

| HW | Выбранный исходник KarpovCourse/ML | Целевая копия | Сохранённая структура |
| --- | --- | --- | --- |
| 5 | Cross-Valodation/HW5_NEW.ipynb | [taxi-cross-validation.ipynb](05-cross-validation/taxi-cross-validation.ipynb) | 23 ячейки, исходный порядок и типы |
| 6 | Scaling/HW_6.ipynb | [taxi-scaling-regularization.ipynb](06-scaling-regularization/taxi-scaling-regularization.ipynb) | 19 ячеек, исходный порядок и типы |
| 7 | EDA/HW_7.ipynb | [taxi-feature-selection.ipynb](07-feature-selection/taxi-feature-selection.ipynb) | 38 ячеек, исходный порядок и типы |

В HW5_NEW уже есть собственный код первой модели, а оценка второй не закончена.
HW5_NEW_fixed — расширенная альтернатива: заново оформлена первая модель,
добавлены преобразования дат, imputer/pipeline и решение второй модели.
HW5_NEW_solved загружает initial_data.csv вместо подготовленных признаков для второй модели;
в сохранённом output есть ошибка преобразования строковой даты в число.
Эти версии не объединялись с базовой работой; авторство добавленных фрагментов — REVIEW.

HW_7 содержит исходные EDA-графики, ручные признаки, цикл get_dummies и начатый SFS.
HW_7_prepared_for_submission и HW_7_corrected_41_columns — доработанные альтернативы:
меняют набор входных признаков, OHE и добавляют проверки ожидаемого числа колонок.
В corrected_41_columns есть импорт из ML.Scaling.HW_6, отсутствующего как Python-модуль.
В prepared_for_submission есть сохранённый KeyboardInterrupt и незакрытая скобка
в ячейке 27 (индекс от нуля); этот файл не проходит проверку синтаксиса.
Ни название «prepared», ни «corrected» не подтверждает готовность работы.
Все альтернативы и Practice-файлы оставлены в исходном проекте без изменений.

Markdown исходных заданий пересказан своими словами в тех же позициях.
Код, переменные, циклы, содержательные комментарии, пустые ответы и маркеры
Your code is here сохранены, кроме перечисленных ниже исправлений.
Пример цикла Lasso в HW6 был дан в исходном задании и не заявляется новой авторской реализацией.
Исторические outputs не перенесены как актуальные результаты.

## Результаты сверки

| Упражнение | Моё решение | Статус | Исправление и причина |
| --- | --- | --- | --- |
| HW5: holdout и KFold | Test 20%, random_state=42; 20 фолдов, random_state=33 | CORRECT | Сохранено |
| HW5: преобразование таргета | log1p(trip_duration) | CORRECT | Сохранено |
| HW5: первая модель, CV и test | LinearSVR и MSLE поверх уже логарифмированного y | FIXED | LinearRegression для заданного MSE-обучения; MSE в лог-шкале без повторного логарифма и clipping |
| HW5: подготовленная таблица | Повторное обращение к trip_duration | FIXED | В местном CSV уже есть log_trip_duration; преобразование выполняется только при наличии исходного таргета |
| HW5: одинаковые фолды | isin сохранял порядок исходной таблицы | FIXED | loc повторяет порядок train/test первой модели |
| HW5: CV и test второй модели | Ячейки не заполнены | INCOMPLETE | Не дописывались |
| HW5: итоговое сравнение | Нет собственного ответа | INCOMPLETE | Не дописывалось |
| HW6: обе оценки CV | Четыре фолда без shuffle, MSE лог-таргета | CORRECT | Сохранено требование собственного исходника не перемешивать данные |
| HW6: ранг и число колонок | matrix_rank и shape после исключения таргета | CORRECT | Сохранено; численный ранг зависит от масштаба и допуска |
| HW6: масштабирование | Новый MinMaxScaler внутри каждого train-фолда | CORRECT | Утечки параметров scaler из validation нет |
| HW6: Ridge и Lasso | Собственные циклы alpha и средняя ошибка по фолдам | CORRECT | Pipeline из разбора не переносился |
| HW6: достижение MSLE < 0.4 | Требует исходного полного датасета | REVIEW | На полном Taxi не запускалось; значения alpha не объявляются подтверждёнными |
| HW7: объединение по id и календарные признаки | merge по индексу, datetime.dt | CORRECT | Формулы сохранены; полное совпадение id двух CSV отдельно не проверялось |
| HW7: графики и выводы по Taxi | Собственные Matplotlib/Seaborn-графики | REVIEW | Полный пересчёт не выполнялся; Seaborn отсутствует в целевой .venv |
| HW7: anomaly | День максимального среднего таргета | FIXED | День бури из разбора — 2016-01-23; максимум длительности не определяет дату погодного события |
| HW7: traffic_jam | Среднее по паре день–час, nlargest(10), isin | CORRECT | Соответствует условию EDA; алгоритм сохранён |
| HW7: One-Hot Encoding | Собственный цикл get_dummies для трёх колонок | CORRECT | Полный OHE допустим; drop_first из разбора не навязывается |
| HW7: ожидаемые 41 колонка | Локальная таблица содержит дополнительные feature_1..20 | REVIEW | Не удалялись признаки и категории ради совпадения числа колонок |
| HW7: корреляция | Series.corr | CORRECT | Формула проверена на малом примере; численный ответ Taxi не пересчитан |
| HW7: прямой отбор | SequentialFeatureSelector(..., n_features_to_select=5), но x/y не определены | FIXED | Добавлены определения x и y; таргет исключён из признаков |
| HW7: список отобранных признаков | Ячейка не заполнена | INCOMPLETE | Не дописывалась |
| HW7: качество после отбора и сравнение | Ячейка не заполнена | INCOMPLETE | Не дописывалась |

Теоретические ответы из разборов в собственные работы не добавлялись.

## Спорные места и data leakage

- В разборе HW5 также применяется isin. Однако при одинаковом позиционном KFold
  состав фолдов совпадает только при одинаковом порядке строк. На синтетических id
  проверено, что loc сохраняет этот порядок.
- В разборе HW6 стоит shuffle=True, но собственный исходник прямо запрещает
  перемешивание. Сохранён KFold без shuffle. Подписи RMSLE в разборе расходятся
  с кодом MSE лог-таргета; в целевой работе оставлена MSLE согласно собственному условию.
- В HW7 полный OHE корректен для используемой LinearRegression; другое число
  колонок само по себе не доказывает ошибку. В processed_data1.csv есть 20 дополнительных
  feature-колонок, а разбор использует базовую обработанную таблицу.
  Минимальное дальнейшее действие — уточнить требуемый входной CSV и точную схему LMS.
  Если требуется схема разбора, сначала выбрать базовые данные; drop_first=True
  можно добавить в имеющийся get_dummies без замены цикла. Это не сделано автоматически.
- traffic_jam определяется по таргету всей таблицы, как прямо требует упражнение EDA.
  Это допустимо для данного учебного исследования, но такой признак нельзя затем
  использовать для заявления независимого качества на CV/test без пересчёта только
  на обучающей части. Перед будущей оценкой минимальное исправление — вычислять top_10
  на train и применять полученный список к validation/test.
- Подготовленные CSV содержат passenger_count, закодированный средним таргетом.
  Из описания предшествующего задания следует кодирование по всей таблице; отделение
  holdout после такого кодирования не устраняет утечку. Поэтому CV на предоставленных
  признаках не объявляется независимой оценкой будущего качества.
  Для такой оценки потребуется исходный passenger_count и расчёт средних только
  по train каждого фолда. CSV и все notebooks ради этого автоматически не перестраивались.
- Финальное упражнение HW7 прямо предлагает оценку на обучающих данных.
  Это намеренная учебная оценка, а не независимая метрика; ячейка пока пустая.

## Данные и окружение

CSV не переносились. Для локального запуска нужны файлы в рабочем каталоге соответствующего notebook:

| HW | CSV и известное локальное расположение |
| --- | --- |
| 5 | Cross-Valodation/initial_data.csv (~174 MB), Cross-Valodation/processed_data.csv (~102 MB) |
| 6 | Scaling/mydata.csv (~102 MB), Scaling/new_data.csv (~398 MB) |
| 7 | EDA/processed_data1.csv (~398 MB), EDA/taxi_data2.csv (~191 MB) |

Это локальные учебные данные Taxi. Право их публичного распространения не подтверждено.
processed_data.csv для HW5 уже содержит log_trip_duration; mydata.csv имеет ту же
базовую схему, а new_data.csv/processed_data1.csv дополнительно содержат feature_1..20.
Их одинаковый размер не выдаётся за доказательство побайтового совпадения.

Необходимы NumPy, pandas и scikit-learn; для графиков HW7 — Matplotlib и Seaborn,
для исполнения notebook — Jupyter/ipykernel. Новые классы, pipeline и тестовые файлы не добавлялись.

Небольшие проверки выполнены в целевой .venv, CPython 3.13.5, NumPy 2.5.4,
pandas 3.1.1, scikit-learn 1.9.1, Matplotlib 3.11.2, без KarpovCourse в sys.path/PYTHONPATH.
HW5: 60 строк и 20 фолдов; проверены тождество метрики, оба вида таргета и совпадение id фолдов.
HW6: 32 строки и четыре фолда; выполнены исходные циклы Ridge/Lasso, проверки ранга и scaler.
HW7: малые проверки календаря, дня бури, top_10, полного OHE, корреляции и SFS на 30 строках.
Seaborn отсутствует; попытка установки не прошла из-за сетевого ограничения.
Графики Seaborn и Run All с полными CSV не проверены.

## Точные изменения вычислительного кода

Индексы ячеек отсчитываются от нуля; Markdown-пересказ в diff ниже не включён.

### HW5, исходная ячейка 10

```diff
--- HW5 source cell 10
+++ HW5 target cell 10
@@ -4 +4 @@
-from sklearn.svm import LinearSVR
+from sklearn.linear_model import LinearRegression
@@ -7 +7 @@
-model_cv = LinearSVR(random_state=33)
+model_cv = LinearRegression()
@@ -9 +9 @@
-# Считаем MSLE (не забываем минус перед функцией)
+# MSE уже логарифмированного таргета соответствует MSLE исходной длительности.
@@ -11 +11 @@
-    model_cv, X_train, y_train, cv=splitter, scoring="neg_mean_squared_log_error"
+    model_cv, X_train, y_train, cv=splitter, scoring="neg_mean_squared_error"
```

### HW5, исходная ячейка 11

```diff
--- HW5 source cell 11
+++ HW5 target cell 11
@@ -4,2 +4,2 @@
-from sklearn.metrics import mean_squared_log_error
-from sklearn.svm import LinearSVR
+from sklearn.metrics import mean_squared_error
+from sklearn.linear_model import LinearRegression
@@ -8 +8 @@
-model = LinearSVR(random_state=33)
+model = LinearRegression()
@@ -14,3 +13,0 @@
-# Защита: заменяем возможные отрицательные предсказания нулями, чтобы не упал логарифм
-y_pred = np.clip(y_pred, 0, None)
-
@@ -18 +15 @@
-test_score = mean_squared_log_error(y_test, y_pred)
+test_score = mean_squared_error(y_test, y_pred)
```

### HW5, исходная ячейка 16

```diff
--- HW5 source cell 16
+++ HW5 target cell 16
@@ -6,2 +6,3 @@
-processed_data = processed_data.assign(log_trip_duration=np.log1p(processed_data['trip_duration']))
-processed_data = processed_data.drop('trip_duration', axis=1)
+if 'trip_duration' in processed_data.columns:
+    processed_data = processed_data.assign(log_trip_duration=np.log1p(processed_data['trip_duration']))
+    processed_data = processed_data.drop('trip_duration', axis=1)
```

### HW5, исходная ячейка 18

```diff
--- HW5 source cell 18
+++ HW5 target cell 18
@@ -7,2 +7,2 @@
-X_train_2 = X_2[X_2.index.isin(train_indexes)]
-y_train_2 = y_2[y_2.index.isin(train_indexes)]
+X_train_2 = X_2.loc[train_indexes]
+y_train_2 = y_2.loc[train_indexes]
@@ -10,2 +10,2 @@
-X_test_2 = X_2[X_2.index.isin(test_indexes)]
-y_test_2 = y_2[y_2.index.isin(test_indexes)]
+X_test_2 = X_2.loc[test_indexes]
+y_test_2 = y_2.loc[test_indexes]
```

### HW7, исходная ячейка 23

```diff
--- HW7 source cell 23
+++ HW7 target cell 23
@@ -3 +3 @@
-storm_date = processed_data.groupby('date')['log_trip_duration'].mean().idxmax()
+storm_date = pd.Timestamp('2016-01-23').date()
```

### HW7, исходная ячейка 34

```diff
--- HW7 source cell 34
+++ HW7 target cell 34
@@ -9,0 +10,2 @@
+x = processed_data.drop('log_trip_duration', axis=1)
+y = processed_data['log_trip_duration']
```
