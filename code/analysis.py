import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import describe
import numpy as np

data_dir = 'out/'
out = 'analysis/'
os.makedirs(out, exist_ok=True)

pages = [
    'fest3.html',
    '4fest.html',
    '6fest.html',
    '7fest.html',
    '8fest.html',
    '9fest.html',
    '10fest.html',
]

tas = [
    'Kanika Rana',
    'Raghavendra Venkatesh',
    'Alex Knauth',
]

entries = []

for week in pages:

    max_score = None
    inspect_grades = {ta: [] for ta in tas}

    print(week)
    print('-' * 80)

    week_dir = os.path.join(data_dir, week)

    for group in os.listdir(week_dir):

        group_dir = os.path.join(week_dir, group)

        for report in os.listdir(group_dir):
            if not ('code-inspection' in report or 'comments' in report):
                continue

            lines = open(os.path.join(group_dir, report)).readlines()
            grader = lines[2].split(': ')[1].strip()

            # Get relevant details from the code inspectioon
            score = lines[1].split(': ')[1].strip()
            numerator = float(score.split('/')[0])
            divisor = float(score.split('/')[1])
            if not max_score: max_score = divisor
            if max_score != divisor:
                raise Exception('Found different max score!')

            print(group, score, grader)

            # Append an entry to the accumulator
            entries.append({
                'group': group,
                'score': numerator,
                'max_score': divisor,
                'norm_score': numerator / divisor,
                'grader': grader,
                'week': week
            })
            inspect_grades[grader].append(numerator)

    # Setup plot
    sns.set(style='white', palette='muted', color_codes=True)
    f, axes = plt.subplots(3, 1, figsize=(7, 7), sharex=True)
    sns.despine()

    # Something like 10-12 bins between 0 and max_score
    binning = binning = list(
        range(0, round(max_score + max_score / 10), max(
            1, int(max_score / 10))))

    for i, ta in enumerate(tas):
        grades = inspect_grades[ta]
        mean = np.mean(grades)
        count = len(grades)

        # Single TA histogram
        g = sns.distplot(
            grades,
            bins=binning,
            kde=False,
            rug=True,
            color=['b', 'r', 'g'][i],
            ax=axes[i]).set_title(ta)

        # Vertical mean line
        axes[i].axvline(
            np.mean(grades),
            color=['b', 'r', 'g'][i],
            linestyle='dashed',
            linewidth=1)

        # Mean and entrycount text
        y_min, y_max = axes[i].get_ylim()
        x_min, x_max = axes[i].get_xlim()
        axes[i].text(x_min + (x_max - x_min) / 20,
                     y_max - (y_max - y_min) / 10, 'Mean: {:.2f}'.format(mean))
        axes[i].text(x_min + (x_max - x_min) / 20, y_max - (y_max - y_min) / 5,
                     'Entries: {:.2f}'.format(count))

    f.suptitle(week + ' - Max score: ' + str(max_score))
    plt.savefig(os.path.join(out, week) + '.png')
    plt.close()

    print()

# Create a dataframe from each entry and produce the average over time plot
df = pd.DataFrame.from_records(entries)
sns.set(style="whitegrid")
g = sns.catplot(
    x="week",
    y="norm_score",
    hue="grader",
    kind="point",
    data=df,
    palette="YlGnBu_d",
    # dodge=True,
    ci=None,
    height=5,
    aspect=1.5)
plt.title("Average TA normalized grade over time")
plt.savefig(os.path.join(out, 'avg_trends.png'))
plt.show()