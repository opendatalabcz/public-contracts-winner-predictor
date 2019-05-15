from stop_words import get_stop_words
from string import punctuation
from ufal.morphodita import Morpho, Tagger, Forms, TaggedLemmas, TokenRanges
from config import config

# MorphoDiTa vars
morpho = Morpho.load(config['dict'])
tagger = Tagger.load(config['tagger'])
forms = Forms()
lemmas = TaggedLemmas()
tokens = TokenRanges()
tokenizer = tagger.newTokenizer()

# Stop words and punctuation
csStopWords = get_stop_words('czech')
csPunctuation = punctuation + '„“‚‘…–—'

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
