# Feature Engineering
def check(star_wars, predictors):

    from sklearn.feature_selection import SelectKBest, f_classif
    import numpy as np
    import matplotlib.pyplot as plt

    # Perform feature selection
    selector = SelectKBest(f_classif, k=5)
    selector.fit(star_wars[predictors], star_wars["IsStarWarsFan"])

    # Get the raw p-values for each feature, and transform from p-values into scores
    scores = -np.log10(selector.pvalues_)

    # Plot the scores.  See how "Pclass", "Sex", "Title", and "Fare" are the best?
    plt.bar(range(len(predictors)), scores)
    plt.xticks(range(len(predictors)), predictors, rotation='vertical')
    plt.show()