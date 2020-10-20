import json

file = open("debug/gante.txt", "r", encoding="utf8")
new_file = open(input("Digite o arquivo de saída (.json): "), "w+")

lines_list = file.readlines()
file.close()
result_dict = {}
cont = 1
errors = 0
for line in lines_list:
    print(cont)
    line = line.replace('\n', '').split(";")
    try:
        result_dict[line[0]] = {
            "bbox": line[1],
            "label": line[2]
        }
        print(line)
    except:
        errors += 1
    cont += 1
print(f"{errors} linhas erradas")

json.dump(result_dict, new_file, indent=1)
new_file.close()
