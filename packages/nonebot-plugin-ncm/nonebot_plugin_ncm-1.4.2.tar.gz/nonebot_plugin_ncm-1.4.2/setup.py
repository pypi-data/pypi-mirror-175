# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot-plugin-ncm']

package_data = \
{'': ['*']}

install_requires = \
['aiofile>=3.7.4,<4.0.0',
 'nonebot-adapter-onebot>=2.0.0b1,<3.0.0',
 'nonebot2>=2.0.0b1,<3.0.0',
 'pyncm>=1.6.8.2.2,<2.0.0.0.0',
 'qrcode>=7.3.1,<8.0.0',
 'tinydb>=4.7.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ncm',
    'version': '1.4.2',
    'description': '基于go-cqhttp与nonebot2的 网易云 无损音乐下载',
    'long_description': '\n\n<p align="center">\n  <img src="https://files.catbox.moe/7cy61g.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-ncm\n\n✨ 基于go-cqhttp与nonebot2的 网易云 无损音乐 点歌/下载 ✨\n</div>\n\n<p align="center">\n  <a href="https://github.com/kitUIN/nonebot-plugin-ncm/blob/master/LICENSE">\n    <img src="https://img.shields.io/badge/license-Apache--2.0-green" alt="license">\n  </a>\n  <a href="https://github.com/nonebot/nonebot2/releases/tag/v2.0.0-rc.1">\n    <img src="https://img.shields.io/static/v1?label=nonebot2&message=v2.0.0-rc.1&color=brightgreen" alt="nonebot">\n  </a>\n  <a href="https://github.com/kitUIN/nonebot-plugin-ncm/releases">\n    <img src="https://img.shields.io/github/v/release/kitUIN/nonebot-plugin-ncm" alt="release">\n  </a>\n  <a href="https://wakatime.com/badge/user/3b5608c7-e0b6-44a2-a217-cad786040b48/project/2a431792-e82f-48f5-839c-9ee566910fe5"><img src="https://wakatime.com/badge/user/3b5608c7-e0b6-44a2-a217-cad786040b48/project/2a431792-e82f-48f5-839c-9ee566910fe5.svg" alt="wakatime"></a>\n</p>\n\n\n## 安装\n### 使用pip安装\n1.`pip install nonebot-plugin-ncm` 进行安装  \n2.并在`bot.py`添加`nonebot.load_plugin(\'nonebot-plugin-ncm\')`\n### 使用nb-cli安装(推荐)\n`nb plugin install nonebot-plugin-ncm` 进行安装\n\n<details>\n  <summary>如果希望使用`nonebot2 a16`及以下版本 </summary>\n  请使用`pip install nonebot-plugin-ncm==1.1.0`进行安装\n</details>\n\n### 命令列表：\n| 命令     | 备注     |\n|--------|--------|\n| /ncm   | 获取命令菜单 |\n| /ncm t | 开启解析   |\n| /ncm f | 关闭解析   |\n| /点歌 歌名 | 点歌     |\n- 命令开始符号会自动识别[`COMMAND_START`](https://v2.nonebot.dev/docs/api/config#Config-command_start)项\n\n## 注意说明\n- 使用的网易云账号**需要拥有黑胶VIP**\n- **默认解析状态为关闭，请在每个群内使用`/ncm t`开启** (或者使用配置中的`white_list`项批量导入需要开启的群号)\n- 默认下载最高音质的音乐 \n- 本程序实质为调用web接口下载音乐上传  \n- 网易云单曲分享到群内会自动解析下载  \n- **仅限群聊使用！！！(因为go-cqhttp还不支持好友发文件)**  \n- **回复bot消息即可自动下载上传音乐文件(回复消息不输入内容也行)**\n- **低版本升级至1.0.0版本请删掉db文件夹**  \n\n## 配置文件说明\n```\nncm_admin=["owner", "admin"] # 设置命令权限（非解析下载，仅解析功能开关设置）\nncm_phone=  # 手机登录\nncm_password=  # 密码\n# 总开关开启后在每个群内依旧是默认关闭的\nncm_song=True  # 单曲解析功能总开关\nncm_list=True  # 歌单解析功能总开关\nncm_search=True  # 点歌功能总开关\nwhite_list=[]  # 白名单一键导入\n```\n\n\n## 功能列表\n- [x] 识别/下载 网易云单曲\n    - 链接\n    - 卡片\n    - 卡片转发\n- [x] 识别/下载 网易云歌单    \n    - 链接\n    - 卡片\n    - 卡片转发\n- [x] 点歌(网易云)\n- [ ] QQ音乐无损下载\n### 示例图\n<details>\n  <summary>点击查看详细内容</summary>\n\n  **单曲**  \n  [![WqbK7d.png](https://z3.ax1x.com/2021/07/30/WqbK7d.png)](https://imgtu.com/i/WqbK7d)\n  **歌单**  \n  [![WqbQAA.png](https://z3.ax1x.com/2021/07/30/WqbQAA.png)](https://imgtu.com/i/WqbQAA)  \n  \n</details>\n\n# 鸣谢\n- [pyncm](https://github.com/greats3an/pyncm)\n- [nonebot2](https://github.com/nonebot/nonebot2)\n',
    'author': 'kitUIN',
    'author_email': 'kulujun@gmail.com',
    'maintainer': 'kitUIN',
    'maintainer_email': 'kulujun@gmail.com',
    'url': 'https://github.com/kitUIN/nonebot-plugin-ncm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
