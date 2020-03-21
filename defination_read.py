from my_tools import read_xml
import sys

if __name__ == '__main__':
    xml_dom = read_xml('simluation_define/SimulaitionDefinition.xml')
    root = xml_dom.documentElement
    prm = xml_dom.getElementsByTagName('primitiveRoundMethod')[0]
    prmitiveRoundMethod = {
        'name': prm.getAttribute('name'),
        'ID': prm.getAttribute('ID'),
        'path': prm.getAttribute('path'),
        'attributes': {},
    }
    for one_attribute_label in prm.getElementsByTagName('attribute'):
        prmitiveRoundMethod['attributes'].update({one_attribute_label.getAttribute('name'): 'init__'})
    sys.path.append(prmitiveRoundMethod['path'])
    from aa__ import *  # 一个特定的名字
    globals()[prmitiveRoundMethod['name']](**prmitiveRoundMethod['attributes'])
