from flask import Flask, request, render_template
import re


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def my_form_post():
    output_list = []
    text = request.form['text']
    syntax_list = text.split('\n')
    for line in enumerate(syntax_list):
        if line[1][0:17].casefold() == str("AttributesContain").casefold():
            divider_idx = (line[1].find(':'))
            if line[1][0:divider_idx].count('|') < 2:
                if line[1].count(':') < 2:
                    syntax_list[line[0]] = line[1].replace(
                        line[1][0:divider_idx + 1], 'ISC[')
                    last_position = syntax_list[line[0]].rfind(']')
                    syntax_list[line[0]] = syntax_list[line[0]][0:last_position] + \
                                           syntax_list[line[0]][last_position].\
                                               replace(']', '] newlinehere ')
                    print(syntax_list[line[0]])
                if line[1].count(':') > 2:
                    syntax_list[line[0]] = \
                        line[1].replace(line[1][0:divider_idx + 1],
                                                      'SpecialKeyword[')
    for val in syntax_list:
        output_list.append(re.sub(r'(?<=\:)[0-9]+(?=\:)', 'any', val))
    return render_template('output.html', data=output_list).replace('\n', '')\
        .replace(' newlinehere ', '\n')
