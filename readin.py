import os
import re
from notion_client import Client
import pandas as pd
import pdb
import markdown
from keys import notion_key, database_key
from PIL import Image


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
    \\usepackage{amsfonts}
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


def outputPdfScaled(texString, outputfile, scaling):

    # output scaled image of Tex file
    outputPdf(texString, outputfile)
    resize_image(outputfile, outputfile, scaling)



def getAllTex(filepath, folder, scaling):

    # save the Tex in the form of pngs

    strings = getTex(filepath)
    for ix, string in enumerate(strings):
        outputPdfScaled(string, folder + '/' + 'file_{}.png'.format(ix), scaling)


def fillFolder(filepath, scaling):
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

    getAllTex(filepath, folder_name, scaling)


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


def replaceStringWithFileLocations(md_file, prefix=''):

    # replace TeX strings with their dedicated file names

    f = open(md_file, "r")
    testString = (f.read())
    pat = r'(?<=\$\$).+?(?=\$\$)'  # See Note at the bottom of the answer

    texStrings = re.findall(pat, testString)
    replacements = ['![alt text]({prefix}file_{i}.png)'.format(prefix=prefix, i=i) for i in range(len(texStrings))]
    for i, j in dict(zip(texStrings, replacements)).items():
        testString = testString.replace(i, j)
    testString = testString.replace('$', '')
    return testString


def convertMDtoHTMLwithFiles(md_file, prefix, outputFile):

    replacedString = replaceStringWithFileLocations(md_file, prefix)
    md = markdown.Markdown()

    f = open(outputFile, "w")
    f.write(md.convert(replacedString))
    f.close()


def resize_image(img_path, new_image_path, scaling):

    # resize and save an image
    image = Image.open(img_path)
    width, height = image.size
    image = image.resize((int(width * scaling), int(height * scaling)), Image.ANTIALIAS)
    image.save(fp=new_image_path)


def upload_target_directory(writing_dir, article_title, article_html_path):

    # create new directory
    os.system('mkdir ' + writing_dir + article_title)
    os.system('mkdir ' + writing_dir + article_title)

    directory = writing_dir + article_title
    os.system('touch ' + directory + '/abstract.txt') # create
    os.system('touch ' + directory + '/title.txt')
    os.system('echo TEST >> ' + directory + '/title.txt')
    os.system('cp ' + article_html_path + ' ' +  directory + '/content.html')

    pass


def copy_images(source_dir, img_dir, img_tag):
    """

    :param source_dir: where do the images come from
    :param img_dir: the static file where we put images
    :param img_tag:
    :return:
    """
    for file in os.listdir(source_dir):
        os.system('cp ' + source_dir + '/' + file + ' ' + img_dir + img_tag + file)


if __name__ == "__main__":

    test_file = 'testMD.md'
    recentStories = 20
    scaling = 0.5

    article_short_name = 'correlation_functions'
    article_title  = 'correlation_functions'

    img_prefix = '/static/correlation_functions_'
    img_tag = 'correlation_functions_'
    article_name = 'Computing-Correlation-Functions-94c988c4376542e18071f1f5c2f589b7.md'
    source_dir = 'output/Computing-Correlation-Functions-94c988c4376542e18071f1f5c2f589b7'
    article_html_path = 'testHTML.html'

    img_dir = '/Users/ahmadafiqhatta/Documents/afiqhatta.com/app/static/'
    static_dir = '/Users/ahmadafiqhatta/Documents/afiqhatta.com/app/static/writing/'
    writing_dir = '/Users/ahmadafiqhatta/Documents/afiqhatta.com/app/static/writing/'  # where the blog stuff is kept

    copy_images(source_dir, img_dir, img_tag)
    upload_target_directory(writing_dir, article_title, article_html_path)


    # # IMPORT STUFF FROM NOTION
    # # get ids and names of recent notion stories
    # ids, names = getRecentStoryIds(notion_key, database_key, recentStories)
    # exportRecentMDs(ids, names)

    #
    # testMDFile = 'notion2md-output/Tuning-a-Checkerboard-State-2dcfee6ad378491ab38764683ae1d492.md'
    # image_tag = 'checkerboard = '
    # testMDFile2 = 'notion2md-output/Computing-Correlation-Functions-94c988c4376542e18071f1f5c2f589b7.md'
    # testMDFile3 = 'notion2md-output/The-Ultraviolet-Catastrophe-b0155ffcb3af4d7bad92b5d6ea7488f1.md'


    # fillFolder(testMDFile3, scaling) # process png files
    # fillFolder(testMDFile, scaling) # process png files
    #
    # # convertMDtoHTMLwithFiles(testMDFile, 'testHTML.html')
    # convertMDtoHTMLwithFiles(testMDFile2, img_prefix, 'testHTML.html')
    #
    # # copy intro blog
    # dir_name = 'test_upload'
    # os.system('touch /Users/ahmadafiqhatta/Documents/afiqhatta.com/app/static/text.txt')
    # os.system('mkdir ' + static_dir  + dir_name)

