import nltk
from flask import Flask, render_template, request
import heapq
import re
#download important modules
nltk.download('stopwords')
# Get English stopwords and punctuation list
from nltk.corpus import stopwords
from string import punctuation
#Using Flask for web page
app=Flask(__name__)
def summarize_text(text):
  text = re.sub(r'\[[0-9]*\]', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  clean_text = re.sub('[^a-zA-Z]', ' ', text)
  clean_text = re.sub(r'\s+', ' ', clean_text)

  # Tokenize
  sentences = nltk.sent_tokenize(text)
  words = nltk.word_tokenize(clean_text.lower())

  # Remove stopwords and create word frequency table
  stop_words = stopwords.words('english')
  word_count = {}

  for word in words:
      if word not in stop_words:
          if word not in word_count:
              word_count[word] = 1
          else:
              word_count[word] += 1

  # Total word count
  max_count = max(word_count.values())
  for word in word_count:
      word_count[word] = word_count[word] / max_count

  # STEP 6: Score sentences
  sentence_scores = {}
  for sentence in sentences:
      for word in nltk.word_tokenize(sentence.lower()):
          if word in word_count:
              if len(sentence.split(' ')) < 30:
                  if sentence not in sentence_scores:
                      sentence_scores[sentence] = word_count[word]
                  else:
                      sentence_scores[sentence] += word_count[word]

  # Generate summary
  summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)
  summary = ' '.join(summary_sentences)
  return summary
    
# Connect with web page
@app.route('/', methods=['GET', 'POST'])
def index():
    summary =''
    if request.method == 'POST':
        input_text = request.form['text']
        summary = summarize_text(input_text)
    return render_template('index.html', summary=summary)

# Run the summarize tool
if __name__ == '__main__':
    app.run(debug=True)