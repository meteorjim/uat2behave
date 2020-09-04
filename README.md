# Uiautomator2 BDD测试框架说明

## 框架介绍

### 相关概念解释

#### 1. [BDD](https://baike.baidu.com/item/%E8%A1%8C%E4%B8%BA%E9%A9%B1%E5%8A%A8%E5%BC%80%E5%8F%91/9424963)

行为驱动开发(BDD)是测试驱动开发的延伸，开发使用简单的，特定于领域的脚本语言。这些DSL将结构化自然语言语句转换为可执行测试。结果是与给定功能的验收标准以及用于验证该功能的测试之间的关系更密切。因此，它一般是测试驱动开发(TDD)测试的自然延伸。

#### 2. [gherkin](https://www.jianshu.com/p/43cb0e79f075)

使用 `Feature`, `Scenario`, `Given`, `When`, `Then`, `And`, `But` 来描述软件行为的, 有商业可读性,领域特定语言, 用于描述软件的行为且不需要关心这个行为的如何实现的。

### 引用包介绍

`pip install -r requirement.txt`

#### 1. [uiautomator2](https://github.com/openatx/uiautomator2)

UiAutomator是Google提供的用来做安卓自动化测试的一个Java库，基于Accessibility服务。而uiautomator2则是将uiautomator中的功能开放出来，在手机上运行了一个http rpc服务，然后再将这些http接口封装成Python库。

#### 2. [behave](https://github.com/behave/behave)

behave 是由python编写与驱动并通过自然语言 (gherkin) 编写测试脚本的工具

behave uses tests written in a natural language style, backed up by Python code.

#### 3. [weditor](https://github.com/alibaba/web-editor) !非必须

类似于uiautomatorviewer，专门为本项目开发的辅助编辑器
编辑器能够提供辅助编写脚本，查看组件信息，调试代码等功能。

### 目录结构解析

```dir tree table
uat2
 ┣ features             用于存放测试用例脚本与'步骤'文件(behave 需要调用结构)
 ┃ ┣ steps              用于存放'步骤'文件
 ┃ ┃ ┣ common_step.py   通用步骤(不建议修改)
 ┃ ┃ ┗ (name)_step.py   通过initial.py生成,用于编写APP相关专用步骤
 ┃ ┃
 ┃ ┣ test_cases         测试用例脚本
 ┃ ┃ ┗ (name).feature   用户自行添加 gherkin 脚本
 ┃ ┃
 ┃ ┗ environment.py     behave框架需要, 测试初始化等代码(不建议修改)
 ┃
 ┣ page_objects         page object model设计模式
 ┃ ┣ (name)             通过initial.py生成
 ┃ ┃ ┣ locators.py      通过initial.py生成, 用于定义各个页面元素以及定位方式
 ┃ ┃ ┣ pages.py         通过initial.py生成, 用于定义各个页面的page_object
 ┃ ┃ ┗ __init__.py      通过initial.py生成，用于定义page_creator，page类别名相关
 ┃ ┃
 ┃ ┣ base_objects.py    page, locator, creator的基础类, 不建议修改
 ┃ ┗ __init__.py        全量引入不要修改
 ┃
 ┣ tools
 ┃ ┗ locator_creator.py weditor抓取元素后生成locator的中间插件
 ┃
 ┣ initial.py           初始化测试脚本
 ┣ logger.conf
 ┣ requirement.txt
 ┣ setup.cfg
 ┗ uat2.conf
```

## 建议使用方法【暂定】

1. 新创建项目，使用`python initial -s 项目名(建议英文缩写) -p 程序包`
2. 在 `page_object/***/page.py` 中定义页面类
3. 在 `page_object/***/__init__.py` 中定义页面类的别名
4. 使用 `weditor` 抓取页面元素，并通过 `tools/locator_creator.py` 转换并定义元素名，复制到`page_object/***/locator.py`中
5. 愉快的使用gherkin语言编写 `***.feature`文件生成测试脚本
6. 脚本运行方法：`behave --no-capture -m --no-capture-stderr ***.feature`
