import sys
import pandas as pd
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import make_pipeline

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t')

for (max_depth, max_features, criterion) in itertools.product([1, 2, 3, 4, 5, 10, 20, 50, None],
                                                              [0.1, 0.25, 0.5, 0.75, 'sqrt', 'log2', None],
                                                              ['gini', 'entropy']):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            DecisionTreeClassifier(max_depth=max_depth,
                                                   max_features=max_features,
                                                   criterion=criterion))
        # 10-fold CV scores for the pipeline
        cv_scores = cross_val_score(estimator=clf, X=features, y=labels, cv=10)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'max_depth={},'.format(max_depth)
    param_string += 'max_features={},'.format(max_features)
    param_string += 'criterion={}'.format(criterion)

    for cv_score in cv_scores:
        out_text = '\t'.join([dataset.split('/')[-1][:-7],
                              'DecisionTreeClassifier',
                              param_string,
                              str(cv_score)])

        print(out_text)
        sys.stdout.flush()
