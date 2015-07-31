#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import logging
import operator

from nupic.frameworks.opf.modelfactory import ModelFactory

import model_params

_LOGGER = logging.getLogger(__name__)



WORDS = ("the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "the.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "quick.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "brown.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "fox.",
         "time.",
         "time.",
         "time.",
         "time.",
         "time.",
         "time.",
         "time.",
         "person.",
         "person.",
         "person.",
         "person.",
         "person.",
         "person.",
         "year.",
         "year.",
         "year.",
         "year.",
         "year.",
         "way.",
         "way.",
         "way.",
         "way.",
         "way.",
         "day.",
         "day.",
         "day.",
         "day.",
         "day.",
         "thing.",
         "thing.",
         "thing.",
         "thing.",
         "man.",
         "man.",
         "man.",
         "man.",
         "world.",
         "world.",
         "world.",
         "world.",
         "life.",
         "life.",
         "life.",
         "hand.",
         "hand.",
         "hand.",
         "part.",
         "part.",
         "part.",
         "child.",
         "eye.",
         "woman.",
         "place.",
         "work.",
         "week.",
         "case.",
         "point.",
         "government.",
         "company.",
         "number.",
         "group.",
         "problem.",
         "year")




def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)

def run(model, letter, reset=False):
  if reset:
   res =  model.run({"letter": letter,
                     "_reset": True})
  else:
    res = model.run({"letter": letter})
  return max(res.inferences['multiStepPredictions'][1].iteritems(), key=operator.itemgetter(1))[0]


def trainPeanut():
  model = createModel()
  model.enableInference({'predictedField': 'letter'})

  numReps = 2
  numWords = len(WORDS)* numReps #sum(1 for line in open("/usr/share/dict/words.", 'r'))
  wordIndex = 0

  #with open("/usr/share/dict/words.", 'r') as f:
  for i in range(0,numReps):
    for word in WORDS:
      modelInput = {"_reset": True}
      for ch in word.lower():
        modelInput["letter"] = ch
        result = model.run(modelInput)
        if "_reset" in modelInput:
          del modelInput["_reset"]
      if wordIndex % 100 == 0:
        print "Training on word {i} / {t}".format(i=wordIndex, t=numWords)
      wordIndex += 1

  return model

def testPeanut(model, wordList):
  goodWord = [True for _ in range(0, len(wordList))]
  for i, word in enumerate(wordList):
    for j, ch in enumerate(word[:-1]):
      if j == 0:
        inferredCh = run(model, ch, reset=True)
      else:
        inferredCh = run(model, ch)
      if inferredCh != word[j+1]:
        goodWord[i] = False
        print ("DEBUG:   "
               "word={word}, "
               "ich={ich}".format(word=word, i=i, ich=inferredCh))

  return goodWord


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  print "======== Training ========"
  model = trainPeanut()

  print "======== Testing ========"

  wordList = ("the.", "quikc.", "brown.", "fox.")
  res = testPeanut(model, wordList)

  print ""

  print wordList
  print res

  print ""
  print "======== Corrections ========"

  # Fix spelling
  for i, r in enumerate(res):
    if not r:
      word = wordList[i]

      # find error...
      for j, ch in enumerate(word[:-1]):
        if j == 0:
          inferredCh = run(model, ch, reset=True)
        else:
          inferredCh = run(model, ch)
        if inferredCh != word[j+1]:
          break

      correction = ""

      run(model, word[0], reset=False)
      correction += word[0]

      for k in range(1,j):
        run(model, word[k])
        correction += word[k]

      while True:
        correction += run(model, correction[-1:])
        if correction[-1:] == '.':
          break
      print ("Correct spelling for '{bad}' is '{good}'"
             .format(bad=word[:-1], good=correction[:-1]))


  print ""

  #import IPython; IPython.embed()