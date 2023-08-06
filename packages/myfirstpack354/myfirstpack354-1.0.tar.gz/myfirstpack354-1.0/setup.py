from distutils.core import setup
'''
**打包+把当前模块放入到本地库作为依赖 流程：
注意一定要进入setup.py文件的所在目录执行下面命令
1：准备模块包文件myfirstpack注意这是个包所以下面有_ini_.py
2.在myfirstpack中写入你想要打包的模块文件demo1.py demo2.py
3.在myfistpack包同级的目录下编写setup.py文件
4.进入setup.py的目录 打开终端执行 
python setup.py sdist
执行后生成
dist目录---myfirstpack354.jar
MANIFEST文件
5.打包后你的模块除了生成.tar包在dist目录下，你的模块同时也传到了你的本地库site-package中但是在安装列表
中并没有安装，你需要安装python setup.py install。这样让你的删除模块才能生效
6.你可尝试pip uninstall myfirstpack354 来删除模块，但是本地库site-package中任然存在模块？？需要手动从site-package


你可在其他的包下的模块中尝试导入from myfirstpack354 import demo1，然后执行模块的方法
python setup.py install
6.python setup.py sdist upload
7.pip uninstall myfirstpack354


**上传打包模块到pypi ----https://pypi.org/
执行完成后就有4个文件
dist目录---myfirstpack354.jar
MANIFEST文件
setup.py文件
使用终端进入setup.py文件所在目录，执行
python setup.py install
python list
'''

setup(
    name='myfirstpack354',#对外我们的模块名字
    version='1.0',
    description='这是第一个对外发布的模块，测试',
    author='rossi',
    author_email='328486536@qq.com',
    py_modules=['myfirstpack354.demo1','myfirstpack354.demo2']
)
