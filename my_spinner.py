# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    """
    my_spinner.py

    A marimo applet that will assign you a task from an importance-weighted task list to do.
    This leverages psychology and neuroscience research, plus the benefits of statistical randomness!
    It also serves as a fun project to grow familiar with marimo's reactivity.

    Author: Dylan Bay
    """

    from dataclasses import dataclass
    from enum import Enum
    from math import isclose
    from random import choices
    from statistics import mean
    from typing import Optional, List

    import altair as alt  # visualization
    # import numpy as np    # not needed?
    # import polars as pl   # track results later?

    # global presets
    DEFAULT_MULTIPLIERS = {"Critical": 5, "Important": 2, "Maintenance": 1}
    return (
        DEFAULT_MULTIPLIERS,
        Enum,
        List,
        Optional,
        alt,
        dataclass,
        isclose,
        mo,
    )


@app.cell
def _(Enum, Optional, dataclass):
    class Priority(Enum):
        """Task priority level.

        Described elsewhere as, roughly:
        CRITICAL: A critical, high-impact, strategic, or time-sensitive task
        IMPORTANT: An important, helpful, or semi-flexible task
        MAINTENANCE: A maintenance or minor task
        """  

        CRITICAL = "Critical"
        IMPORTANT = "Important"
        MAINTENANCE = "Maintenance"

    @dataclass
    class Task:
        """A single task with a name (description) and priority (Enum-enforced)"""

        name: str
        priority: Priority

    @dataclass
    class WeightedTask:
        """A cousin to Task, has a weight assigned and allowed to be a break.

        Breaks are priority None, and also have the is_break flag.
        """

        name: str
        weight: float
        priority: Optional[Priority]
        is_break: bool = False
    return Priority, Task, WeightedTask


@app.cell
def _(DEFAULT_MULTIPLIERS, List, Task, WeightedTask, alt, altair):
    def weighted_categories(
        tlist: List[Task], 
        include_break: bool = True, 
        break_weight: float = .15,
        debug: bool = False
    ) -> List[WeightedTask]:
        """Create WeightedTask list from Task list, with a break addition optional.

        Note that break_weight is meaningless if include_break is not set.
        break_weight should be between 0 and 1, but will interpret 1 to 99.9 as percentages.
        """

        if (break_weight < 0) or (break_weight >= 100):
            raise ValueError("break_weight must be a probability (between 0 and 1 noninclusive)")
            # i.e. will not allow a guaranteed break, or related easter egg (for now!)
        elif break_weight == 0:
            include_break = False
        elif 1 < break_weight < 100:
            break_weight /= 100
        # else 0 < break_weight < 1 as intended
        if debug: print(f"break_weight: {break_weight}")

        wtlist: List[WeightedTask] = []
        if include_break:
            wtlist.append(WeightedTask("Break", break_weight, None, True))
        total_weight = sum([DEFAULT_MULTIPLIERS[t.priority.value] for t in tlist])
        if debug: print(f"total_weight: {total_weight}")
        for t in tlist: 
            if include_break:
                t_weight = DEFAULT_MULTIPLIERS[t.priority.value] * (1 - break_weight) / total_weight
            else: 
                t_weight = DEFAULT_MULTIPLIERS[t.priority.value] / total_weight
            if debug: print(f"Appending: {t.name}, {t_weight}, {t.priority}, False")
            wtlist.append(WeightedTask(t.name, t_weight, t.priority, False))

        return wtlist

    def graph_weights(tlist: List[Task], graph_type: str = "pie") -> alt.Chart:
        """Create and display an altair chart of what the spinner final weights look like

        Takes a list of tasks, optionally produces stacked "bar" chart, returns the chart
        """

        return altair.Chart([]).properties(title = "PLACEHOLDER CHART")
    return (weighted_categories,)


@app.cell
def _(Priority, Task, mo):
    # an initial template tasklist
    tasklist: list[Task] = [
        *[Task("A critical, high-impact, strategic, or time-sensitive task", 
               Priority.CRITICAL) for _ in range(3)],
        *[Task("An important, helpful, or semi-flexible task", 
               Priority.IMPORTANT) for _ in range(4)],
        *[Task("A maintenance or minor task", 
               Priority.MAINTENANCE) for _ in range(5)],
    ]

    tasklist_interactable = ti = mo.ui.array([
         *[mo.ui.dictionary({"Task": mo.ui.text(
                                 value = task.name, 
                                 full_width = True),  # debounce = 400?
                             "Priority": mo.ui.dropdown(
                                 options = [p.value for p in Priority], 
                                 value = task.priority.value)
         }) for task in tasklist]
    ])
    tasklist_interactable

    #TODO: need a BUTTON for adding and removing rows! 
    #TODO: Change the way this renders. I want it to have headers, auto-grouping by task priority if possible?
    return (tasklist_interactable,)


@app.cell
def _(Priority, Task, tasklist_interactable):
    tasklist_current = [Task(row["Task"], Priority(row["Priority"])) 
                        for row in tasklist_interactable.value]

    tasklist_current
    # this seems to properly update by reference from previous cells
    return (tasklist_current,)


@app.cell
def _(isclose, tasklist_current, weighted_categories):
    wt_test = weighted_categories(tasklist_current, debug=True)
    wt_test
    assert (isclose(sum([wt_task.weight for wt_task in wt_test]), 1.0, abs_tol=0.001), 
            "The total probability must be 1!")
    return


if __name__ == "__main__":
    app.run()
