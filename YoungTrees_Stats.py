import matplotlib.pyplot as plt
import pandas as pd

young_trees_csv = "J:\\GISprojects\\YoungTrees\\YoungTrees.csv"

plt.style.use('seaborn-whitegrid')

date_thresholds = [1000, 1700, 1800, 1900, 1950, 2000, 2010, 2015]
models = ['s1', 's1_s2']
df = pd.read_csv(young_trees_csv)

for date_threshold in date_thresholds:

    date_range = None
    if date_threshold == 1000:
        date_range = "All Data"
    else:
        date_range = "Post {}".format(date_threshold)
    print("{:=^80}".format("Accuracy Report - {}".format(date_range)))


    threshold_data = df[(df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')]

    data_within_threshold = len(threshold_data.index)
    print("Sample size: {}".format(data_within_threshold))

    true_positive = df[(df["restock_ind"] == 1) & (df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                             & (df["min_PLYEAR_AGREED"] is not 'NA')]
    true_negative = df[(df["restock_ind"] == 0) & (df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                       & (df["min_PLYEAR_AGREED"] is not 'NA')]
    false_positive = df[(df["restock_ind"] == 0) & (df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                        & (df["min_PLYEAR_AGREED"] is not 'NA')]
    false_negative = df[(df["restock_ind"] == 1) & (df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                        & (df["min_PLYEAR_AGREED"] is not 'NA')]

    tp_count = len(true_positive.index)
    tp_percentage = tp_count/data_within_threshold*100
    print("\tTrue Positives: {}({:.3f}%)".format(tp_count, tp_percentage))
    tn_count = len(true_negative.index)
    tn_percentage = tn_count/data_within_threshold*100
    print("\tTrue Negative: {}({:.3f}%)".format(tn_count, tn_percentage))
    fp_count = len(false_positive.index)
    fp_percentage = fp_count/data_within_threshold*100
    print("\tFalse Positives: {}({:.3f}%)".format(fp_count, fp_percentage))
    fn_count = len(false_negative.index)
    fn_percentage = fn_count/data_within_threshold*100
    print("\tFalse Positives: {}({:.3f}%)".format(fn_count, fn_percentage))

    print("Total Accuracy: {}({:.3f})%\n".format(tp_count+tn_count, tp_percentage+tn_percentage))

    min_young_trees = df[(df["min_PLYEAR_AGREED"] >= int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')]
    max_young_trees = df[(df["max_PLYEAR_AGREED"] >= int(date_threshold)) & (df["max_PLYEAR_AGREED"] is not 'NA')]


    min_a_young_trees_year_prob = min_young_trees[["min_PLYEAR_AGREED", "prob_2021"]]
    max_a_young_trees_year_prob = max_young_trees[["max_PLYEAR_AGREED", "prob_2021"]]
    min_young_trees_year_prob = min_young_trees[["min_PLYR", "prob_2021"]]
    max_young_trees_year_prob = max_young_trees[["max_PLYR", "prob_2021"]]

    print("Covariance")
    cov_min_a = (min_a_young_trees_year_prob.cov().iloc[0, 1])
    cov_max_a = (max_a_young_trees_year_prob.cov().iloc[0, 1])
    cov_min = (min_young_trees_year_prob.cov().iloc[0, 1])
    cov_max = (max_young_trees_year_prob.cov().iloc[0, 1])
    print("\tMin Agreed Planting Year vs Probability: {:.3f}".format(cov_min_a))
    print("\tMax Agreed Planting Year vs Probability: {:.3f}".format(cov_max_a))
    print("\tMin Planting Year vs Probability: {:.3f}".format(cov_min))
    print("\tMax Planting Year vs Probability: {:.3f}".format(cov_max))

    print("Pearson correlation")
    pc_min_a = min_a_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
    pc_max_a = max_a_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
    pc_min = min_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
    pc_max = max_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
    print("\tMin Agreed Planting Year vs Probability: {:.3f}".format(pc_min_a))
    print("\tMax Agreed Planting Year vs Probability: {:.3f}".format(pc_max_a))
    print("\tMin Planting Year vs Probability: {:.3f}".format(pc_min))
    print("\tMax Planting Year vs Probability: {:.3f}".format(pc_max))

    for model in models:

        print("{:-^80}".format("Model - {}".format(model)))

        model_threshold_data = df[(df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')
                                  & (df["model_2021"] == model)]
        model_data_within_threshold = len(model_threshold_data.index)
        print("Sample size: {}".format(model_data_within_threshold))

        model_true_positive = df[(df["restock_ind"] == 1) & (df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                                 & (df["min_PLYEAR_AGREED"] is not 'NA') & (df["model_2021"] == model)]
        model_true_negative = df[(df["restock_ind"] == 0) & (df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                                 & (df["min_PLYEAR_AGREED"] is not 'NA') & (df["model_2021"] == model)]
        model_false_positive = df[(df["restock_ind"] == 0) & (df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                                  & (df["min_PLYEAR_AGREED"] is not 'NA') & (df["model_2021"] == model)]
        model_false_negative = df[(df["restock_ind"] == 1) & (df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold))
                                  & (df["min_PLYEAR_AGREED"] is not 'NA') & (df["model_2021"] == model)]

        model_tp_count = len(model_true_positive.index)
        model_tp_percentage =  model_tp_count/model_data_within_threshold*100
        print("\tTrue Positives: {}({:.3f}%)".format(model_tp_count, model_tp_percentage))
        model_tn_count = len(model_true_negative.index)
        model_tn_percentage = model_tn_count/model_data_within_threshold*100
        print("\tTrue Negative: {}({:.3f}%)".format(model_tn_count, model_tn_percentage))
        model_fp_count = len(model_false_positive.index)
        model_fp_percentage = model_fp_count/model_data_within_threshold*100
        print("\tFalse Positives: {}({:.3f}%)".format(model_fp_count, model_fp_percentage))
        model_fn_count = len(model_false_negative.index)
        model_fn_percentage = model_fn_count/model_data_within_threshold*100
        print("\tFalse Negative: {}({:.3f}%)".format(model_fn_count, model_fn_percentage))

        print("Total Accuracy: {}({:.3f})%\n".format(model_tp_count+model_tn_count, model_tp_percentage+tn_percentage))

        model_min_young_trees = df[(df["min_PLYEAR_AGREED"] >= int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')
                                   & (df["model_2021"] == model)]
        model_max_young_trees = df[(df["max_PLYEAR_AGREED"] >= int(date_threshold)) & (df["max_PLYEAR_AGREED"] is not 'NA')
                                   & (df["model_2021"] == model)]

        model_min_a_young_trees_year_prob = model_min_young_trees[["min_PLYEAR_AGREED", "prob_2021"]]
        model_max_a_young_trees_year_prob = model_max_young_trees[["max_PLYEAR_AGREED", "prob_2021"]]
        model_min_young_trees_year_prob = model_min_young_trees[["min_PLYR", "prob_2021"]]
        model_max_young_trees_year_prob = max_young_trees[["max_PLYR", "prob_2021"]]

        print("Covariance")
        model_cov_min_a = (model_min_a_young_trees_year_prob.cov().iloc[0, 1])
        model_cov_max_a = (model_max_a_young_trees_year_prob.cov().iloc[0, 1])
        model_cov_min = (model_min_young_trees_year_prob.cov().iloc[0, 1])
        model_cov_max = (model_max_young_trees_year_prob.cov().iloc[0, 1])
        print("\tMin Agreed Planting Year vs Probability: {:.3f}".format(model_cov_min_a))
        print("\tMax Agreed Planting Year vs Probability: {:.3f}".format(model_cov_max_a))
        print("\tMin Planting Year vs Probability: {:.3f}".format(model_cov_min))
        print("\tMax Planting Year vs Probability: {:.3f}".format(model_cov_max))

        print("Pearson correlation")
        model_pc_min_a = model_min_a_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
        model_pc_max_a = model_max_a_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
        model_pc_min = model_min_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
        model_pc_max = model_max_young_trees_year_prob.corr(method='pearson', min_periods=1).iloc[0, 1]
        print("\tMin Agreed Planting Year vs Probability: {:.3f}".format(model_pc_min_a))
        print("\tMax Agreed Planting Year vs Probability: {:.3f}".format(model_pc_max_a))
        print("\tMin Planting Year vs Probability: {:.3f}".format(model_pc_min))
        print("\tMax Planting Year vs Probability: {:.3f}".format(model_pc_max))

    # min_young_trees = df[(df["min_PLYEAR_AGREED"] >= int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')]
    # max_young_trees = df[(df["max_PLYEAR_AGREED"] >= int(date_threshold)) & (df["max_PLYEAR_AGREED"] is not 'NA')]
    # print("Length of Min Agreed Dataset: {}".format(len(min_young_trees.index)))
    # print("Length of Max Agreed Dataset: {}".format(len(max_young_trees.index)))
    #
    min_restocked = df[(df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')]
    min_not_restocked = df[(df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["min_PLYEAR_AGREED"] is not 'NA')]
    max_restocked = df[(df["class_2021"] == 1) & (df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["max_PLYEAR_AGREED"] is not 'NA')]
    max_not_restocked = df[(df["class_2021"] == 0) & (df["min_PLYEAR_AGREED"] > int(date_threshold)) & (df["max_PLYEAR_AGREED"] is not 'NA')]

    plt.plot(min_restocked.min_PLYEAR_AGREED, min_restocked.prob_2021,'o',markersize=2, color='green')
    plt.plot(max_not_restocked.max_PLYEAR_AGREED, min_not_restocked.prob_2021,'o',markersize=2, color='red')
    plt.title('Maximum Plant Year -  Agreed - {}'.format(date_threshold))
    plt.xlabel('Year')
    plt.ylabel('Restock Probability')
    plt.show()

    plt.plot(max_restocked.max_PLYEAR_AGREED, max_restocked.prob_2021,'o',markersize=2, color='green')
    plt.plot(max_not_restocked.max_PLYEAR_AGREED, max_not_restocked.prob_2021,'o',markersize=2, color='red')
    plt.title('Minimum Plant Year -  Agreed 0 {}'.format(date_threshold))
    plt.xlabel('Year')
    plt.ylabel('Restock Probability')
    plt.show()


