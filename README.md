# hfut-course-exchange

鉴于各种刷课脚本横行，特制作此换课脚本以方便各位进行安全换课。

## 写在前面

此换课脚本**不能**100%保证换课成功，但相较于手动换课成功率会提高不少。当你执行换课脚本的时候，如果他人的刷课脚本正好被触发了，那么就会很遗憾，你的课被截了。

感谢[Dawnnnnnn/hfut-course](https://github.com/Dawnnnnnn/hfut-course)的刷课脚本，我是在它的基础上改造出来的。

## 使用说明

### 环境安装

程序在Python 3.6下测试通过，建议安装Python 3.6

需要安装一个必要的库，使用`pip install requests`来安装

### 运行配置

运行之前，你需要先配置`config.py`。

`giver_`是课程给出者，`receiver_`是课程接收者。

`username`是用户名，`password`是密码

然后你就配置好了交换双方的账户和密码

我们来配置课程

`lesson`是课程ID，获取方法：右键你想要换的课程的选课按钮，选择审查元素，然后把`data-id`属性的值复制进来就行

`turn`指示当前选课轮数，对于2018-2019学年第二学期二轮选课中，必修选课填写`321`，公选和体育填写`322`

### 运行

目录下执行`py exchange.py`即可运行

理论上有3个结果：**交换成功**，**交换失败但是一切如初**以及**被截课**

理论上不会出现错误，如果出现错误（输出了一堆堆栈），请仔细检查你的配置或网络连接

### 高级脚本

如果你注意了目录下的文件，你会注意到还有一个`exchange-test.py`。这也是一个换课脚本，并且做了理论上得最优优化，能以最短间隔发出退课和选课得数据包。并在发完所有数据包（退课，选课，尝试回选）之后再判定结果。

由于`exchange.py`被反馈说还有可能被刷课（据说是6掉1的概率），故出此*邪招*，但是，`exchange-test.py`**不保证安全性**，因为这脚本没有经过详细测试，只是通过抓包提示得知选课可以成功。

`exchange-test.py`不会给你任何可读显示，只会显示三个操作的结果，结果是一个`bool`。这里列出表格，以辅助你检查结果：

|Drop course status|Add course status|Re-add course status|结果|
|:---|:---|:---|:---|
|True|True|True|你截了别人的课。~~还不赶快向全校学生谢罪？~~|
|True|True|False|**换课成功**|
|True|False|True|**没换成功，但是一切如初**|
|True|False|False|**被截课**|
|False|True|True|*常规操作无法复现此结果（你乱玩我就不保证了）*|
|False|True|False|*常规操作无法复现此结果（你乱玩我就不保证了）*|
|False|False|True|*常规操作无法复现此结果（你乱玩我就不保证了）*|
|False|False|False|无法退课|

## 原理分析

观看了一部分截课，刷课脚本，共同点都是用了`sleep()`来防止被服务器干掉，本程序就是将选课和退课两部分之间的时间尽量缩短，以达到在截课刷课机器`sleep()`的时候完成换课

但是运气不佳会发生刚退课就被刷课机器截取的情况。
