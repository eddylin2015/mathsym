import re
import math

def IterateMultiDict(f):
    """
    Iterate requset.form
    """
    #f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            print (key+":"+value)

### math
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)    

### input ans 
def Text2St(ans):
    if ans.strip() == "": return "-3.1415926"
    ans = re.sub(r"X", r"x", ans)
    ans = re.sub(r"(\d)x", r"\1*x", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)x", r"\1*x", ans))
    ans=re.sub(r"x[(]", r"x*(", ans)
    ans = re.sub(r"x[ ]*", r"x", ans)
    ans = ans.replace(r"x^", r"x**")

    ans = re.sub(r"Y", r"y", ans)
    ans = re.sub(r"(\d)y", r"\1*y", ans)
    ans = ans = re.sub(r"[)][(]", r")*(", re.sub(r"(\d)y", r"\1*y", ans))
    ans=re.sub(r"y[(]", r"y*(", ans)
    ans = re.sub(r"y[ ]*", r"y", ans)
    ans = ans.replace(r"y^", r"y**")
    
    ans=re.sub(r"(\d)[(]", r"\1*(", ans)
    ans=re.sub(r"(\d)J[(]", r"\1*J(", ans)
    ans = ans.replace(r"J(", r"sqrt(")
    return ans

def NTE2Table(data):
    return '<table><tr>{}</tr><tr>{}</tr></table>'.format(
           '<th>{}</th>'.format('</th><th>'.join( r for r in  r"編號,題型,題目,答案,作答,檢查,提示".split(","))),
           '</tr><tr>'.join(
               '<td>{}</td>'.format(
                   '</td><td>'.join("$$%s$$" % r[_] if i==2 else "%s" % r[_] for i, _ in enumerate(r))) for r in data)
           )

