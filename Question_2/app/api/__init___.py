from model.QA_model import QA_model as model

model_name = "deepset/xlm-roberta-large-squad2"
model = model(model_name, model_name)