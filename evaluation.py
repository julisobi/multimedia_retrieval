import pandas as pd
from distances import ann
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------------------------------------
# This file contains functions to compute evaluation metrics and plot those values.
# -----------------------------------------------------------------------------------------------------------


def evaluate_meshes(excel_file):
    total_acc, total_prec, total_recc = 0, 0, 0
    acc_prec_recc_cat_list = []
    df = pd.read_excel(excel_file, index_col=0)
    for index, row in df.iterrows():
        file = row.values[0]
        category = file.split("/")[1]
        if file == "LabeledDB_new/Hand/subs_183.off":
            continue
        distances = ann(df, file, 15, 20)
        categories = [tup[1].split("/")[1] for tup in distances]
        y_pred = [1 if cat == category else 0 for cat in categories]
        TP = y_pred.count(1)
        FP = y_pred.count(0)
        FN = 20 - TP
        TN = 360 - FP
        acc = (TP + TN) / (TP + TN + FP + FN)
        prec = TP / (TP + FP)
        rec = TP / (TP + FN)
        total_acc += acc
        total_prec += prec
        total_recc += rec
        acc_prec_recc_cat_list.append((acc, prec, rec, category))
    print(
        f"Airplane accuracy, precision, recall: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Airplane']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Airplane']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Airplane']) / 20}")
    print(
        f"Ant accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Ant']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Ant']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Ant']) / 20}")
    print(
        f"Armadillo accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Armadillo']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Armadillo']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Armadillo']) / 20}")
    print(
        f"Bearing accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Bearing']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Bearing']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Bearing']) / 20}")
    print(
        f"Bird accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Bird']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Bird']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Bird']) / 20}")
    print(
        f"Bust accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Bust']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Bust']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Bust']) / 20}")
    print(
        f"Chair accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Chair']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Chair']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Chair']) / 20}")
    print(
        f"Cup accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Cup']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Cup']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Cup']) / 20}")
    print(
        f"Fish accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Fish']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Fish']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Fish']) / 20}")
    print(
        f"FourLeg accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'FourLeg']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'FourLeg']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'FourLeg']) / 20}")
    print(
        f"Glasses accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Glasses']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Glasses']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Glasses']) / 20}")
    print(
        f"Hand accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Hand']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Hand']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Hand']) / 20}")
    print(
        f"Human accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Human']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Human']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Human']) / 20}")
    print(
        f"Mech accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Mech']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Mech']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Mech']) / 20}")
    print(
        f"Octopus accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Octopus']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Octopus']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Octopus']) / 20}")
    print(
        f"Plier accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Plier']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Plier']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Plier']) / 20}")
    print(
        f"Table accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Table']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Table']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Table']) / 20}")
    print(
        f"Teddy accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Teddy']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Teddy']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Teddy']) / 20}")
    print(
        f"Vase accuracy: {sum([e[0] for e in acc_prec_recc_cat_list if e[3] == 'Vase']) / 20}, {sum([e[1] for e in acc_prec_recc_cat_list if e[3] == 'Vase']) / 20}, {sum([e[2] for e in acc_prec_recc_cat_list if e[3] == 'Vase']) / 20}")

    print(f"Total accuracy: {total_acc / 380}")
    print(f"Total precision: {total_prec / 380}")
    print(f"Total recall: {total_recc / 380}")

    return acc_prec_recc_cat_list


def histograms(results_list):
    categories = ['Airplane', 'Ant', 'Armadillo', 'Bearing', 'Bird', 'Bust', 'Chair', 'Cup', 'Fish', 'FourLeg',
                  'Glasses', 'Hand', 'Human', 'Mech', 'Octopus', 'Plier', 'Table', 'Teddy', 'Vase']
    acc, prec, rec = [], [], []
    results = []
    for cat in categories:
        results.append((cat, sum([e[0] for e in results_list if e[3] == cat]) / 20,
                        sum([e[1] for e in results_list if e[3] == cat]) / 20,
                        sum([e[2] for e in results_list if e[3] == cat]) / 20))
        acc.append(sum([e[0] for e in results_list if e[3] == cat]) / 20)
        prec.append(sum([e[1] for e in results_list if e[3] == cat]) / 20)
        rec.append(sum([e[2] for e in results_list if e[3] == cat]) / 20)
    results.sort(key=lambda tup: tup[1], reverse=True)

    x = np.arange(len(categories))
    width = 0.2

    acc_sorted = [tup[1] for tup in results]
    prec_sorted = [tup[2] for tup in results]
    rec_sorted = [tup[3] for tup in results]
    cat_sorted = [tup[0] for tup in results]
    fig, ax = plt.subplots()
    ax.bar(x - width, acc_sorted, width, label='accuracy')
    ax.bar(x, prec_sorted, width, label='precision')
    ax.bar(x + width, rec_sorted, width, label='recall')
    ax.set_ylabel('Results')
    ax.set_xticks(x)
    ax.set_xticklabels(cat_sorted)
    plt.xticks(rotation=90)
    ax.legend()
    plt.show()


# MAIN
# evaluate_meshes("normalized.xlsx")
# histograms(evaluate_meshes("normalized.xlsx"))
