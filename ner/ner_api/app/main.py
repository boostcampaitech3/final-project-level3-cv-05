from __future__ import absolute_import, division, print_function, unicode_literals
from model.net import KobertCRF
from fastapi import FastAPI
from fastapi.param_functions import Depends
from typing import Dict, List, Tuple
from pydantic import BaseModel
from get_model import get_model, get_ner_result, get_vocab_tokenizer, get_ner_to_index, get_tokenizer
from get_name_entity import DecoderFromNamedEntitySequence


app = FastAPI()


class NamecardText(BaseModel):
    text: List[str]


async def get_result_list(ner_result: List) -> List:
    result_list = []

    for namecard in ner_result:
        dict_per_namecard = {'PER': [], 'ORG': []}
        for word_and_tag in namecard:
            word, tag = word_and_tag.values()
            if tag == 'PER':
                dict_per_namecard['PER'].append(word)
            elif tag == 'ORG':
                dict_per_namecard['ORG'].append(word)
        
        result_list.append(dict_per_namecard)
    return result_list


@app.post("/ner/")
async def get_ner_inference(namecard_text: NamecardText, 
                            model: KobertCRF = Depends(get_model), 
                            token_and_vocab: Tuple = Depends(get_vocab_tokenizer)) -> List[Dict]:
    """
    NER model inference 결과를 반환한다

    Args:
        namcard_text (NamecardText): 
            Key - 'text'
            Value - 각 명함의 text 내용이 문자열로 연결되어있는 List (각 명함마다 List의 str 원소 한 개)
        ex. {
                'text': 
                ['김민수 삼성전자 tom 서울특별시 박민수 영등포구 123-45 010-1234-5687', '경기도 수원시 장안구 010-5456-5654 이지연 LG전자']
            }
    Returns:
        각 명함마다 'PER', 'ORG' Tag 의 결과가 담긴 dict를 원소로 갖는 List
        ex. [{'PER': [' 김민수', ' 박민수'], 'ORG': [' 삼성전자']}, {'PER': [' 이지연'], 'ORG': [' LG전자']}]
    """
    all_text_list = namecard_text.text
    ptr_tokenizer, vocab = token_and_vocab
    tokenizer = await get_tokenizer(vocab, ptr_tokenizer)
    index_to_ner = await get_ner_to_index()
    decoder_from_res = DecoderFromNamedEntitySequence(tokenizer=tokenizer, index_to_ner=index_to_ner)
    model.eval()
    ner_result = await get_ner_result(all_text_list, tokenizer, model, decoder_from_res)
    result_list = await get_result_list(ner_result)
    return result_list