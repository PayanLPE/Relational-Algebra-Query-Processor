operators = ["sigma", "pi", "natural_join", "left_outer_join", "right_outer_join", "full_outer_join"]

def main(): 
    relations = parse_relation('data.txt')
    queue = parse_query("query.txt", relations)
    relation = exec_query(queue, relations)
    output(relation)

def parse_relation(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    relations = {}
    current_relation = []
    current_relation_name = ''
    for line in lines:
        line = line.strip()
        if '=' in line:
            # new relation
            line = line.split('=')
            current_relation_name = line[0].strip()
        elif '}' in line:
            # ends
            relations[current_relation_name] = current_relation
            current_relation = []
        elif '{' in line:
            continue
        elif not line == '':
            # remove padding
            line = line.replace("'", '')
            line = line.replace(' ', '')
            line = line.split(',')

            # cast to correct data type
            for i in range(len(line)):
                try:
                    # integer
                    line[i] = int(line[i])
                except ValueError:
                    try:
                        # float
                        line[i] = float(line[i])
                    except ValueError:
                        if line[i].lower() == 'true':
                            line[i] = True
                        elif line[i].lower() == 'false':
                            line[i] = False

            current_relation.append(line)
        else:
            continue
    return relations

def parse_query(filename, relations):
    with open(filename, 'r') as file:
        lines = file.readlines()

    text = lines[0]
    text = text.split(" ")

    # credit: https://brilliant.org/wiki/shunting-yard-algorithm/, my own implementation from pseudocode
    queue = []
    stack = []
    for i in range(len(text)):
        if text[i] in relations.keys():
            queue.append(text[i])
        elif text[i] in operators:
            if (text[i] == "sigma" or text[i] == "pi"):
                stack.append(text[i] + " " + text[i+1])
            else:
                stack.append(text[i])
        elif text[i] == '(':
            stack.append(text[i])
        elif text[i] == ')':
            elem = stack.pop()
            while not elem == '(':
                queue.append(elem)
                elem = stack.pop()
    
    for _ in range(len(stack)):
        elem = stack.pop()
        if elem != '(':
            queue.append(elem)

    return queue

def exec_query(queue, relations):
    current_relation_a = []
    current_relation_b = []
    for x in queue:
        if x in relations.keys():
            if not current_relation_a == []:
                current_relation_b = relations[x]
            else:
                current_relation_a = relations[x]

        elif "sigma" in x:
            x = x.split(" ")
            if current_relation_b == []:
                current_relation_a = sigma(x[1], current_relation_a)
            else:
                current_relation_b = sigma(x[1], current_relation_b)
        elif "pi" in x:
            x = x.split(" ")
            if current_relation_b == []:
                current_relation_a = pi(x[1], current_relation_a)
            else:
                current_relation_b = pi(x[1], current_relation_b)
        elif "natural_join" in x:
            current_relation_a = natural_join(current_relation_a, current_relation_b)
            current_relation_b = []
        elif "left_outer_join" in x:
            current_relation_a = left_outer_join(current_relation_a, current_relation_b)
            current_relation_b = []
        elif "right_outer_join" in x:
            current_relation_a = right_outer_join(current_relation_a, current_relation_b)
            current_relation_b = []
        elif "full_outer_join" in x:
            current_relation_a = full_outer_join(current_relation_a, current_relation_b)
            current_relation_b = []
        
    return current_relation_a

def output(relation):
    print("Output: ")
    for x in relation:
        print(x)

def sigma(conditions, relation):
    conditions = conditions.split(',')
    attributes = [x.split('>')[0].split('<')[0].split('=')[0].split('!')[0] for x in conditions]
    attributes_index = [relation[0].index(x) for x in attributes]

    for i in range(len(conditions)):
        temp = "[%s]" % attributes_index[i]
        conditions[i] = conditions[i].replace(attributes[i], temp)

    new_relation= []
    new_relation.append(relation[0])
    for i in range(1, len(relation)): 
        check = True
        for x in conditions:
            x = "relation[%s]" % i + x
            if eval(x) == False:
                check = False
        if check:
            new_relation.append(relation[i])
    return new_relation

def pi(rows, relation):
    rows = rows.split(',')
    attributes_index = [relation[0].index(x) for x in rows]

    new_relation= []
    for i in range(len(relation)): 
        new_relation.append([relation[i][j] for j in attributes_index])
    return new_relation

def natural_join(relation_a, relation_b):
    attributes_a = relation_a[0]
    attributes_b = relation_b[0]

    # get all common attributes of a and b
    common_attributes = [x for x in attributes_a if x in attributes_b]
    common_attributes_a_index = [relation_a[0].index(x) for x in common_attributes]
    common_attributes_b_index = [relation_b[0].index(x) for x in common_attributes]

    # get the remain_attributes_b_index
    remain_attributes_b_index = list(set(range(len(attributes_b))) - set(common_attributes_b_index))
    

    # change it to all [common_attributes_index] for eval() later
    for i in range(len(common_attributes_a_index)):
        common_attributes_a_index[i] = "[%s]" % common_attributes_a_index[i]

    for i in range(len(common_attributes_b_index)):
        common_attributes_b_index[i] = "[%s]" % common_attributes_b_index[i]

    new_relation= []
    part_relation_b = [relation_b[0][i] for i in remain_attributes_b_index]
    new_relation.append(relation_a[0] + part_relation_b)
        
    for i in range(1, len(relation_a)):
        for j in range(1, len(relation_b)):
            check = True
            for index in range(len(common_attributes_a_index)):
                statement = "relation_a[%s]" % i + common_attributes_a_index[index] + "==" + "relation_b[%s]" % j + common_attributes_b_index[index]
                if eval(statement) == False:
                    check = False
            if check:
                part_relation_b = [relation_b[j][k] for k in remain_attributes_b_index]
                new_relation.append(relation_a[i] + part_relation_b)
    return new_relation

def left_outer_join(relation_a, relation_b):
    attributes_a = relation_a[0]
    attributes_b = relation_b[0]

    # get all common attributes of a and b
    common_attributes = [x for x in attributes_a if x in attributes_b]
    common_attributes_a_index = [relation_a[0].index(x) for x in common_attributes]
    common_attributes_b_index = [relation_b[0].index(x) for x in common_attributes]

    # get the remain_attributes_b_index
    remain_attributes_b_index = list(set(range(len(attributes_b))) - set(common_attributes_b_index))
    

    # change it to all [common_attributes_index] for eval() later
    for i in range(len(common_attributes_a_index)):
        common_attributes_a_index[i] = "[%s]" % common_attributes_a_index[i]

    for i in range(len(common_attributes_b_index)):
        common_attributes_b_index[i] = "[%s]" % common_attributes_b_index[i]

    new_relation= []
    # append attributes
    part_relation_b = [relation_b[0][i] for i in remain_attributes_b_index]
    new_relation.append(relation_a[0] + part_relation_b)

    for i in range(1, len(relation_a)):
        added = False
        for j in range(1, len(relation_b)):
            check = True
            # evaluate all common attributes make sure all the same
            for index in range(len(common_attributes_a_index)):
                statement = "relation_a[%s]" % i + common_attributes_a_index[index] + "==" + "relation_b[%s]" % j + common_attributes_b_index[index]
                if eval(statement) == False:
                    check = False
                
            # if all same, add to new_relation
            if check:
                part_relation_b = [relation_b[j][k] for k in remain_attributes_b_index]
                new_relation.append(relation_a[i] + part_relation_b)
                added = True
        # if not same, add with None 
        if not added:
            temp = relation_a[i] + [None] * (len(remain_attributes_b_index))
            new_relation.append(temp)
    return new_relation

def right_outer_join(relation_a, relation_b):
    return left_outer_join(relation_b, relation_a)

def full_outer_join(relation_a, relation_b):
    attributes_a = relation_a[0]
    attributes_b = relation_b[0]

    # get all common attributes of a and b
    common_attributes = [x for x in attributes_a if x in attributes_b]
    common_attributes_a_index = [relation_a[0].index(x) for x in common_attributes]
    common_attributes_b_index = [relation_b[0].index(x) for x in common_attributes]

    # get the remain_attributes_b_index
    remain_attributes_b_index = list(set(range(len(attributes_b))) - set(common_attributes_b_index))
    

    # change it to all [common_attributes_index] for eval() later
    for i in range(len(common_attributes_a_index)):
        common_attributes_a_index[i] = "[%s]" % common_attributes_a_index[i]

    for i in range(len(common_attributes_b_index)):
        common_attributes_b_index[i] = "[%s]" % common_attributes_b_index[i]

    new_relation= []

    # append attributes
    part_relation_b = [relation_b[0][i] for i in remain_attributes_b_index]
    new_relation.append(relation_a[0] + part_relation_b)

    added_in_relation_b = []

    for i in range(1, len(relation_a)):
        added = False
        for j in range(1, len(relation_b)):
            check = True
            # evaluate all common attributes make sure all the same
            for index in range(len(common_attributes_a_index)):
                statement = "relation_a[%s]" % i + common_attributes_a_index[index] + "==" + "relation_b[%s]" % j + common_attributes_b_index[index]
                if eval(statement) == False:
                    check = False
                
            # if all same, add to new_relation
            if check:
                part_relation_b = [relation_b[i][k] for k in remain_attributes_b_index]
                new_relation.append(relation_a[i] + part_relation_b)
                added = True

                added_in_relation_b.append(j)
        # if not same, add with None 
        if not added:
            temp = relation_a[i] + [None] * (len(remain_attributes_b_index))
            new_relation.append(temp)

    # add the remain rows in relation_b that wasnt added in a
    for i in range(1, len(relation_b)):
        if not i in added_in_relation_b:
            temp = [None] * (len(relation_b) - (len(remain_attributes_b_index))) + relation_b[i]
            new_relation.append(temp)
    return new_relation

if __name__ == "__main__":
    main()