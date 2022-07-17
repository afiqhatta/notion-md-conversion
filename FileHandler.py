import pandas as pd
import readin as rd
import numpy as np
from glob import glob
from keys import *


class FileHandler(object):

    def __init__(self, notion_key, database_key, stories_to_load):

        self.notion_key = notion_key
        self.database_key = database_key
        self.stories_to_load = stories_to_load

    def _load_ids_names(self):

        ids, names = rd.getRecentStoryIds(self.notion_key, self.database_key, self.stories_to_load)

        return dict(zip(ids, names))

    def verify_markdowns_exist(self, md_folder='notion2md-output'):
        """

        :param md_folder:
        :return:
        """
        markdowns = [i.split('/')[-1].split('.')[0] for i in glob('notion2md-output/*')]

        return np.isin(markdowns, list(self._load_ids_names().values()))

    def verify_htmls_exist(self, html_folder='htmls'):
        """

        :param html_folder:
        :return:
        """
        htmls = [i.split('/')[-1].split('.')[0] for i in glob('notion2md-output/*')]

        return np.isin(htmls, list(self._load_ids_names().values()))

    def file_table(self, story_number):
        """
        Return a html table for the output
        :param story_number: the number of Notion Stories to Expose
        :return: A html table of what you have published
        """

        ids, names = rd.getRecentStoryIds(notion_key, database_key, story_number)
        names_clean = [' '.join(string.split('-')[:-1]) for string in names]

        df = pd.DataFrame(columns=['Name', 'NotionId', 'Markdown?', 'html_link', 'Ghost', 'Medium'],
                          index=range(len(names_clean)))

        df.loc[:, 'Name'] = names_clean
        df.loc[:, 'NotionId'] = ids
        df.loc[:, 'Markdown?'] = 'Yes'

        return df.to_html()
