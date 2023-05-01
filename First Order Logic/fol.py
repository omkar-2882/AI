import time

def input_file():
    f = open("input.txt","r")
    noq = int(f.readline().strip())
    q = []
    for i in range(noq):
        q.append(f.readline().strip())
    nKB = int(f.readline().strip())
    KB = []
    for i in range(nKB):
        KB.append(f.readline().strip())
    return noq, q, nKB, KB


def addInKB(KB, query):
    if query in KB:
        return False
    return True


def resolvable(query, query1):
    part = query.split(' | ')
    part1 = query1.split(' | ')
    cntUnifiable = 0
    cntUnified = 0
    flag = 0
    for pt in range(len(part)):
        for pt1 in range(len(part1)):
            pred = part[pt][ : part[pt].index('(')].strip()
            pred1 = part1[pt1][ : part1[pt1].index('(')].strip()
            param = query.split(' | ')[pt][query.split(' | ')[pt].index('(') + 1 : query.split(' | ')[pt].index(')')].split(',')
            param1 = query1.split(' | ')[pt1][query1.split(' | ')[pt1].index('(') + 1 : query1.split(' | ')[pt1].index(')')].split(',')
            if pred.startswith('~') and not pred1.startswith('~') and pred[1:] == pred1:
                flag = 1
            elif not pred.startswith('~') and pred1.startswith('~') and pred == pred1[1:]:
                flag = 1

            if flag == 1:
                flag = 0
                cntUnifiable += 1
                stringg = []
                err = 0
                count = 0
                for p in range(len(param)):
                    if param[p][0].isupper() and param1[p][0].isupper() and param[p] == param1[p]:
                        count += 1
                    elif param[p][0].isupper() and param1[p][0].isupper() and param[p] != param1[p]:  # Both Const
                        err = 1
                        return False
                    elif param[p][0].isupper() and param1[p][0].islower():  # replace in 1
                        count += 1
                        query1 = query1.replace(("(" + param1[p]), ("(" + param[p]))
                        query1 = query1.replace((param1[p] + ")"), (param[p] + ")"))
                        query1 = query1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query1)
                    elif param[p][0].islower() and param1[p][0].isupper():  # replace in 0
                        count += 1
                        query = query.replace(("(" + param[p]), ("(" + param1[p]))
                        query = query.replace((param[p] + ")"), (param1[p] + ")"))
                        query = query.replace(("," + param[p] + ","), ("," + param1[p] + ","))
                        param[p] = param1[p]
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query)
                    elif param[p][0].islower() and param1[p][0].islower():  # Both variable 0 -> 1
                        count += 1
                        query1 = query1.replace(("(" + param1[p]), ("(" + param[p]))
                        query1 = query1.replace((param1[p] + ")"), (param[p] + ")"))
                        query1 = query1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        param[p] = param1[p]
                        if p == len(param) - 1 and err == 0:
                            stringg.append(query)
                if count == len(param):
                    cntUnified += 1
                    count = 0
    if cntUnifiable == cntUnified and cntUnified > 0:
        cntUnified = 0
        cntUnifiable = 0
        return True
    else:
        return False

    return False


def unify(query, query1, KBase):
    part = query.split(' | ')
    part1 = query1.split(' | ')
    for t in part:
        pred = t[:t.index('(')].strip()
        param = t[t.index('(')+1:t.index(')')].split(',')
        flag = 0
        for t1 in part1:
            # print "T1:" + t1
            pred1 = t1[:t1.index('(')].strip()
            param1 = t1[t1.index('(')+1:t1.index(')')].split(',')
            if pred.startswith('~') and not pred1.startswith('~') and pred[1:] == pred1:
                flag = 1
            elif not pred.startswith('~') and pred1.startswith('~') and pred == pred1[1:]:
                flag = 1

            if flag == 1:  # For Same Predicate unify
                stringg = []
                err = 0
                qr = query[:]
                qr1 = query1[:]
                count = 0
                for p in range(len(param)):
                    if param[p][0].isupper() and param1[p][0].isupper() and param[p] == param1[p]:
                        count += 1
                        if p == len(param)-1 and err == 0:
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].isupper() and param1[p][0].isupper() and param[p] != param1[p]:  # Both Const
                        err = 1
                    elif param[p][0].isupper() and param1[p][0].islower() and err == 0:  # replace in 1
                        count += 1
                        qr1 = qr1.replace(("("+param1[p]),("("+param[p]))
                        qr1 = qr1.replace((param1[p] + ")"), (param[p] + ")"))
                        qr1 = qr1.replace((","+param1[p] + ","), (","+param[p] + ","))

                        if p == len(param)-1 and err == 0:
                            param1 = param
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].islower() and param1[p][0].isupper() and err == 0:  # replace in 0
                        count += 1
                        qr = qr.replace(("(" + param[p]), ("(" + param1[p]))
                        qr = qr.replace((param[p] + ")"), (param1[p] + ")"))
                        qr = qr.replace(("," + param[p] + ","), ("," + param1[p] + ","))
                        if p == len(param)-1 and err == 0:
                            param = param1
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                                # print uf1
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)
                    elif param[p][0].islower() and param1[p][0].islower() and err == 0:  # Both variable 0 -> 1
                        count += 1
                        qr1 = qr1.replace(("(" + param1[p]), ("(" + param[p]))
                        qr1 = qr1.replace((param1[p] + ")"), (param[p] + ")"))
                        qr1 = qr1.replace(("," + param1[p] + ","), ("," + param[p] + ","))
                        if p == len(param) - 1 and err == 0:
                            param1 = param
                            u = qr.split(' | ')
                            uf = []
                            for pi in u:
                                if pi != (pred + '('+(',').join(param)+')'):
                                    uf.append(pi)
                            # print uf
                            u1 = qr1.split(' | ')
                            uf1 = []
                            for pi1 in u1:
                                if pi1 != (pred1 + '('+(',').join(param1)+')'):
                                    uf1.append(pi1)
                                # print uf1
                            unified = " | ".join(set(uf + uf1))
                            stringg.append(unified)

                if count == len(param):
                    count = 0
                    return unified
            flag = 0


def resolution(q1, KBase, t):
    if q1 == None or q1 == "":
        return True
    # if not str in KBase :
    if addInKB(KBase, q1):
        KBase.append(q1)
    else:
        return False
    ll = []
    for idx in range(len(KBase)):
        if resolvable(q1, b[idx]):
            ll.append(KBase[idx])
    for idx in range(len(ll)):
        if ((time.time() - t) > 200):
            return False
        ans = unify(q1, ll[idx], KBase)
        if resolution(ans, KBase, t):
            return True
    return False

def standardize(KB):
    for i in range(len(KB)):
        temp = KB[i].split(' | ')
        param = []
        for t in temp:
            param.extend(t[t.index('(') + 1:t.index(')')].split(','))
        param = list(set(param))
        for p in range(len(param)):
            if param[p][0].islower():
                KB[i] = KB[i].replace(("(" + param[p]), ("(" + param[p] + str(i)))
                KB[i] = KB[i].replace((param[p] + ")"), (param[p]+ str(i) + ")"))
                KB[i] = KB[i].replace(("," + param[p] + ","), ("," + param[p]+ str(i) + ","))


def write(ans):
    file = open("output.txt", "w")
    for a in ans:
        file.write(str(a).upper()+"\n")
    file.close()


def main():
    nq, q, nKB, KB = input_file()
    standardize(KB)
    ans = []
    for i in range(len(q)):
        if q[i].startswith('~'):
            q[i] = q[i][1:]
        else:
            q[i] = '~' + q[i]
        try:
            a = resolution(q[i], KB[:], time.time())
        except:
            a = "FALSE"
        ans.append(a)
    write(ans)
    # print KB

main()