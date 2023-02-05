from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


def convert(a):
    final_ans = []
    # Starting latex lines
    final_ans.append("\\documentclass{article}")
    final_ans.append("\\usepackage[utf8]{inputenc}")
    final_ans.append("\\usepackage{algorithm}")
    final_ans.append("\\usepackage{algpseudocode}")
    final_ans.append("\n")
    final_ans.append("\\title{<Title>}")
    final_ans.append("\\author{<Your Name>}")
    final_ans.append("\n")
    final_ans.append("\\begin{document}")
    final_ans.append("\\maketitle")
    final_ans.append("\n")
    final_ans.append("\n")
    final_ans.append("\\begin{algorithm}")

    # Removing empty spaces from lines
    for i in range(0, len(a)):
        a[i] = a[i].strip()

    # Extracting useless lines before function name like blank lines and comments
    while len(a) > 0:

        # Removing blank lines
        if len(a[0]) == 0:
            a.pop(0)

        else:
            if len(a[0]) >= 2:
                # Removing single line comments
                if a[0][0] == "/" and a[0][1] == "/":
                    strin = ""
                    a[0] = a[0][2:]
                    a[0] = a[0].strip()
                    strin += a[0]
                    strin = strin.strip()
                    strin = "\\Comment{" + strin + "}"
                    final_ans.append(strin)
                    a.pop(0)
                else:
                    # Removing multiple line comments
                    if a[0][0] == "/" and a[0][1] == "*":
                        strin = ""

                        # Removing multiple line comments that appear on single line
                        if len(a[0]) >= 4 and a[0][-2] == "*" and a[0][-1] == "/":
                            a[0] = a[0][2:-2]
                            a[0] = a[0].strip()
                            strin += a[0]
                            strin += " "
                            a.pop(0)

                        # Removing multiple line comments that appear on different multiple line
                        else:
                            a[0] = a[0][2:]
                            a[0] = a[0].strip()
                            strin += a[0]
                            strin += " "
                            a.pop(0)

                            while len(a) > 0:

                                if len(a[0]) >= 2:
                                    if a[0][-2] == "*" and a[0][-1] == "/":
                                        a[0] = a[0][0:-2]
                                        a[0] = a[0].strip()
                                        strin += a[0]
                                        strin += " "
                                        a.pop(0)
                                        break
                                    else:
                                        a[0] = a[0].strip()
                                        strin += a[0]
                                        strin += " "
                                        a.pop(0)

                                else:
                                    a.pop(0)

                        strin = strin.strip()
                        strin = "\\Comment{" + strin + "}"
                        final_ans.append(strin)

                    else:
                        break

            else:
                break

    # Extracting function from code
    function_name = ""
    index = 0
    for i in range(0, len(a[0])):
        if a[0][i] == "(":
            index = i
            break

    function_name = a[0][:index]
    function_name = function_name.strip()
    a[0] = a[0][index:]

    index = 0
    for i in range(len(function_name) - 1, -1, -1):
        if function_name[i] == " ":
            index = i
            break

    function_name = function_name[index + 1 :]

    function_name1 = "\\Procedure{" + function_name + "}{"
    function_name = "\\caption{" + function_name + "}"

    final_ans.append(function_name)
    final_ans.append("\\begin{algorithmic}")

    # Extracting function parameters from code
    a[0] = a[0][1:]
    func_parameters = ""

    while len(a) > 0:
        index = 0

        a[0] = a[0].strip()
        if len(a[0]) == 0:
            a.pop(0)
            continue

        for i in range(0, len(a[0])):
            if a[0][i] == "," or a[0][i] == ")":
                index = i
                break

        parame = a[0][:index]
        a[0] = a[0][index:]

        parame = parame.strip()

        for i in range(len(parame) - 1, -1, -1):
            if parame[i] == " ":
                index = i
                break

        parame = parame[index + 1 :]
        if len(parame) > 0:
            if parame[0] == "&":
                parame = parame[1:]

        parame = parame + ","

        func_parameters = func_parameters + parame

        if a[0][0] == ")":
            a[0] = a[0][1:]
            break
        else:
            a[0] = a[0][1:]

    func_parameters = func_parameters[:-1]
    function_name1 = function_name1 + func_parameters + "}"
    final_ans.append(function_name1)

    a[0] = a[0].strip()

    if len(a) > 0 and len(a[0]) >= 2:
        if a[0][0] == "/" and a[0][1] == "/":
            a[0] = a[0][2:]
            a[0] = a[0].strip()
            strin = ""
            strin = "\\Comment{" + a[0] + "}"
            final_ans.append(strin)
            a.pop(0)

    if len(a) > 0 and len(a[0]) >= 4:
        if a[0][0] == "/" and a[0][1] == "*" and a[0][-2] == "*" and a[0][-1] == "/":
            a[0] = a[0][2:-2]
            a[0] = a[0].strip()
            strin = ""
            strin = "\\Comment{" + a[0] + "}"
            final_ans.append(strin)
            a.pop(0)

    # Pseudo Code for main code inside function

    procedure_list = ["\\EndProcedure"]

    while len(a) > 0:
        a[0] = a[0].strip()
        if len(a[0]) == 0:
            a.pop(0)
            continue

        if a[0][0] == "{":
            a[0] = a[0][1:]
            continue

        if a[0][0] == "}":
            final_ans.append(procedure_list[-1])
            procedure_list.pop()
            a[0] = a[0][1:]
            continue
        if len(a[0]) >= 2:
            # Removing single line comments
            if a[0][0] == "/" and a[0][1] == "/":
                strin = ""
                a[0] = a[0][2:]
                a[0] = a[0].strip()
                strin += a[0]
                strin = strin.strip()
                strin = "\\Comment{" + strin + "}"
                final_ans.append(strin)
                a.pop(0)
                continue

        if len(a[0]) >= 6:
            if a[0][0:6] == "return":
                a[0] = a[0][:-1]
                a[0] = a[0].strip()
                a[0] = a[0][6:]

                a[0] = a[0].strip()
                retur = "\\State \\Return {" + a[0] + "}"
                a.pop(0)
                final_ans.append(retur)
                continue

        if len(a[0]) >= 4:

            # Removing multiple line comments that appear on single line
            if a[0][0] == "/" and a[0][1] == "*":
                strin = ""

                if a[0][-2] == "*" and a[0][-1] == "/":
                    a[0] = a[0][2:-2]
                    a[0] = a[0].strip()
                    strin += a[0]
                    strin += " "
                    strin = strin.strip()
                    strin = "\\Comment{" + strin + "}"
                    final_ans.append(strin)
                    a.pop(0)
                    continue

        if len(a[0]) >= 2:

            # Removing multiple line comments
            if a[0][0] == "/" and a[0][1] == "*":
                strin = ""

                a[0] = a[0][2:]
                a[0] = a[0].strip()
                strin += a[0]
                strin += " "
                a.pop(0)

                while len(a) > 0:

                    if len(a[0]) >= 2:
                        if a[0][-2] == "*" and a[0][-1] == "/":
                            a[0] = a[0][0:-2]
                            a[0] = a[0].strip()
                            strin += a[0]
                            strin += " "
                            a.pop(0)
                            break
                        else:
                            a[0] = a[0].strip()
                            strin += a[0]
                            strin += " "
                            a.pop(0)

                    else:
                        a.pop(0)

                strin = strin.strip()
                strin = "\\Comment{" + strin + "}"
                final_ans.append(strin)

                continue

        # If Statement
        if len(a[0]) >= 2:
            # break
            if a[0][0] == "i" and a[0][1] == "f":
                procedure_list.append("\\EndIf")
                a[0] = a[0][2:]
                if_param = ""
                count_para = 0

                while len(a) > 0:
                    check = False
                    a[0] = a[0].strip()

                    for i in range(0, len(a[0])):
                        if a[0][i] == "(":
                            count_para = count_para + 1
                        if a[0][i] == ")":
                            count_para = count_para - 1

                        if count_para == 0:
                            check = True
                            if_param = if_param + a[0][:i]
                            a[0] = a[0][i + 1 :]

                            break

                    if check:
                        break
                    else:
                        if_param = if_param + a[0]
                        a.pop(0)

                if_param = if_param[1:]
                if_param = if_param.strip()
                if_param = "$ " + if_param + " $"
                if_param = "\\If{" + if_param + "}"
                final_ans.append(if_param)
                continue

        # Else Statement
        if len(a[0]) >= 4:
            if a[0][0:4] == "else":
                # break
                procedure_list.append("\\EndIf")
                final_ans = final_ans[:-1]
                a[0] = a[0][4:]
                a[0] = a[0].strip()

                if len(a[0]) >= 2 and a[0][0:2] == "if":
                    a[0] = a[0][2:]
                    if_param = ""
                    count_para = 0
                    while len(a) > 0:
                        check = False
                        a[0] = a[0].strip()
                        for i in range(0, len(a[0])):
                            if a[0][i] == "(":
                                count_para = count_para + 1
                            if a[0][i] == ")":
                                count_para = count_para - 1
                            if count_para == 0:
                                check = True
                                if_param = if_param + a[0][:i]
                                a[0] = a[0][i + 1 :]
                                break

                        if check:
                            break
                        else:
                            if_param = if_param + a[0]
                            a.pop(0)

                    if_param = if_param[1:]
                    if_param = if_param.strip()
                    if_param = "$ " + if_param + " $"
                    if_param = "\ElsIf{" + if_param + "}"
                    final_ans.append(if_param)
                else:
                    final_ans.append("\\Else")

                continue

        # While Loop
        if len(a[0]) >= 5:
            if (
                a[0][0] == "w"
                and a[0][1] == "h"
                and a[0][2] == "i"
                and a[0][3] == "l"
                and a[0][4] == "e"
            ):
                procedure_list.append("\\EndWhile")
                a[0] = a[0][5:]
                if_param = ""
                count_para = 0
                while len(a) > 0:
                    check = False
                    a[0] = a[0].strip()
                    for i in range(0, len(a[0])):
                        if a[0][i] == "(":
                            count_para = count_para + 1
                        if a[0][i] == ")":
                            count_para = count_para - 1
                        if count_para == 0:
                            check = True
                            if_param = if_param + a[0][:i]
                            a[0] = a[0][i + 1 :]
                            break

                    if check:
                        break
                    else:
                        if_param = if_param + a[0]
                        a.pop(0)

                if_param = if_param[1:]
                if_param = if_param.strip()

                if_param = " " + if_param + " "
                if_param = "\\While{" + if_param + "}"
                final_ans.append(if_param)

                continue

        # For Loop
        if len(a[0]) >= 3:
            if a[0][0] == "f" and a[0][1] == "o" and a[0][2] == "r":
                procedure_list.append("\\EndFor")
                a[0] = a[0][3:]

                if_param = ""
                count_para = 0
                while len(a) > 0:
                    check = False
                    a[0] = a[0].strip()
                    for i in range(0, len(a[0])):
                        if a[0][i] == "(":
                            count_para = count_para + 1
                        if a[0][i] == ")":
                            count_para = count_para - 1
                        if count_para == 0:
                            check = True
                            if_param = if_param + a[0][:i]
                            a[0] = a[0][i + 1 :]
                            break

                    if check:
                        break
                    else:
                        if_param = if_param + a[0]
                        a.pop(0)

                if_param = if_param[1:]
                if_param = if_param.strip()

                if len(if_param) >= 4 and if_param[:4] == "auto":
                    if_param = if_param[4:]
                    if_param = if_param.strip()
                    x11 = ""
                    x12 = ""
                    for j1 in range(0, len(if_param)):
                        if if_param[j1] == ":":
                            x11 = if_param[:j1]
                            x12 = if_param[j1 + 1 :]
                            break

                    if_param = x11 + " in " + x12

                    if_param = "\\For{" + if_param + "}"
                    final_ans.append(if_param)
                    continue

                temp = if_param.split(";")
                if_param = ""

                temp1 = temp[0].split("=")
                temp1[0].strip()
                temp2 = temp1[0].split(" ")
                if_param = temp2[1] + " $\\leftarrow$ "
                temp1[1].strip()
                if_param = if_param + temp1[1]
                temp[1].strip()

                for j1 in range(len(temp[1]) - 1, -1, -1):
                    if temp[1][j1] == "=" or temp[1][j1] == ">" or temp[1][j1] == "<":
                        temp[1] = temp[1][j1 + 1 :]
                        break

                temp[2].strip()
                if temp[2][-1] == "+":
                    if_param = if_param + " to "
                if temp[2][-1] == "-":
                    if_param = if_param + " downto "

                if_param = if_param + temp[1]

                if_param = " " + if_param + " "
                if_param = "\\For{" + if_param + "}"
                final_ans.append(if_param)
                continue

        # Input statement
        if len(a[0]) >= 3:
            if a[0][0:3] == "cin":

                a[0] = a[0][0:-1]
                temp = a[0].split(">>")

                entered_element = ""
                for i in range(1, (len(temp))):
                    temp[i] = temp[i].strip()
                    entered_element += temp[i]
                    entered_element += " "
                    if i != (len(temp) - 1):
                        entered_element += "and "
                entered_element = "\\State \\textbf{input} " + entered_element
                final_ans.append(entered_element)
                a.pop(0)
                continue

        # Output Statement
        if len(a[0]) >= 4:
            if a[0][0:4] == "cout":
                a[0] = a[0][0:-1]
                temp = a[0].split("<<")
                temp[-1] = temp[-1].strip()
                if temp[-1] == "endl":
                    temp = temp[0:-1]
                entered_element = "\\State \\textbf{print} "
                for i in range(1, (len(temp))):
                    temp[i] = temp[i].strip()
                    entered_element += temp[i]
                    entered_element += " "
                    if i != (len(temp) - 1):
                        entered_element += "and "
                final_ans.append(entered_element)
                a.pop(0)
                continue

        if (
            (len(a[0]) >= 3 and a[0][0:3] == "int")
            or (
                len(a[0]) >= 4
                and (a[0][0:4] == "long" or a[0][0:4] == "auto" or a[0][0:4] == "char")
            )
            or (len(a[0]) >= 5 and (a[0][0:5] == "float" or a[0][0:5] == "short"))
            or (len(a[0]) >= 6 and (a[0][0:6] == "signed" or a[0][0:6] == "double"))
            or (len(a[0]) >= 8 and a[0][0:8] == "unsigned")
        ):
            while len(a[0]) >= 6 and (a[0][0:6] == "signed"):
                a[0] = a[0][6:]
                a[0] = a[0].strip()

            while len(a[0]) >= 8 and a[0][0:8] == "unsigned":
                a[0] = a[0][8:]
                a[0] = a[0].strip()
            while len(a[0]) >= 5 and (a[0][0:5] == "float" or a[0][0:5] == "short"):
                a[0] = a[0][5:]
                a[0] = a[0].strip()

            while len(a[0]) >= 4 and (
                a[0][0:4] == "long" or a[0][0:4] == "auto" or a[0][0:4] == "char"
            ):
                a[0] = a[0][4:]
                a[0] = a[0].strip()
            while len(a[0]) >= 6 and (a[0][0:6] == "double"):
                a[0] = a[0][6:]
                a[0] = a[0].strip()

            while len(a[0]) >= 3 and a[0][0:3] == "int":
                a[0] = a[0][3:]
                a[0] = a[0].strip()

            while len(a[0]) >= 6 and (a[0][0:6] == "signed"):
                a[0] = a[0][6:]
                a[0] = a[0].strip()

            while len(a[0]) >= 8 and a[0][0:8] == "unsigned":
                a[0] = a[0][8:]
                a[0] = a[0].strip()
            while len(a[0]) >= 5 and (a[0][0:5] == "float" or a[0][0:5] == "short"):
                a[0] = a[0][5:]
                a[0] = a[0].strip()

            while len(a[0]) >= 4 and (
                a[0][0:4] == "long" or a[0][0:4] == "auto" or a[0][0:4] == "char"
            ):
                a[0] = a[0][4:]
                a[0] = a[0].strip()
            while len(a[0]) >= 6 and (a[0][0:6] == "double"):
                a[0] = a[0][6:]
                a[0] = a[0].strip()

            while len(a[0]) >= 3 and a[0][0:3] == "int":
                a[0] = a[0][3:]
                a[0] = a[0].strip()

            a[0] = a[0][0:-1]
            temp = a[0].split(",")
            for j in temp:
                flag = False
                j = j.strip()
                for k in range(1, (len(j) - 1)):
                    if j[k] == "=":
                        flag = True
                        temp = "\\State " + j[0:k] + " $\leftarrow$ " + j[k + 1 :]
                        final_ans.append(temp)
                        break
                if not flag:

                    temp = "\\State Define a variable " + j
                    final_ans.append(temp)

            a.pop(0)
            continue

        variable = ["vector", "list", "stack", "map", "queue", "priority_queue"]
        exist = False
        for var in variable:
            if len(a[0]) >= len(var):

                if a[0][: len(var)] == var:

                    a[0] = a[0][len(var) :]
                    paren_count = 0
                    a[0] = a[0].strip()
                    for i in range(0, len(a[0])):
                        if a[0][i] == "<":
                            paren_count = paren_count + 1
                        if a[0][i] == ">":
                            paren_count = paren_count - 1

                        if paren_count == 0:
                            a[0] = a[0][i + 1 :]
                            break

                    a[0] = a[0].strip()
                    a[0] = a[0][:-1]
                    a[0] = a[0].strip()

                    temp = a[0].split(",")
                    for i in temp:
                        i = i.strip()
                        strin = "\\State Define a " + var + " " + i
                        final_ans.append(strin)
                    a.pop(0)
                    exist = True
                    break

        if exist:
            continue

        statement = ""
        for i in range(0, len(a[0])):
            if a[0][i] == ";":
                statement = a[0][:i]
                a[0] = a[0][i + 1 :]
                break

        statement = statement.strip()
        temp = statement.split("=")
        statement = ""
        for x12 in temp:
            statement = statement + x12 + " $\leftarrow$ "

        if len(statement) >= 14:
            statement = statement[:-14]

        statement = "\\State " + statement
        final_ans.append(statement)

    final_ans.append("\\end{algorithmic}")
    final_ans.append("\\end{algorithm}")
    final_ans.append("\n")
    final_ans.append("\\end{document}")

    for i in range(0, len(final_ans)):
        temp = final_ans[i].split("_")
        strin = ""

        for x in temp:
            strin = strin + x + "\_"
        if len(strin) >= 2:
            strin = strin[:-2]

        final_ans[i] = strin

    for i in range(0, len(final_ans)):
        if len(final_ans[i]) >= 2:
            if final_ans[i][-1] == "+" and final_ans[i][-2] == "+":
                final_ans[i] = final_ans[i][:-2]
                final_ans[i] = (
                    final_ans[i] + " $ \\leftarrow $ " + final_ans[i][7:] + " + 1"
                )
                continue
            if final_ans[i][-1] == "-" and final_ans[i][-2] == "-":
                final_ans[i] = final_ans[i][:-2]
                final_ans[i] = (
                    final_ans[i] + " $ \\leftarrow $ " + final_ans[i][7:] + " - 1"
                )
                continue

    # vect = ["<", ">", "=", "&"]
    # for sig in vect:
    #     for i in range(0,len(final_ans)):
    #         temp = final_ans[i].split(sig)
    #         strin = ""

    #         for x in temp:
    #             strin = strin + x + "$ " + sig + " $"
    #         if(len(strin)>=5):
    #             strin = strin[:-5]

    #         final_ans[i]=strin

    return final_ans


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyse", methods=["POST"])
def analyse():
    message = "Input code is not in format as required, please change and retry."
    try:
        if request.method == "POST":
            rawtext = request.form["rawtext"].split("\n")
            a = rawtext
            message = convert(a)
    except:
        render_template("index.html", message=message)

    return render_template("index.html", message=message)

    # return render_template('index.html', message=message)


if __name__ == "__main__":
    app.run(debug=True)
