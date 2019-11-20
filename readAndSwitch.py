# 我的第一个Python程序
from my_tools import read_xml


def read_simulation_def_meta_model_code(path,nameStr):
    # 此处写读取解析xml文件的代码，读取仿真类型代号对应的内容放到simulation_code中
    dom = read_xml(path)
    root = dom.documentElement
    item = root.getElementsByTagName(nameStr)[0]
    return item.firstChild.data

# 这个path存着仿真定义元模型文件的路径
def slot_read_simulation_def_meta_model():
    path = 'D:\\Workspace\\PycharmProjects\\untitled\\xml\\SimulaitionDefinition.xml'
    simulation_code = read_simulation_def_meta_model_code(path,'simulationExecutionTypeCode')
    if simulation_code=='CE':
        print("输出CE")
        pass
    elif simulation_code == 'b':
        print("11111")
        pass
    elif simulation_code == 'c':
        pass
    elif simulation_code == 'd':
        print("11111")
        pass
    elif simulation_code == 'e':
        pass
    elif simulation_code == 'f':
        print("11111")
        pass
    elif simulation_code == 'g':
        pass
    else:
        print('wrong simulation type code.')
