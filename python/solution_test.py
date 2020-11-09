import sys
from solution import Solution


if __name__ == '__main__':

    files = [
        {"input": "input000.txt", "output": "output000.txt"},
        {"input": "input001.txt", "output": "output001.txt"},
        {"input": "input002.txt", "output": "output002.txt"},
        {"input": "input003.txt", "output": "output003.txt"},
        {"input": "input004.txt", "output": "output004.txt"},
        {"input": "input005.txt", "output": "output005.txt"},
        {"input": "input006.txt", "output": "output006.txt"},
        {"input": "input007.txt", "output": "output007.txt"},
        {"input": "input008.txt", "output": "output008.txt"},
        {"input": "input009.txt", "output": "output009.txt"},
        {"input": "input010.txt", "output": "output010.txt"},
        {"input": "input011.txt", "output": "output011.txt"},
        {"input": "input012.txt", "output": "output012.txt"},
    ]

    for file in files:

        expected_result = open("../test/output/" + file["output"], "r").readline()

        with open("../test/input/" + file["input"], "r") as f:

            """
            No Readme é informado o seguinte:
                "A primeira linha contém o número de eventos a serem processados. Da segunda em diante,
                os dados do evento separados por vírgula."

            Para simular esse mesmo input com os arquivos de teste dentro da pasta input, estou adicionando
            o número de linhas/eventos na primeira linha da mensagem enviada para a Solution processar
            """

            lines = f.readlines()
            number_of_events = len(lines)
            file_input = str(number_of_events) + "\n"  # Adicionando o número de linhas no inicio da mensagem
            file_input += "".join(lines)
            result = Solution.process_messages(messages=file_input)

            if sys.argv[1] == "detail":
                print("###############################################################################################")
                print("File: %s - Result: %s" % (file["input"], result))
                print("File: %s - Result: %s" % (file["output"], expected_result))

            else:
                print(result)
