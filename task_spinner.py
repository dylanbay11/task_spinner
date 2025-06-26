import marimo

__generated_with = "0.14.0"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import random
    import numpy as np
    from typing import List, Tuple


@app.function
def calculate_weighted_selection(critical_tasks: List[str], 
                               important_tasks: List[str], 
                               maintenance_tasks: List[str]) -> str:
    """
    Calculate weighted random selection with fixed 15% break probability
    
    Weights:
    - Critical: 6x weight
    - Important: 2x weight  
    - Maintenance: 1x weight
    - Take a Break: Fixed 15% probability
    """
    
    # Filter out empty tasks
    critical_tasks = [task for task in critical_tasks if task.strip()]
    important_tasks = [task for task in important_tasks if task.strip()]
    maintenance_tasks = [task for task in maintenance_tasks if task.strip()]
    
    # First check if we should take a break (15% probability)
    if random.random() < 0.15:
        return "🌟 Take a Break! 🌟\n\nTime to rest and recharge. Take 15-20 minutes to step away from your tasks."
    
    # If no break, proceed with weighted selection of tasks
    all_tasks = []
    weights = []
    
    # Add critical tasks with 6x weight
    for task in critical_tasks:
        all_tasks.append(f"🔥 CRITICAL: {task}")
        weights.append(6)
    
    # Add important tasks with 2x weight
    for task in important_tasks:
        all_tasks.append(f"⭐ IMPORTANT: {task}")
        weights.append(2)
    
    # Add maintenance tasks with 1x weight
    for task in maintenance_tasks:
        all_tasks.append(f"🔧 MAINTENANCE: {task}")
        weights.append(1)
    
    # If no tasks are entered, return helpful message
    if not all_tasks:
        return "📝 Please enter at least one task to get started!"
    
    # Weighted random selection
    selected_task = random.choices(all_tasks, weights=weights, k=1)[0]

    return selected_task


@app.function
def create_task_spinner():
    """Create a weighted task spinner interface for marimo notebook"""
    
    # UI Components for task input
    critical_inputs = [
        mo.ui.text(placeholder=f"Critical Task {i+1}", label=f"Critical Task {i+1}") 
        for i in range(3)
    ]
    
    important_inputs = [
        mo.ui.text(placeholder=f"Important Task {i+1}", label=f"Important Task {i+1}") 
        for i in range(4)
    ]
    
    maintenance_inputs = [
        mo.ui.text(placeholder=f"Maintenance Task {i+1}", label=f"Maintenance Task {i+1}") 
        for i in range(5)
    ]
    
    # Spin button
    spin_button = mo.ui.button(label="🎯 Spin for Next Task", kind="success")
    
    # Display the input form
    input_form = mo.vstack([
        mo.md("## 🎯 Weighted Task Spinner"),
        mo.md("### Critical Tasks (High Priority)"),
        mo.vstack(critical_inputs),
        mo.md("### Important Tasks (Medium Priority)"),
        mo.vstack(important_inputs),
        mo.md("### Maintenance Tasks (Low Priority)"),
        mo.vstack(maintenance_inputs),
        mo.md("---"),
        spin_button
    ])
    
    return input_form, critical_inputs, important_inputs, maintenance_inputs, spin_button


@app.function
def display_task_statistics(critical_tasks: List[str], 
                          important_tasks: List[str], 
                          maintenance_tasks: List[str]):
    """Display statistics about task distribution and probabilities"""
    
    # Filter out empty tasks
    critical_count = len([task for task in critical_tasks if task.strip()])
    important_count = len([task for task in important_tasks if task.strip()])
    maintenance_count = len([task for task in maintenance_tasks if task.strip()])
    
    total_tasks = critical_count + important_count + maintenance_count
    
    if total_tasks == 0:
        return mo.md("Enter some tasks to see probability statistics!")
    
    # Calculate total weight (excluding break)
    total_weight = (critical_count * 6) + (important_count * 2) + (maintenance_count * 1)
    
    # Calculate probabilities (85% of the time, since break is 15%)
    critical_prob = (critical_count * 6 / total_weight) * 0.85 if total_weight > 0 else 0
    important_prob = (important_count * 2 / total_weight) * 0.85 if total_weight > 0 else 0
    maintenance_prob = (maintenance_count * 1 / total_weight) * 0.85 if total_weight > 0 else 0
    break_prob = 0.15
    
    stats_text = f"""
    ## 📊 Task Selection Probabilities
    
    **Total Tasks:** {total_tasks}
    
    - 🔥 **Critical Tasks:** {critical_prob:.1%} chance ({critical_count} tasks)
    - ⭐ **Important Tasks:** {important_prob:.1%} chance ({important_count} tasks)
    - 🔧 **Maintenance Tasks:** {maintenance_prob:.1%} chance ({maintenance_count} tasks)
    - 🌟 **Take a Break:** {break_prob:.1%} chance (fixed)
    
    ---
    *Critical tasks are 6x more likely than maintenance tasks*
    *Important tasks are 2x more likely than maintenance tasks*
    """
    
    return mo.md(stats_text)


@app.cell
def _():
    # Create the main interface
    form, critical_inputs, important_inputs, maintenance_inputs, spin_button = create_task_spinner()
    return (
        critical_inputs,
        form,
        important_inputs,
        maintenance_inputs,
        spin_button,
    )


@app.cell
def _(
    critical_inputs,
    form,
    important_inputs,
    maintenance_inputs,
    spin_button,
):
    # Process the spin when button is clicked
    if spin_button.value:
        # Get current task values
        critical_tasks = [inp.value for inp in critical_inputs]
        important_tasks = [inp.value for inp in important_inputs] 
        maintenance_tasks = [inp.value for inp in maintenance_inputs]
    
        # Get the selected task
        selected_task = calculate_weighted_selection(critical_tasks, important_tasks, maintenance_tasks)
    
        # Display results
        result_display = mo.vstack([
            mo.md("## 🎲 Your Next Task:"),
            mo.md(f"### {selected_task}"),
            mo.md("---"),
            display_task_statistics(critical_tasks, important_tasks, maintenance_tasks)
        ])
    else:
        # Display statistics without selection
        critical_tasks = [inp.value for inp in critical_inputs]
        important_tasks = [inp.value for inp in important_inputs]
        maintenance_tasks = [inp.value for inp in maintenance_inputs]
    
        result_display = display_task_statistics(critical_tasks, important_tasks, maintenance_tasks)

    # Display the complete interface
    mo.vstack([
        form,
        mo.md("---"),
        result_display
    ])
    return


if __name__ == "__main__":
    app.run()
