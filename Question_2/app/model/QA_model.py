from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

#model_name = "deepset/xlm-roberta-large-squad2"
class QA_model:

    def __init__(self, model_name, tokenizer):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=tokenizer)

    def get_time(self, context):
        """
        Get free time and busy time in passage.
        Args:
            context (str): is the passage want to get time.
        Returns:
            Return free time and busy time.
        """
        # Get free time
        QA_free = {
            'question' : "When is the free time?",
            'context' : context 
        }
        res_free = self.nlp(QA_free)

        # Get busy time
        QA_busy = {
            'question' : "When is the busy time?",
            'context' : context 
        }
        res_busy = self.nlp(QA_busy)
  
        return processing_time(res_free, res_busy)

def processing_time(res_free, res_busy):
    """
    Extract real time user avaiable or not.
    Args:
        res_free (respone of pipline): respone of pipline for free time in parse.
        res_busy : respone of pipline for busy time in parse.
    Return:
        Free time, Busy time
    """
    # Case of answer
    if res_free['answer'] not in res_busy['answer'] or res_busy['answer'] not in res_free['answer']:
        return res_free['answer'], res_busy['answer']
    
    if res_free['score'] >= res_busy['score'] :
        return res_free['answer'], None
    else:
        return None, res_busy['answer']

if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = QA_model(model_name, model_name)
    context = "My avaiable time includes Wednesday and Friday afternoons."
    free, busy = model.get_time(context)
    print( f"Free time: {free}, busy time: {busy}")