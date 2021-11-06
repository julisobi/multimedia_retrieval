from sklearn.metrics import accuracy_score
import pandas as pd
from distances import ann


def evaluate_meshes(excel_file):
    acc_list = 0
    acc_cat_list = []
    df = pd.read_excel(excel_file, index_col=0)
    for index, row in df.iterrows():
        file = row.values[0]
        category = file.split("/")[1]
        if file == "LabeledDB_new/Hand/subs_183.off":
            continue
        distances = ann(df, file, 10, 20)
        categories = [tup[1].split("/")[1] for tup in distances]
        y_pred = [1 if cat == category else 0 for cat in categories]
        y_true = [1] * 20
        acc = accuracy_score(y_true, y_pred)
        acc_list += acc
        acc_cat_list.append((acc, category))
    print(acc_cat_list)
    print(f"Airplane accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Airplane']) / 20}")
    print(f"Ant accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Ant']) / 20}")
    print(f"Armadillo accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Armadillo']) / 20}")
    print(f"Bearing accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Bearing']) / 20}")
    print(f"Bird accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Bird']) / 20}")
    print(f"Bust accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Bust']) / 20}")
    print(f"Chair accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Chair']) / 20}")
    print(f"Cup accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Cup']) / 20}")
    print(f"Fish accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Fish']) / 20}")
    print(f"FourLeg accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'FourLeg']) / 20}")
    print(f"Glasses accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Glasses']) / 20}")
    print(f"Hand accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Hand']) / 20}")
    print(f"Human accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Human']) / 20}")
    print(f"Mech accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Mech']) / 20}")
    print(f"Octopus accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Octopus']) / 20}")
    print(f"Plier accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Plier']) / 20}")
    print(f"Table accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Table']) / 20}")
    print(f"Teddy accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Teddy']) / 20}")
    print(f"Vase accuracy: {sum([e[0] for e in acc_cat_list if e[1] == 'Vase']) / 20}")



    print(acc_list / 380)


evaluate_meshes("normalized.xlsx")
