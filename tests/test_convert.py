import sys
sys.path.append('..')
from app import convert

def test_convert():
    test = ['void test()']
    res = ['\\documentclass{article}', '\\usepackage[utf8]{inputenc}', '\\usepackage{algorithm}', '\\usepackage{algpseudocode}', '\n', '\\title{<Title>}', '\\author{<Your Name>}', '\n', '\\begin{document}', '\\maketitle', '\n', '\n', '\\begin{algorithm}', '\\caption{test}', '\\begin{algorithmic}', '\\Procedure{test}{}', '\\end{algorithmic}', '\\end{algorithm}', '\n', '\\end{document}']
    assert res == convert(test)