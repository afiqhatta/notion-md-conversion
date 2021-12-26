import os
import re
from notion_client import Client
import pandas as pd
import pdb
import markdown


def getTex(filepath):
    # return a list of Tex strings

    f = open(filepath, "r")
    testString = (f.read())
    pat = r'(?<=\$\$).+?(?=\$\$)'  # See Note at the bottom of the answer

    return re.findall(pat, testString)


def outputPdf(texString, outputfile):

    baseString = """\documentclass[preview]{standalone}
    \\usepackage{amstext}
    \\usepackage{amsmath}
    \\begin{document}
    \\begin{equation}
    """

    endString = """
    \end{equation}
    \end{document}
    """

    testString = baseString + texString + endString
    with open('readme.tex', 'w') as f:
        f.write(testString)
    os.system('pdflatex readme.tex')
    os.system('convert -density 300 readme.pdf -quality 90 {}'.format(outputfile))


def getAllTex(filepath, folder):

    strings = getTex(filepath)
    for ix, string in enumerate(strings):
        outputPdf(string, folder + '/' + 'file_{}.png'.format(ix))


def fillFolder(filepath):
    """
    Get a markdown file and then create a folder with images inside.

    :param filepath: the location of the markdown file
    :return: a folder with the images inside
    """
    # automatically create and then fill folders
    if not os.path.isdir('output'):
        os.system('mkdir output')

    folder_name = 'output/{}'.format(filepath.split('/')[-1].split('.')[0])
    if not os.path.isdir(folder_name):
        os.system('mkdir {}'.format(folder_name))

    getAllTex(filepath, folder_name)


def getRecentStoryIds(notion_key, database_key, recentStories):
    """
    Get recent Notion page IDs from a database.
    :param notion_key: notion access token
    :param database_key: database key
    :param recentStories: the number of recent stories that need to be retrived
    :return: list of IDs, list of file names
    """

    os.environ['NOTION_TOKEN'] = notion_key
    notion = Client(auth=notion_key)

    df = pd.DataFrame(notion.databases.query(database_key)['results'])
    recent_stories = df.sort_values(by='last_edited_time', ascending=False)[:recentStories]
    names = recent_stories.url.values

    return recent_stories.id.values, [item.split('/')[-1] for item in names]


def exportRecentMDs(id_list, name_list):

    # gets a list of ids and names and then exports them to markdown files
    for item, name in zip(id_list, name_list):
        os.system('notion2md -i {}'.format(item))
        os.system('mv notion2md-output/{id_name}.md notion2md-output/{name}.md'.format(id_name=item, name=name))


def replaceStringWithFileLocations(md_file):

    # replace TeX strings with their dedicated file names

    f = open(md_file, "r")
    testString = (f.read())
    pat = r'(?<=\$\$).+?(?=\$\$)'  # See Note at the bottom of the answer

    texStrings = re.findall(pat, testString)
    replacements = ['![alt text](file_{}.png)'.format(i) for i in range(len(texStrings))]
    for i, j in dict(zip(texStrings, replacements)).items():
        testString = testString.replace(i, j)
    testString = testString.replace('$', '')
    return testString


def convertMDtoHTMLwithFiles(md_file, outputFile):

    replacedString = replaceStringWithFileLocations(md_file)
    md = markdown.Markdown()

    f = open(outputFile, "w")
    f.write(md.convert(replacedString))
    f.close()


if __name__ == "__main__":
    test_file = 'testMD.md'

    notion_key = "secret_M5WK7SAzNLfk0S4p3nvYCywdsfcMrfHmjbeSBmyQQ7X"
    database_key = 'a46622e0eea642ae8ee3866883abb37a'
    recentStories = 10
    testMDFile = 'notion2md-output/Tuning-a-Checkerboard-State-2dcfee6ad378491ab38764683ae1d492.md'

    # get ids and names of recent notion stories
    # ids, names = getRecentStoryIds(notion_key, database_key, recentStories)
    # exportRecentMDs(ids, names)

    # fillFolder('notion2md-output/Tuning-a-Checkerboard-State-2dcfee6ad378491ab38764683ae1d492.md')
    convertMDtoHTMLwithFiles(testMDFile, 'testHTML.html')







