from flask import Flask, send_file
import readin as rd
import pandas as pd
from keys import *

app = Flask(__name__)


def verify_markdowns_exist():
    pass


def file_table(story_number):
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


@app.route("/")
def hello_world():
    recentStories = 10

    ids, names = rd.getRecentStoryIds(notion_key, database_key, recentStories)
    name_string = ['<ul>{name}: at id {id}</ul>'.format(name=' '.join(string.split('-')[:-1]), id=id)
                   for string, id in zip(names, ids)]

    notion_list =  "<p>" + "".join(name_string) + "</p>"

    header = '<h2>Afiq, Welcome to Your Publication Log!</h2>

    html = """
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script type=text/javascript>
                $(function() {
                  $('a#test').on('click', function(e) {
                    e.preventDefault()
                    $.getJSON('/background_process_test',
                        function(data) {
                      //do nothing
                    });
                    return false;
                  });
                });
        </script>


        //button
        <div class='container'>
            <h3>Test</h3>
                <form>
                    <a href=# id=test><button class='btn btn-default'>Test</button></a>
                </form>

        </div>
        """

    return header + file_table(recentStories) + html


@app.route('/download')
def downloadFile():
    path = "notion2md-output/Decentralised-Exchanges-5a8e6d112ed646e6bf56eaf5266a2b13.md"
    return send_file(path, as_attachment=True)

@app.route('/htmlpage')
def test():
    html = """
    <p>In the previous article, I explained a state that broke time-translation symmetry was created. In that article, the Hamiltonian created had a parameter h. For time-translation symmetry to be broken, we had to set h=0. This is an idealised scenario. In real-life, we would try our best to set h=0, but there are going to be practical and experimental deviations from this value. So, we need to show that time-symmetry breaking still works even when we perturb h a tiny bit. </p>
    <p><br/></p>
    <p>How do we show that the result still holds even with a tiny perturbation? We need to prove that perturbing the value of h to a small value still maintains the We look at the energy difference of eigenstates that are connected locally. There is usually an energy gap between these eigenstates. If there is a gap, then the perturbed eigenstates only differ from unperturbed eigenstates by a local time evolution. If this is the case, short range correlated states can’t turn into long ranage correlated states. </p>
    <p><br/></p>
    <p>Here, we’ll present a slightly more rigourous arguemnt. Let’s take the unperturbed Hamiltonian, where we’ve set h = 0. This has the floquet operator given below. </p>
    <p><img alt="alt text" src="static/Time-Crystals-Part-IV-e4d83a3f158e47dfa4863c849f459eca_file_0.png" /></p>
    <p>The now want to perturb h a bit. Changing h a tiny bit is known as a local perturbation, since h only acts on the local part of the Hamiltonian - it acts on sigma_i terms. </p>
    <p>We want to show that if we perurb it, that the modified Floquet operator is still diagonal. If it’s stil diagonal, then the eigenstates don’t mix (at least to the first order). This is akin to finding some operator S such that the term below is diagonal. </p>
    <p><img alt="alt text" src="static/Time-Crystals-Part-IV-e4d83a3f158e47dfa4863c849f459eca_file_1.png" /></p>
    <p>The next question is then whether S is local. If S was non-local, then we could potentially connect short range correlated states too long range correlated ones.  So, we have to prove that this operator is <a href="http://local.om">local.</a> To prove this, we break down the operator into smaller parts. To break this down, we write the perturbation as a sum of smaller parts. </p>
    <p><img alt="alt text" src="static/Time-Crystals-Part-IV-e4d83a3f158e47dfa4863c849f459eca_file_2.png" /></p>
    <p>Since we do this, we can also break up S into smaller parts, labelled by S_X. If we prove that these smaller pieces are local, then we are done. </p>
    <p><br/></p>
    <h3>Numerical Analysis of the Floquet Operator</h3>
    <p>To confirm that the numerical resonances don’t destroy the symmetry breaking, we numerically analyse the Floquet operator. </p>
    <p><br/></p>
    <h3>References</h3>
    <p>[1] <a href="https://arxiv.org/pdf/cond-mat/0305505.pdf">https://arxiv.org/pdf/cond-mat/0305505.pdf</a></p>
    <p>[2] <a href="https://arxiv.org/pdf/quant-ph/0601019.pdf">https://arxiv.org/pdf/quant-ph/0601019.pdf</a></p>
    <p><br/></p>
    """
    return html



#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():


    print ("Hello")
    return ("nothing")
