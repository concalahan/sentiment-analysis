import nltk

class Analyzer():
    """Implements sentiment analysis."""
    # constructor
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.posWords = set()
        posFile = open(positives, "r")
        for line in posFile:
            if line.strip():
                self.posWords.add(line.rstrip("\n"))
        posFile.close()
        
        self.negWords = set()
        negFile = open(negatives, "r")
        for line in negFile:
            if line.strip():
                self.negWords.add(line.rstrip("\n"))
        negFile.close()
        
    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        score = 0
        for words in self.posWords:
            if text == words:
                score += 1
        for words in self.negWords:
            if text == words:
                score -= 1
        return score
