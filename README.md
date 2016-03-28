# Pholcus
[![Build Status](https://api.travis-ci.org/listen-lavender/pholcus.svg?branch=master)](https://api.travis-ci.org/listen-lavender/pholcus)

pholcus是一个抓取管理平台，目前支持脚本，任务，数据和用户的管理，方便协作。

其实我觉得任何跑数据的脚本任务都可以用pholcus集中管理，方便复用查看和跨部门协作。pholcus的理想状态是在server段能通过配置data source和data path就能自动生成抓取脚本，godhand.py就是一个努力过的痕迹，鉴于生成结果不稳定，暂时不能实现。现状还是由开发人员开发以后注册，但是可以在线调整代码。

我join的第一个创业团队是快捷酒店团队，也是team leader老赵带我做爬虫工作的，感谢他的引导。

## gds

Server of pholcus

- 管理脚本，包括脚本注册，脚本分发、脚本粒度参数控制，脚本在线热调整和脚本权限。
- 管理任务，包括任务的执行控制，任务的日志跟踪，任务粒度参数调整，任务的报表。
- 管理数据，包括数据查看，数据的push和pull。
- 管理用户，支持管理员administrator，开发者developer和运营operator三类用户管理。

## gdc

Client of pholcus.

- 脚本工程构建
- 脚本工程部署


## Installation

    参见gds和gdc的read me

## Discussion and support

Report bugs on the *GitHub issue tracker <https://github.com/listen-lavender/pholcus/issues*. 