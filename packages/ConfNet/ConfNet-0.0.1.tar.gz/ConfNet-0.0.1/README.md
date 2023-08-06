# 第一章 GraphEmbedding运维
## 运维说明
1. tensorflow可以认为只是一个包，因为其用法是：import tensorflow as tf
2. Anaconda = python+conda（包管理器+科学计算库）
    1. Anaconda是一个开源的Python发行版本，其包含了conda（conda是一个包管理器）、Python等180多个科学包及其依赖项，比如numpy、pandas等。里包含了Python，所以下载了Anaconda的就不需要下载Python了。
    2. 官网下载安装Anaconda3-2021.11-MacOSX-x86_64 (1).pkg
    3. 用conda 安装的包，是安装在全局的，在ide里的任何项目都可以用，跟npm安装的类似。所以应该在anaconda里安装tensorflow
3. anaconda换源：
    1. conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
    2. conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
    3. conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
    4. conda config --add channels http://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
    5. conda config --set show_channel_urls yes
    6. 注意，清除国内源的命令：conda config --remove-key channels
    

3. 在Pycharm里面配置anaconda环境
    1. anaconda里面包含很多库，在Pycharm里面配置anaconda环境，很多库就可以不用安装了。
    2. 设置python interpreter（类比设置Java执行器）：
        Preference->Project Interpreter-> 齿轮 -> add-> 【注意！不是python环境】Conda Environment->Existing environment->
        找到目录：/anaconda3/envs/【这里是anaconda里的环境名】sureenvirontment/bin/python
        （注意，不是/Users/sure/opt/anaconda3/python.app/Contents/MacOS/python，这个好像是默认的）
4. 说明：anaconda里的environments相当于重新创建一个包的根目录，是为了不同项目如果有不同依赖的时候来切换，避免互相干扰。不这样做，下面在anaconda里安装的包，在import的时候就会报错找不到
如果设置了，那么上面的设置里，python interpreter就应该是上面增加的interpreter

5. 安装包（方法一）：mac的anaconda安装后没有Anaconda prompt，但是直接在Anaconda navigator里似乎无法安装包，
这时候需要到这个目录里去执行
    * cd /Users/sure/opt/anaconda3/bin (最好用方法2)
    * 安装tensorflow：pip3 install tensorflow
    * 安装xgboost：pip install xgboost -i https://pypi.tuna.tsinghua.edu.cn/simple
    * 安装shapely: pip install shapely
    * 安装：pip install pandas networkx joblib tqdm gensim fastdtw matplotlib scikit-learn -i https://pypi.tuna.tsinghua.edu.cn/simple
（方法二），在anaconda界面，环境后面的绿箭头，点击打开terminal，然后同上
6. 在terminal里执行时，记得指定anaconda里的python：
    * cd 项目目录: cd /Users/sure/PycharmProjects/mygraphembedding
    * python setup.py install
    * cd examples
    * python struc2vec_flight.py
7. 也可以用下面设置，更方便：
    ![](./pics/ide_1.png)
    ![](./pics/ide_2.png)
8. 6月26日切换到gitee

## 项目运行命令
1. 清理文件夹 build, dist, examples/result, examples/temp_struc2vec, ge.egg-info
2. 增加新类，需要在ge/models/__init__.py文件里去增加这个类
2. 重新初始化： 上面的python地址/python setup.py install

# 第二章 python打包
## 包仓库PyPI
PyPI是Python Package Index的缩写，是Python的官方索引
地址： https://pypi.org/

所有发布到PyPI的包，可以使用pip命令来安装：
```shell
pip install <package name>
```

pip：是Python 官方的标准的 Python 包管理器，用来安装和管理 Python 标准库之外的其他包（第三方包）。
从 Python 3.4 起，pip 已经成为 Python 安装程序的一部分。
作为类比，其他包管理器还有conda，区别是conda管理的不是PyPI的包，而是来自Anaconda repository以 Anaconda Cloud的conda包。
Conda的包是二进制文件（pip的包是whl格式的压缩包）且不仅限于Python软件，还可能包含C或C ++库，R包或任何其他软件。


Python库打包的格式包括Wheel和Egg。Egg格式是由setuptools在2004年引入，而Wheel格式是由PEP427在2012年定义。使用Wheel和Egg安装都不需要重新构建和编译，其在发布之前就应该完成测试和构建。
Egg和Wheel本质上都是一个 zip格式包，Egg文件使用.egg扩展名，Wheel使用.whl 扩展名。Wheel的出现是为了替代Egg，其现在被认为是Python的二进制包的标准格式。
以下是 Wheel 和 Egg 的主要区别：
- Wheel 有一个官方的 PEP427 来定义，而 Egg 没有 PEP 定义
- Wheel 是一种分发格式，即打包格式。而 Egg 既是一种分发格式，也是一种运行时安装的格式，并且是可以被直接 import
- Wheel 文件不会包含 .pyc 文件
- Wheel 使用和 PEP376 兼容的 .dist-info 目录，而 Egg 使用 .egg-info 目录
- Wheel 有着更丰富的命名规则。
- Wheel 是有版本的。每个 Wheel 文件都包含 wheel 规范的版本和打包的实现
- Wheel 在内部被 sysconfig path type 管理，因此转向其他格式也更容易

## 样例代码
### 目录结构
1. 创建一个测试项目，git的目录也在这个界别，例如：
sure_pypi_project

2. 在项目下，创建一个待发布的包目录，这里主要写代码，例如：
package_sure_pypitest

3. 在sure_pypi项目目录下，创建三个文件：
    - README.rst
    - LICENSE
    - setup.py


目录结构如下：  
|—sure_pypi_project  
|&nbsp;&nbsp;&nbsp;&nbsp;|—package_sure_pypitest  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|—\_\_init\_\_.py  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|—main.py  
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|—surego.py  
|&nbsp;&nbsp;&nbsp;&nbsp;|—README.rst  
|&nbsp;&nbsp;&nbsp;&nbsp;|—setup.py  
|&nbsp;&nbsp;&nbsp;&nbsp;|—LICENSE  

### 配置文件如下
- README.rst：说明文档，markdown格式
- LICENSE：许可证，上传到PyPI的每个包都包含许可证


#### setup.py脚本如下
是setuptools的构建脚本，用来描述项目，包括项目名字、版本、依赖库、支持系统、在哪些版本的python上运行，


示例：
```python
from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='package_mikezhou_talk',  # 包名
      version='1.0.0',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='mikezhou_talk',
      author_email='762357658@qq.com',
      url='https://mp.weixin.qq.com/s/9FQ-Tun5FbpBepBAsdY62w',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
```

重要参数说明：  
 - name：项目的名称，name是包的分发名称。
 - version：项目的版本。需要注意的是，PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
 - packages：指定最终发布的包中要包含的packages。 通常为包含 __init__.py 的文件夹。可以指定where、include和exclude
 - install_requires：项目依赖哪些库，这些库会在pip install的时候自动安装

包含数据文件：
 - package_data:该参数是一个从包名称到glob模式列表的字典
 - include_package_data:该参数被设置为True时自动添加包中受版本控制的数据文件，可替代package_data，同时，exclude_package_data 可以排除某些文件。注意当需要加入没有被版本控制的文件时，还是仍然需要使用 package_data 参数才行。
 - data_files: 该参数通常用于包含不在包内的数据文件，即包的外部文件，如：配置文件，消息目录，数据文件。其指定了一系列二元组，即(目的安装目录，源文件) ，表示哪些文件被安装到哪些目录中。如果目录名是相对路径，则相对于安装前缀进行解释。
 - manifest template: manifest template 即编写 MANIFEST.in 文件，文件内容就是需要包含在分发包中的文件。一个 MANIFEST.in 文件如下：

其他参数说明：  
 - author和author_email：项目作者的名字和邮件, 用于识别包的作者。 
 - description：项目的简短描述
 - long_description：项目的详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
 - classifiers：其他信息，一般包括项目支持的Python版本，License，支持的操作系统。


编写技巧：  
可以采用克隆setup.py仓库（推荐）的方式来简化填写。  
大名鼎鼎的requests库的作者大神kennethreitz为大家准备了一个仓库作为一个setup.py的很好的模板：  
```shell
git clone  https://github.com/kennethreitz/setup.py
```

### 功能代码如下
1. 要注意源代码文件夹的名字与setup.py里配置的包名（Name）要一致。
2. 包目录下一定要有__init__.py文件，否则虽然打包不会错，但是安装后import时候会无法import。
3. main.py是入口执行文件，用来开启服务，对于二方库不是必须的
例如，在package_sure_pypitest包目录下，创建main.py文件：

【main.py】 
```python
import itertools

case_list = ['用户名', '密码']
value_list = ['正确', '不正确', '特殊符号', '超过最大长度']


def gen_case(item=case_list, value=value_list):
    '''输出笛卡尔用例集合'''
    for i in itertools.product(item, value):
        print('输入'.join(i))

def test_print():
	    print("欢迎搜索关注公众号: 「测试开发技术」!")

if __name__ == '__main__':
    test_print()
```

方法文件【surego.py】
```python
def success_print():
    print("成功调用了surego方法！")
```

## 打包
### 工具
安装打包工具setuptools和wheel：
```shell
python3 -m pip install --user --upgrade setuptools wheel
```

### 打包
1 检查setup.py是否有错误：
```shell
python setup.py check
```

2 打包1（tar.gz格式源码包）。在setup.py同级目录运行下面命令，则在当前目录的dist文件夹下, 会多出一个tar.gz结尾的包：
```shell
python setup.py sdist build
```
3 打包2（wheels格式）。在setup.py同级目录运行下面命令，这样会在dist文件夹下面生成一个whl文件
```shell
python setup.py bdist_wheel --universal
```
4 打包3（同时打tar.gz和wheels），在setup.py同级目录运行下面命令，会在dist目录下生成一个tar.gz的源码包和一个.whl的Wheel包：
```shell
python3 setup.py sdist bdist_wheel
```

## 发布
1 去https://pypi.org/account/register/注册账号
用户名：surewong.com

2 安装twine，注意只有twine> = 1.11.0 才能将元数据正确发送到 Pypi上：
```shell
pip install twine
```

3 上传包，期间会让你输入注册的用户名和密码，成功后就发布到PyPI了：
```shell
python setup.py bdist_wheel --universal
twine upload dist/*
```

每次更新：
```shell

twine upload dist/*
```

## 验证
1. 可以在官网查看

2. 可以用pip安装，命令在官网上也能看到
pip install sure-pypi-test==0.1.2


3. 另外注意，如果用的是anaconda里python 
	这个时候需要把包安装到anaconda里，如果which python给出的是anaconda的python，则直接安装就行。如果不是，可以在anaconda界面的环境右边箭头，打开anaconda prompt，然后再用pip install
	> 备注：在ide里用which python、which pip可以查看)，第一个注意是在执行器里设置对应的python版本。vscode是在launch.json里加上："python.defaultInterpreterPath": "/Users/sure/opt/anaconda3/bin/python"）
		
4. 代码使用：
```python
from sure-pypi-test import surego

if __name__ == '__main__':
    surego.success_print()
```

## 包结构的补充说明
Python对包的处理相当简单，包就是文件夹，但该文件夹下必须存在 init.py 文件。

常见的包结构如下：
![](./pics/package.png)
使用：from package import item
这个子项(item)既可以是子包也可以是其他命名，如函数、类、变量等。

### 子包
注意：在ide里创建子包的时候，每一层新建的时候要建Python Package，而不是Directory

包可以嵌套，包含子包，例如：
![](./pics/subpackage.png)


对于子包的使用，有如下三种方式：
1. 只导入包里的特定模块，例如： import sound.efforts.echo 就只导入了 sound.effects.echo 子模块。它必须通过完整的名称来引用：sound.effects.echo.echofilter()
2. 另一种写法from sound.effects import echo，可以在没有包前缀的情况下也可以使用：echo.echofilter()
3. 或者 from sound.effects.echo import echofilter，也可以直接调：echo.echofilter()

注意：import item.subitem.subsubitem 这样的语法时，这些子项必须是包，最后的子项可以是包或模块，但不能是类、函数、变量等。

在包内互相引用的时候，可以按相对位置引入子模块，比如在echo模块中，可以这样引用
```python
from . import reverse              # 同级目录 导入 reverse
from .. import frormats            # 上级目录 导入 frormats
from ..filters import equalizer    # 上级目录的filters模块下 导入 equalizer
```

### 从*导入包
import * 这样的语句理论上是希望文件系统找出包中所有的子模块，然后导入它们。  

但这可能会花长时间，并出现边界效应等。Python 解决方案是提供一个明确的包索引。这个索引由__init__.py定义 all 变量，该变量为一列表，如上例 sound/effects 下的__init__.py 中，可定义 all = [“echo”,“surround”,“reverse”]  

这意味着， from sound.effects import * 会从对应的包中导入以上三个子模块； 尽管提供 import * 的方法，仍不建议在生产代码中使用这种写法。  


**\_\_init\_\_.py文件**
一般是空文件即可，也可以：1. 执行包的初始化代码；2. 定义all变量

# 第三章 python加密
参考：https://www.jianshu.com/p/21598f3dd584?u_atoken=400c6702-46ba-4ea5-8983-842436448b1b&u_asession=01l9pknhe9sh7FelQCzN_ZSHbLz2mkuzDYuWYfGRC3ZUQ6Z6C3yNT03UvHRqsvVAq1X0KNBwm7Lovlpxjd_P_q4JsKWYrT3W_NKPr8w6oU7K_3Cj0yC45eJDHoLQLNbD0VzdjoMV1y19BFQvaXcOyBfmBkFo3NEHBv0PZUm6pbxQU&u_asig=05gOlPQd-cxCpa2nAR_5pqQ4FTeKMffNqGYf3Lxrd5SYdxxqihQtqwdJKy0FfXu1d-TtBGvhE7q1d6rgA3E9-pJ5J-UxIH6xpXc_IHhEZzkt3CbydFgOvjbTjDQYhuBpP9XzbZcPS6jE-XCczGH3Z_9XonT2ZORMUiEmyjnOoGkqT9JS7q8ZD7Xtz2Ly-b0kmuyAKRFSVJkkdwVUnyHAIJzfp17FA0GXdI_8RjTy3UpaubgYbyupsxVHnz81XruDg8qBR97QLsOYcZJeUxi-_JXu3h9VXwMyh6PgyDIVSG1W_BOR0p7904ABDU2qzvwImbxXcb_Of8IEFkEDWaheITx1AHgWKUx3qMwWxDK-5d6YKfX0f85gBDHYVRtkelYGxFmWspDxyAEEo4kbsryBKb9Q&u_aref=rOejnxekj8Gpjxn7LZZJKhX6nU8%3D

## 5种方法简介
1. 用解释器生成的.pyc文件：已经有现成的反编译工具，可以直接破解
2. 代码混淆：实测了，Intensio-Obfuscator有bug跑不起来。pyobfuscate（GitHub - astrand/pyobfuscate: pyobfuscate）混淆效果很一般，连变量名都替换不掉，教程https://mythreyatechblog.wordpress.com/2016/12/02/how-to-use-pyobfuscate/
3. 用py2exe打包成二进制文件：只能在windows上运行
4. 修改解释器，并使用配套该解释器加密的python文件。因为解释器是二进制的，进行保护：太难
5. 编译成c++，然后再加密：一般使用cython

## 参考
https://zhuanlan.zhihu.com/p/466169852 
https://blog.csdn.net/weixin_29488835/article/details/113517683

## Cython是什么
虽然现在流行pybind11。但Cython更经典，至少Cython本身的质量是没问题的，大量C扩展都是基于它，如numpy。

Cython是一种编程语言，它使得为Python语言编写C扩展就像Python本身一样容易。
它旨在成为Python语言的超集，赋予它高级、面向对象、函数式和动态编程。
除此之外，它的主要功能是支持作为语言一部分的可选静态类型声明。源代码被翻译成优化的 C/C++ 代码并编译为 Python 扩展模块。这允许非常快速的程序执行和与外部 C 库的紧密集成，同时保持 Python 语言众所周知的高程序员生产力。


## 关于Cython运行的原理
https://cython.readthedocs.io/en/latest/src/quickstart/overview.html 

## Cython的安装
https://cython.readthedocs.io/en/latest/src/quickstart/install.html

The simplest way of installing Cython is by using pip:
```shell script
pip install Cython
```

The newest Cython release can always be downloaded from https://cython.org/. Unpack the tarball or zip file, enter the directory, and then run:
```shell script
python setup.py install
```

## 第一个Cython代码
首先编辑hello.pyx：
```python
def say_hello_to(name):
    print("Hello %s!" % name)
```

因为是Cython可以理解为Python的超集，所以Python的语法适用于Cython

现在我们将hello.pyx用Cython编译成.c文件
该.c文件由 C 编译器编译成一个.so文件（或.pyd在 Windows 上），该文件可以 import直接编辑到 Python 会话中。 setuptools负责这部分。
编写一个 setuptoolssetup.py来构建Cython 代码
（虽然使用Pyximport可以使.pyx 像.py文件一样导入 Cython文件，但是不推荐，所以之后也不进行太多记录）
setup.py：

```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("hello.pyx"),
    zip_safe=False,
)
```
之后需要在命令行进入.pyx路径使用python setup.py build_ext --inplace即可生成.pyd，改文件可以直接被调用
```python
import hello
hello.say_hello_to('Ning')
```
运行结果为：
Hello Ning!

## 使用
打包完，使用so文件即可


# 第四章 原项目信息
# Method
项目地址：https://github.com/shenweichen/GraphEmbedding 

|   Model   | Paper                                                                                                                      | Note                                                                                        |
| :-------: | :------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| DeepWalk  | [KDD 2014][DeepWalk: Online Learning of Social Representations](http://www.perozzi.net/publications/14_kdd_deepwalk.pdf)   | [【Graph Embedding】DeepWalk：算法原理，实现和应用](https://zhuanlan.zhihu.com/p/56380812)  |
|   LINE    | [WWW 2015][LINE: Large-scale Information Network Embedding](https://arxiv.org/pdf/1503.03578.pdf)                          | [【Graph Embedding】LINE：算法原理，实现和应用](https://zhuanlan.zhihu.com/p/56478167)      |
| Node2Vec  | [KDD 2016][node2vec: Scalable Feature Learning for Networks](https://www.kdd.org/kdd2016/papers/files/rfp0218-groverA.pdf) | [【Graph Embedding】Node2Vec：算法原理，实现和应用](https://zhuanlan.zhihu.com/p/56542707)  |
|   SDNE    | [KDD 2016][Structural Deep Network Embedding](https://www.kdd.org/kdd2016/papers/files/rfp0191-wangAemb.pdf)               | [【Graph Embedding】SDNE：算法原理，实现和应用](https://zhuanlan.zhihu.com/p/56637181)      |
| Struc2Vec | [KDD 2017][struc2vec: Learning Node Representations from Structural Identity](https://arxiv.org/pdf/1704.03165.pdf)        | [【Graph Embedding】Struc2Vec：算法原理，实现和应用](https://zhuanlan.zhihu.com/p/56733145) |


# How to run examples
1. clone the repo and make sure you have installed `tensorflow` or `tensorflow-gpu` on your local machine. 
2. run following commands
```bash
python setup.py install
cd examples
python deepwalk_wiki.py
```

## DisscussionGroup & Related Projects

<html>
    <table style="margin-left: 20px; margin-right: auto;">
        <tr>
            <td>
                公众号：<b>浅梦的学习笔记</b><br><br>
                <a href="https://github.com/shenweichen/GraphEmbedding">
  <img align="center" src="./pics/code.png" />
</a>
            </td>
            <td>
                微信：<b>deepctrbot</b><br><br>
 <a href="https://github.com/shenweichen/GraphEmbedding">
  <img align="center" src="./pics/deepctrbot.png" />
</a>
            </td>
            <td>
<ul>
<li><a href="https://github.com/shenweichen/AlgoNotes">AlgoNotes</a></li>
<li><a href="https://github.com/shenweichen/DeepCTR">DeepCTR</a></li>
<li><a href="https://github.com/shenweichen/DeepMatch">DeepMatch</a></li>
<li><a href="https://github.com/shenweichen/DeepCTR-Torch">DeepCTR-Torch</a></li>
</ul>
            </td>
        </tr>
    </table>
</html>

# Usage
The design and implementation follows simple principles(**graph in,embedding out**) as much as possible.
## Input format
we use `networkx`to create graphs.The input of networkx graph is as follows:
`node1 node2 <edge_weight>`

![](./pics/edge_list.png)
## DeepWalk

```python
G = nx.read_edgelist('../data/wiki/Wiki_edgelist.txt',create_using=nx.DiGraph(),nodetype=None,data=[('weight',int)])# Read graph

model = DeepWalk(G,walk_length=10,num_walks=80,workers=1)#init model
model.train(window_size=5,iter=3)# train model
embeddings = model.get_embeddings()# get embedding vectors
```

## LINE

```python
G = nx.read_edgelist('../data/wiki/Wiki_edgelist.txt',create_using=nx.DiGraph(),nodetype=None,data=[('weight',int)])#read graph

model = LINE(G,embedding_size=128,order='second') #init model,order can be ['first','second','all']
model.train(batch_size=1024,epochs=50,verbose=2)# train model
embeddings = model.get_embeddings()# get embedding vectors
```
## Node2Vec
```python
G=nx.read_edgelist('../data/wiki/Wiki_edgelist.txt',
                        create_using = nx.DiGraph(), nodetype = None, data = [('weight', int)])#read graph

model = Node2Vec(G, walk_length = 10, num_walks = 80,p = 0.25, q = 4, workers = 1)#init model
model.train(window_size = 5, iter = 3)# train model
embeddings = model.get_embeddings()# get embedding vectors
```
## SDNE

```python
G = nx.read_edgelist('../data/wiki/Wiki_edgelist.txt',create_using=nx.DiGraph(),nodetype=None,data=[('weight',int)])#read graph

model = SDNE(G,hidden_size=[256,128]) #init model
model.train(batch_size=3000,epochs=40,verbose=2)# train model
embeddings = model.get_embeddings()# get embedding vectors
```

## Struc2Vec


```python
G = nx.read_edgelist('../data/flight/brazil-airports.edgelist',create_using=nx.DiGraph(),nodetype=None,data=[('weight',int)])#read graph

model = model = Struc2Vec(G, 10, 80, workers=4, verbose=40, ) #init model
model.train(window_size = 5, iter = 3)# train model
embeddings = model.get_embeddings()# get embedding vectors
```
