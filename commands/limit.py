def limit(args):
    usage = "/me {user} -> Usage: !limit <number1> <number2>"
    data =''

    try:
        n1,n2 = (int(args[0]),int(args[1]))
        for x in range(n1,n2+1):
            if x == n2:
                data+='%s' % x
            else:
                data+='%s, ' % x

    except:
        return usage

    return data