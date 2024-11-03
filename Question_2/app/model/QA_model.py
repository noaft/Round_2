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
            'question' : 'When is the free time time in the passage?',
            'context' : context 
        }
        res = self.nlp(QA_free)
        free_time = res['answer']

        # Get busy time
        QA_busy = {
            'question' : 'When is the busy time time in the passage?',
            'context' : context 
        }
        res = self.nlp(QA_busy)
        busy_time = res['answer']

        return free_time , busy_time

if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = QA_model(model_name, model_name)
    context = 'I am free on Tuesday afternoons and Thursday mornings, but I am unavailable every Monday and Wednesday, I have free time every night. Balancing our schedules will help maximize attendance.'
    free, busy = model.get_time(context)
    print( f"Free time: {free}, busy time: {busy}")