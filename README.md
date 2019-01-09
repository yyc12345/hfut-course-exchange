# hfut-course-sxchange

鉴于各种刷课脚本横行，特制作此换课脚本以方便各位进行安全换课。

## 写在前面

此换课脚本**不能**100%保证换课成功，但相较于手动换课成功率会提高不少。当你执行换课脚本的时候，如果他人的刷课脚本正好被触发了，那么就会很遗憾，你的课被截了。

感谢[Dawnnnnnn/hfut-course](https://github.com/Dawnnnnnn/hfut-course)的刷课脚本，我是在它的基础上改造出来的。

一切刷课脚本与截课脚本都应当下地狱

## 使用说明

重点：目前版本只支持用户位数为5位数的用户换课，请勿使用六位数的账户执行换课

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

## 原理分析

观看了一部分截课，刷课脚本，共同点都是用了`sleep()`来防止被服务器干掉，本程序就是将选课和退课两部分之间的时间尽量缩短，以达到在截课刷课机器`sleep()`的时候完成换课

但是运气不佳会发生刚退课就被刷课机器截取的情况。
