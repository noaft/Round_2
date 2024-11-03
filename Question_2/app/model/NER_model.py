import spacy

class NER_model:

    def __init__(self, model_name):
        self.nlp = spacy.load("en_core_web_sm")

    def detect_date_entities(self, doc):
        """
        Extracts named entities from a given document using the provided NLP model.
        
        Args:
            doc (str): The input text document from which to extract entities.
        
        Returns:
            list: A list of tuples containing the extracted entities if their corresponding label is "Date" and "Time.
        """
        doc_ = self.nlp(doc)
        result = []
        for ent in doc_.ents:
            if ent.label_ in ["DATE", "TIME"]:
                result.append([ent.text, ent.label_])

if __name__ == '__main__':
    # test
    # python3 -m spacy install en_core_web_sm
    model = NER_model("en_core_web_sm")
    detect = model.detect_date_entities("I am free on Tuesday afternoons and Thursday mornings, but I am unavailable every Monday and Wednesday, I have free time every night. Balancing our schedules will help maximize attendance.")
    print(detect)