from pyltp import Segmentor
from pyltp import SentenceSplitter


_segmentor = None
_sent_splitter = None

def split(content):
    '''分句和分词'''
    global _segmentor, _sent_splitter
    if _segmentor is None:
        model_path = r'ltp_data_v3.4.0/cws.model'
        segmentor = Segmentor()  # 初始化实例
        segmentor.load(model_path) # 加载分词模型
        _segmentor = segmentor  # 设置全局变量, 避免每次都重新加载模型, 耗时
        _sent_splitter = SentenceSplitter() # 句子分割模型
    sents = _sent_splitter.split(content)  # 先进行分句
    _sents = []
    for sent in sents:
        words = _segmentor.segment(sent) # 分词
        sent = ' '.join(words) # 用空格把词隔开
        _sents.append(sent)
    content = '. '.join(_sents)  # 用.把句子隔开
    return content


def clean(content):
    content = content.replace('.', '') # 删除句子分隔符
    content = content.replace(' ', '') # 删除空格
    return content


if __name__=="__main__":
    from gensim.summarization.summarizer import summarize
    with open("report2.txt", "r") as myfile:
        content = "".join(myfile.readlines()[1:])
    print(f'\033[92m原文\033[0m: {content}')
    tokens = split(content)
    print(f'\033[92m分词\033[0m: {tokens}')
    word_count = 100
    result = summarize(text=tokens, word_count=word_count)
    result = clean(result)
    print(f'\033[92m{word_count} 字总结:\033[0m {result}')
