import pandas as pd
import Cleaner
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
import FeatureSelector

# read csv

star_wars = pd.read_csv("star_wars.csv", encoding="ISO-8859-1")

# clean data

star_wars = Cleaner.clean(star_wars)

# split into train and test data
star_wars_train = star_wars[:-200]
star_wars_test = star_wars[-200:]


# Initialize our algorithm with the default paramters
# n_estimators is the number of trees we want to make
# min_samples_split is the minimum number of rows we need to make a split
# min_samples_leaf is the minimum number of samples we can have at the place where a tree branch ends (the bottom points of the tree)
alg = RandomForestClassifier(random_state=1, n_estimators=10, min_samples_split=2, min_samples_leaf=1)

# Set predictors
predictors = ["SeenSW", "IsStarTrekFan", "Gender", "Age", "Income", "Education", "Location"]

# uncomment to check what features to use
# FeatureSelector.check(star_wars, predictors)

# Fit the algorithm using the full training data.
alg.fit(star_wars_train[predictors], star_wars_train["IsStarWarsFan"])
# Predict using the test dataset.  We have to convert all the columns to floats to avoid an error.
predictions = alg.predict_proba(star_wars_test[predictors].astype(float))[:,1]

predictions[predictions > 0.5] = 1
predictions[predictions <= 0.5] = 0

predictions = predictions.astype(int)

submission = pd.DataFrame({
        "Id": star_wars_test["RespondentID"],
        "IsStarWarsFan": predictions
    })

print(submission.head(10))

# get score
scores = cross_validation.cross_val_score(alg, star_wars[predictors], star_wars['IsStarWarsFan'], cv=3)

print(scores.mean())




