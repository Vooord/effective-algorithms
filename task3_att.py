# Новак Ян ПИ17-1, вариант – 1 (номер по списку – 8)
#
# Задание:
# 1. Невероятно популярная испаноязычная поисковая система Goog проводит огромный объем
# вычислений при каждом пересчете индекса. К счастью, в распоряжении компании имеется
# один суперкомпьютер с практически неограниченным запасом мощных рабочих станций.
# Вычисления разбиты на n заданий J1, J2, ..., Jn, которые могут выполняться полностью
# независимо друг от друга. Каждое задание состоит из двух фаз: сначала оно проходит
# предварительную обработку на суперкомпьютере, а затем завершается на одной из рабочих
# станций. Допустим, обработка задания Ji требует pi секунд на суперкомпьютере, а затем
# fi секунд на рабочей станции. На площадке доступны как минимум n рабочих станций,
# поэтому завершающая фаза обработки всех заданий может проходить параллельно — все
# задания будут выполняться одновременно. Однако суперкомпьютер может работать только с
# одним заданием, поэтому администратор должен определить порядок передачи заданий
# суперкомпьютеру. Как только первое задание в этом порядке будет обработано на
# суперкомпьютере, оно передается на рабочую станцию для завершения; после обработки на
# суперкомпьютере второе задание передается на рабочую станцию независимо от того,
# завершилось первое задание или нет (так как рабочие станции работают параллельно), и
# т. д. Допустим, расписание представляет собой упорядоченный список заданий для
# суперкомпьютера, а время завершения расписания определяется самым ранним временем
# завершения всех заданий на рабочих станциях. Очень важно свести к минимуму эту
# характеристику, так как она определяет, насколько быстро El Goog сможет построить
# новый индекс.
#
# Предложите алгоритм с полиномиальным временем, который находит расписание с минимальным
# временем завершения.
#
# Примечание: Описание подходов к решению задачи представлены ниже в блоке `if __name__ == "__main__":`,
# который является входной точкой в программу.

from typing import List, Dict, Tuple


def analyzeQueue(queue: List[Dict[str, int]]) -> Dict[str, int]:
    length = 0
    latestTaskcompleteTime = 0
    for task in queue:
        length += task["p"]
        taskCompleteTime = length + task["f"]
        if latestTaskcompleteTime < taskCompleteTime:
            latestTaskcompleteTime = taskCompleteTime
    return {"p_time": length, "f_time": latestTaskcompleteTime}


def sortByKey(
    tasks: List[Dict[str, int]], sortKey: str = "f", reverse: bool = True
) -> List[Dict[str, int]]:
    return sorted(tasks, key=lambda x: x[sortKey], reverse=reverse)


def sortByCoefSum(
    tasks: List[Dict[str, int]], p: float = 0.1, f: float = 0.9, reverse: bool = True
) -> List[Dict[str, int]]:
    # если сумма коэффициентов не равна 1, нормализуем коэффициенты
    if p + f != 1:
        p = p / (p + f)
        f = 1 - p
    return sorted(tasks, key=lambda x: x["p"] * p + x["f"] * f, reverse=reverse)


def sortByAttitude(
    tasks: List[Dict[str, int]],
    attitudeKeys: Tuple[str, str] = ("p", "f"),
    reverse: bool = True,
) -> List[Dict[str, int]]:
    return sorted(
        tasks, key=lambda x: x[attitudeKeys[0]] / x[attitudeKeys[1]], reverse=reverse
    )


def showQueue(queue: List[Dict[str, int]]) -> str:
    res = ["["]
    res.extend(["\t" + str(task) for task in queue])
    res.append("]")
    return "\n".join(res)


def runExperiment(
    tasks: List[Dict[str, int]],
    expName: str = "",
    printExperimentNames: bool = True,
    printResultedQueue: bool = False,
    printAnalyticStats: bool = True,
) -> Dict[str, Dict[str, int]]:
    analytics = {}

    if printExperimentNames:
        print(f"-- Experiment: {expName} --")

    queue = sortByKey(tasks)
    queue_analyze_stats = analyzeQueue(queue)
    analytics["f_sort"] = queue_analyze_stats
    if printExperimentNames:
        print("--- F Sort ---")
    if printResultedQueue:
        print(showQueue(queue))
    if printAnalyticStats:
        print(f"\t{queue_analyze_stats}")

    queue = sortByKey(tasks, "p")
    queue_analyze_stats = analyzeQueue(queue)
    analytics["p_sort"] = queue_analyze_stats
    if printExperimentNames:
        print("--- P Sort ---")
    if printResultedQueue:
        print(showQueue(queue))
    if printAnalyticStats:
        print(f"\t{queue_analyze_stats}")

    queue = sortByAttitude(tasks, ("p", "f"))
    queue_analyze_stats = analyzeQueue(queue)
    analytics["attitude_sort"] = queue_analyze_stats
    if printExperimentNames:
        print("--- Attitude Sort ---")
    if printResultedQueue:
        print(showQueue(queue))
    if printAnalyticStats:
        print(f"\t{queue_analyze_stats}")

    if printExperimentNames:
        print("--- Coef Sum Sort ---")
    for i in range(1, 10):
        coef = i / 10
        if printExperimentNames:
            print(f"\t-- sorting with coef: p={coef}, f={1 - coef}")

        queue = sortByCoefSum(tasks, coef, 1 - coef)
        queue_analyze_stats = analyzeQueue(queue)
        analytics[f"coef_sort_{coef}"] = queue_analyze_stats
        if printResultedQueue:
            print(showQueue(queue))
        if printAnalyticStats:
            print(f"\t\t{queue_analyze_stats}")

    print('Experiment finished successfully.\n\n')
    return analytics


if __name__ == "__main__":
    # В условии сказано, что все операции на суперкомпьютере (p)  выполняются последовательно.
    # Это означает, что время их выполнения константно и равно сумме всех p.
    # Все операции на рабочих станциях (f) могут выполняться параллельно и независимо друг
    # от друга, при этом кол-во рабочих станций гарантируется как n+1, где n – общее кол-во задач.
    # Операция f не может быть запущена до выполнения соответствующей операции p.
    # Исходя из всего этого, наша задача – найти такую очередь задач, при которой остаточное время,
    # необходимое для окончания самой поздней (с точки зрения завершения) операции f минимально.

    # рассмотрим следующие варианты сортировки:
    # 1. сортировка заданий по убыванию времени операций f
    # 2. сортировка заданий по убыванию времени операций p
    # 3. сортировка заданий по убыванию суммы `coef * p + (1-coef) * f`, где coef - коэффициент из
    #    диапазона [0.1, 0.9] с шагом 0.1
    # 4. сортировка заданий по убыванию отношения параметров `p/f`

    # теоретические выводы по поставленным вариантам
    # 1. так как мы сортируем по убываю f, то после завершения последней операции p начнется
    #    операция f минимальной продолжительности, что гарантирует минимальное остаточное время
    # 2. сортировка по параметру p не имеет смысла, так как все операции p выполняются последовательно,
    #    соответственно суммарное время, затраченное на операции p, будет константно, а поседняя
    #    операция p может запускать не самую короткую операцию f, что не гарантирует минимального
    #    остаточного времени
    # 3. данный вариант представляет собой некоторый компромисс между решениями 1 и 2, вводя
    #    коэффициент значимости параметров p и f, однако, исходя из вывода к решению 2, сортировать
    #    по параметру p не имеет смысла
    # 4. отношение параметров p и f представляет собой коэффициент относительной продолжительности
    #    выполнения операций самого задания и никак не учитывает их продолжительность, то есть
    #    коэффициент задания с `p = 10, f = 5` будет равен коэффициенту задания с `p = 100, f = 50`,
    #    однако очевидно, что порядок заданий должен быть [2, 1], а суммарное время будет равно 150,
    #    в то время как алгоритм может вернуть последовательность [1, 2], при этом суммарное время
    #    будет равно 160, то есть равные коэффициенты дают различные решения

    # При первой попытке защиты этого решения, был предложен вариант оптимизации,
    # который схематично выглядит примерно так:
    # p-flow : ——————————————|
    # f-flow : ————|———-|————|
    #
    # Очевидно, что он имеет смысл только, когда мы имеет лишь одну рабочую станцию для выполнения задач f.
    # При этом мы допускаем, что есть еще своя очередь для задач f, прошедших этап p.
    #
    # Добиться такой ситуации можно вот как:
    # 1) Находим такие задачи, для которых p намного меньше f
    # 2) Быстро прогоняем их через p –> они попадают в очередь на f
    # 3) Когда очередь на f достаточно большая, мы запускаем большую задачу на p
    #
    # Как было сказано, в нашем случае это не имеет смысла.
    # Кол-во рабочих станций гарантированно как n + 1 и никакой очереди для f физически не может быть.

    # Исходя из четырех рассмотренных решений, мы упираемся в оптимальный алгоритм сортировки
    # во всех четырех решениях, поэтому следует оптимизировать алгоритм сортировки.
    #
    # Для удобства возьмем встроенную в язык программирования Python функцию sorted, которая
    # возвращает отсортированный массив в соответствии с переданным ключом.
    #
    # Временная сложность встроенного алгоритма сортировки - O(n*log(n)) в лучшем случае, что
    # так же соответствует временной сложности в общем случае, и O(n^2) в худшем случае.
    # Это соответствует алгоритму быстрой сортировки, который является жадным алгоритмом:
    # 1. случайным образом выбирается опорный элемент массива (обычно - середина массива)
    # 2. остальные элементы массива сравниваются с опорным и, если они меньше опорного,
    #    помещаются в левую часть массива, иначе - в правую
    # 3. рекурсивно повторить алгоритм для обоих отрезков (отрезки "меньших" и "больших"
    #    элементов), если отрезок имеет длину не более двух - вернуть отсортированный отрезок,
    #    метод сортировки в данном случае - сравнение обоих элементов отрезка

    # Для подтверждения теории на практике реализуем все 4 рассмотренных решения для различных наборов данных:

    basic_random_case = [
        {'p': 10, 'f': 20},
        {'p': 5, 'f': 10},
        {'p': 3, 'f': 29},
        {'p': 15, 'f': 10},
        {'p': 12, 'f': 12},
        {'p': 11, 'f': 11},
        {'p': 15, 'f': 8},
        {'p': 13, 'f': 15},
        {'p': 9, 'f': 9},
    ]
    runExperiment(basic_random_case, "Basic")
    # output >>>
    # -- Experiment: Basic --
    # --- F Sort ---
    # 	{'p_time': 93, 'f_time': 101}
    # --- P Sort ---
    # 	{'p_time': 93, 'f_time': 122}
    # --- Attitude Sort ---
    # 	{'p_time': 93, 'f_time': 122}
    # --- Coef Sum Sort ---
    # 	-- sorting with coef: p=0.1, f=0.9
    # 		{'p_time': 93, 'f_time': 101}
    # 	-- sorting with coef: p=0.2, f=0.8
    # 		{'p_time': 93, 'f_time': 102}
    # 	-- sorting with coef: p=0.3, f=0.7
    # 		{'p_time': 93, 'f_time': 103}
    # 	-- sorting with coef: p=0.4, f=0.6
    # 		{'p_time': 93, 'f_time': 103}
    # 	-- sorting with coef: p=0.5, f=0.5
    # 		{'p_time': 93, 'f_time': 103}
    # 	-- sorting with coef: p=0.6, f=0.4
    # 		{'p_time': 93, 'f_time': 103}
    # 	-- sorting with coef: p=0.7, f=0.30000000000000004
    # 		{'p_time': 93, 'f_time': 108}
    # 	-- sorting with coef: p=0.8, f=0.19999999999999996
    # 		{'p_time': 93, 'f_time': 117}
    # 	-- sorting with coef: p=0.9, f=0.09999999999999998
    # 		{'p_time': 93, 'f_time': 117}
    # Experiment finished successfully.

    f_gt_p_case = [
        {'p': 10, 'f': 16},
        {'p': 4, 'f': 8},
        {'p': 17, 'f': 27},
        {'p': 23, 'f': 28},
        {'p': 8, 'f': 19},
        {'p': 16, 'f': 24},
        {'p': 4, 'f': 21},
        {'p': 0, 'f': 9},
        {'p': 0, 'f': 21},
        {'p': 25, 'f': 28}
    ]
    runExperiment(f_gt_p_case, "All 'f' are greater than 'p'")
    # output >>>
    # -- Experiment: All 'f' are greater than 'p' --
    # --- F Sort ---
    # 	{'p_time': 107, 'f_time': 119}
    # --- P Sort ---
    # 	{'p_time': 107, 'f_time': 128}
    # --- Attitude Sort ---
    # 	{'p_time': 107, 'f_time': 128}
    # --- Coef Sum Sort ---
    # 	-- sorting with coef: p=0.1, f=0.9
    # 		{'p_time': 107, 'f_time': 119}
    # 	-- sorting with coef: p=0.2, f=0.8
    # 		{'p_time': 107, 'f_time': 119}
    # 	-- sorting with coef: p=0.3, f=0.7
    # 		{'p_time': 107, 'f_time': 119}
    # 	-- sorting with coef: p=0.4, f=0.6
    # 		{'p_time': 107, 'f_time': 124}
    # 	-- sorting with coef: p=0.5, f=0.5
    # 		{'p_time': 107, 'f_time': 124}
    # 	-- sorting with coef: p=0.6, f=0.4
    # 		{'p_time': 107, 'f_time': 124}
    # 	-- sorting with coef: p=0.7, f=0.30000000000000004
    # 		{'p_time': 107, 'f_time': 124}
    # 	-- sorting with coef: p=0.8, f=0.19999999999999996
    # 		{'p_time': 107, 'f_time': 128}
    # 	-- sorting with coef: p=0.9, f=0.09999999999999998
    # 		{'p_time': 107, 'f_time': 128}
    # Experiment finished successfully.

    p_gt_f_case = [
        {'p': 14, 'f': 4},
        {'p': 9, 'f': 8},
        {'p': 2, 'f': 2},
        {'p': 30, 'f': 19},
        {'p': 17, 'f': 17},
        {'p': 27, 'f': 12},
        {'p': 10, 'f': 7},
        {'p': 11, 'f': 2},
        {'p': 21, 'f': 14},
        {'p': 27, 'f': 7}
    ]
    runExperiment(p_gt_f_case, "All 'p' are greater than 'f'")
    # output >>>
    # -- Experiment: All 'p' are greater than 'f' --
    # --- F Sort ---
    # 	{'p_time': 168, 'f_time': 170}
    # --- P Sort ---
    # 	{'p_time': 168, 'f_time': 174}
    # --- Attitude Sort ---
    # 	{'p_time': 168, 'f_time': 185}
    # --- Coef Sum Sort ---
    # 	-- sorting with coef: p=0.1, f=0.9
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.2, f=0.8
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.3, f=0.7
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.4, f=0.6
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.5, f=0.5
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.6, f=0.4
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.7, f=0.30000000000000004
    # 		{'p_time': 168, 'f_time': 170}
    # 	-- sorting with coef: p=0.8, f=0.19999999999999996
    # 		{'p_time': 168, 'f_time': 174}
    # 	-- sorting with coef: p=0.9, f=0.09999999999999998
    # 		{'p_time': 168, 'f_time': 174}
    # Experiment finished successfully.

    mixed_case = [
        {'p': 9, 'f': 26},
        {'p': 9, 'f': 26},
        {'p': 9, 'f': 9},
        {'p': 20, 'f': 28},
        {'p': 6, 'f': 16},
        {'p': 30, 'f': 1},
        {'p': 21, 'f': 2},
        {'p': 6, 'f': 3},
        {'p': 9, 'f': 4},
        {'p': 14, 'f': 8}
    ]
    runExperiment(mixed_case, "Mixed case: both f > p and p > f")
    # output >>>
    # -- Experiment: Mixed case: both f > p and p > f --
    # --- F Sort ---
    # 	{'p_time': 133, 'f_time': 134}
    # --- P Sort ---
    # 	{'p_time': 133, 'f_time': 143}
    # --- Attitude Sort ---
    # 	{'p_time': 133, 'f_time': 159}
    # --- Coef Sum Sort ---
    # 	-- sorting with coef: p=0.1, f=0.9
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.2, f=0.8
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.3, f=0.7
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.4, f=0.6
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.5, f=0.5
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.6, f=0.4
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.7, f=0.30000000000000004
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.8, f=0.19999999999999996
    # 		{'p_time': 133, 'f_time': 136}
    # 	-- sorting with coef: p=0.9, f=0.09999999999999998
    # 		{'p_time': 133, 'f_time': 143}
    # Experiment finished successfully.


    # Небольшое пояснение к выводимым данным:
    # 'p_time' - время окончания работы последнего процесса p,
    # 'f_time' - время окончания работы последнего процесса f.
    # Таким образом, искомое остаточное время равно `f_time - p_time`

    # В результате четырех экспериментов и эксперимента с интервалами видно, что время работы
    # суперкомпьютера, как и предполагалось, константно и не меняется от решения к решению,
    # в то время как результирующее время индексирования зависело от способа сортировки:
    # сортировка по продолжительности операций f стабильно выдает лучший результат, при этом
    # коэффициентная сортировка всегда выдает схожий результат при маленькой значимести
    # критерия p, однако коэффициент зависит от входных данных, что позволяет предположить
    # о незначимости учета продолжительности операций p при оптимизации времени индексации

    # Итог: оптимизация достигается за счет сортировки заданий по параметру f, сортировка
    # производится при помощи жадного алгоритма быстрой сортировки, действующего по
    # принципу "разделяй и властвуй". Временная сложность в общем случае равна O(n*log(n)),
    # что является наилучшим результатом для всех известных алгоритмов сортировки
