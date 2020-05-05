import json
import xmltodict


class A(object):
    def __init__(self, a, b, AA_):
        self.a = a
        self.b = b
        self.AA_ = AA_


def AA(self):
    if (self.a > 10):
        return
    else:
        self.a += 1
        tmp = self.a
        print(tmp)
        self.AA_(self)


a = A(0, 1, AA)
print('s')
AA(a)


def xmltojson(xmlstr):
    # parse是的xml解析器
    xmlparse = xmltodict.parse(xmlstr)
    # json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    # dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse, indent=1)
    return jsonstr


def jsontoxml(jsonstr):
    # xmltodict库的unparse()json转xml
    xmlstr = xmltodict.unparse(jsonstr)
    print(xmlstr)
    return xmlstr


with open(r'F:\pythonCode\PycharmProjects\simulation_execution_monitoring\members\fpMemberXml_C.xml', 'r', encoding='utf-8') as f:
    content=f.read()

dict_json=xmltojson(content)  # 调用转换函数
data=json.loads(dict_json)
with open(r'F:\pythonCode\PycharmProjects\simulation_execution_monitoring\members\fpMemberXml_C.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data,indent=2,ensure_ascii=False))
