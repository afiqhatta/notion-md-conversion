import pandas as pd
import readin as rd
import numpy as np
from glob import glob
from keys import *
import pickle


class notionHandler(object):

    def __init__(self, notionKey, databaseKey, numberOfStories):

        self.notionKey = notionKey
        self.databaseKey = databaseKey
        self.numberOfStories = numberOfStories


    def _load_ids_names(self):

        ids, names = rd.getRecentStoryIds(self.notionKey, self.databaseKey, self.numberOfStories)

        return dict(zip(ids, names))

    def saveIdsNameToPickle(self, pickleName):

        idsNamesDict = self._load_ids_names()

        with open('{}'.format(pickleName), 'wb') as f:
            pickle.dump(idsNamesDict, f)
