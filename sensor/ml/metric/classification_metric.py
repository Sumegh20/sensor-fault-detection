# from sensor.entity.artifact_entity import ClassificationMetricArtifact
# from sensor.exception import SensorException
# from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
# import os, sys

# def calculate_metric(model, x, y) -> ClassificationMetricArtifact:
#     """
#     model: estimator
#     x: input feature
#     y: output feature
#     """
#     yhat = model.predict(x)

#     classification_metric = ClassificationMetricArtifact(
#         f1_score=f1_score(y, yhat),
#         recall_score=recall_score(y, yhat),
#         precision_score=precision_score(y, yhat),
#     )

#     return classification_metric


# def total_cost(y_true, y_pred):
#     """
#     This function takes y_ture, y_predicted, and prints Total cost due to misclassification
#     """
#     tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

#     cost = 10 * fp + 500 * fn

#     return cost


from sensor.entity.artifact_entity import ClassificationMetricArtifact
from sensor.exception import SensorException
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
import os, sys



def get_classification_score(y_true, y_pred)->ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true, y_pred)
        model_recall_score = recall_score(y_true, y_pred)
        model_precision_score = precision_score(y_true, y_pred)

        classification_metric = ClassificationMetricArtifact(f1_score=model_f1_score, recall_score=model_recall_score, precision_score=model_precision_score)
        return classification_metric
    except Exception as e:
        raise SensorException(e, sys)
