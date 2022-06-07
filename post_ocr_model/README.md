# Train
```
# model 경로에서 
python trainer.py --config [CONFIG DIR]
```
# 구조 
```bash
📂 post_ocr_model /
├── 📄 config.yaml
├── 📄 main.py
├── 📄 run.py
└── 📂 model /
    ├── 📄 __init__.py
    ├── 📄 config.yaml
    ├── 📄 dataset.py
    ├── 📄 feature_engineering.py
    ├── 📄 loss.py
    ├── 📄 model.py
    ├── 📄 rule_base_classification.py
    ├── 📄 tab_transform.py
    ├── 📄 tab_utils.py
    └── 📄 trainer.py

```  

# model files    
### Feature Engineering  
**01. tab_utils.py**  
- convert 'json' to 'dataframe'   
 
**02. tab_transform.py**   
- Feature Engineering 연산 및 적용

**03. feature engineering.py**   
- `tab_utils.py` 와 `tab_transform.py`를 통해 받은 json 데이터로부터 13개의 features를 만들고 이를 dataframe 형태로 반환  


### Train
**04. dataset.py**  
- 받은 명함 이미지를 bbox + margin 기준으로 cut    
- 자른 이미지, 자른 이미지의 json 데이터로 `feature engineering.py`를 통해 만든 13개의 features, 정답 category data로 반환   
- 반환된 데이터를 dataloader에 넣음  

**05. loss.py**  
- loss 정의 (cross_entropy, f1 loss)   

**06. model.py**  
- CNN모델을 통해 이미지에서 뽑은 1000개의 features   
- MLP모델을 통해 13개의 features에서 뽑은 100개의 features   
- 총 1100개의 features을 통해 MLP모델로 classifier   

**07. trainer.py**  
- pytorch_lightning을 이용하여 `dataset.py`의 dataloader로 불러온 데이터들을 `model.py`의 learner를 통해 모델 학습   

### Etc.
**07. \__init__.py**   
- get_model : pretrained checkpoints 파일을 통해 학습시킨 모델 반환   
- inference : test이미지 내 각 bbox + margin 이미지에 대하여 category 예측값 반환 

