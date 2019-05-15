from stop_words import get_stop_words
from string import punctuation
from ufal.morphodita import Morpho, Tagger, Forms, TaggedLemmas, TokenRanges

# MorphoDiTa vars
morpho = None
tagger = None
forms = Forms()
lemmas = TaggedLemmas()
tokens = TokenRanges()
tokenizer = tagger.newTokenizer()

# Stop words and punctuation
csStopWords = get_stop_words('czech')
csPunctuation = punctuation + '„“‚‘…–—'

def initLemmatizer(config):
  global morpho, tagger
  morpho = Morpho.load(config.dict)
  tagger = Tagger.load(config.tagger)

def lemmatize(text):
  res = []
  tokenizer.setText(text)
  t = 0
  while tokenizer.nextSentence(forms, tokens):
    tagger.tag(forms, lemmas)

    for i in range(len(lemmas)):
      lemma = lemmas[i]
      token = tokens[i]
      raw = morpho.rawLemma(lemma.lemma)
      t = token.start + token.length

      if raw in csPunctuation:
        continue

      if raw in csStopWords:
        continue

      res.append(raw)

  return ' '.join(res)
