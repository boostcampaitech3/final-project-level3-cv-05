import torch
import json
import yaml
import pickle
from typing import Dict, List, Tuple
from pathlib import Path
from data_utils.vocab_tokenizer import Vocabulary
from data_utils.vocab_tokenizer import Tokenizer
from data_utils.pad_sequence import keras_pad_fn
from data_utils.utils import Config
from model.net import KobertCRF
from fastapi.param_functions import Depends
from gluonnlp.data import SentencepieceTokenizer


with open("configs/config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

tok_path = config['tok_path']
checkpoint_path = config['checkpoint_path']
model_dir = Path(config['model_dir'])
model_config = Config(json_path=config['model_config'])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


async def get_vocab_tokenizer(tok_path: str = tok_path) -> Tuple[SentencepieceTokenizer, Vocabulary]:
    ptr_tokenizer = SentencepieceTokenizer(tok_path)

    with open(model_dir / "vocab.pkl", 'rb') as f:
        vocab = pickle.load(f)
    return ptr_tokenizer, vocab


async def get_tokenizer(vocab, ptr_tokenizer) -> Tokenizer:
    tokenizer = Tokenizer(vocab=vocab, split_fn=ptr_tokenizer, pad_fn=keras_pad_fn, maxlen=model_config.maxlen)
    return tokenizer


async def get_model(model_config = model_config,
            checkpoint_path: str = checkpoint_path,
            token_and_vocab: Tuple = Depends(get_vocab_tokenizer)
            ) -> KobertCRF:
    """
        KobertCRT Model 을 반환합니다
    """

    len_ner_to_index = 25
    _, vocab = token_and_vocab
    model = KobertCRF(config=model_config, num_classes=len_ner_to_index, vocab=vocab)
    model_dict = model.state_dict()

    if checkpoint_path:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
        convert_keys = {}
        for k, v in checkpoint['model_state_dict'].items():
            new_key_name = k.replace("module.", '')
            if new_key_name not in model_dict:
                print("{} is not int model_dict".format(new_key_name))
                continue
            convert_keys[new_key_name] = v

        model.load_state_dict(convert_keys)
    
    model.to(device)
    return model


async def get_ner_result(all_text_list: List, tokenizer: Tokenizer, model: KobertCRF, decoder_from_res: List) -> List:
    ner_result = []
    
    for input_text in all_text_list:
        
        list_of_input_ids = tokenizer.list_of_string_to_list_of_cls_sep_token_ids([input_text])
        x_input = torch.tensor(list_of_input_ids).long().to(device)
        list_of_pred_ids = model(x_input)

        list_of_ner_word = decoder_from_res(list_of_input_ids=list_of_input_ids, list_of_pred_ids=list_of_pred_ids)
        ner_result.append([word for word in list_of_ner_word if word['tag'] == 'PER' or word['tag'] == 'ORG'])
    return ner_result


async def get_ner_to_index(model_dir: Path = model_dir) -> Tuple[Dict, Dict]:
    with open(model_dir / "ner_to_index.json", 'rb') as f:
        ner_to_index = json.load(f)
        index_to_ner = {v: k for k, v in ner_to_index.items()}
    return index_to_ner