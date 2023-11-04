# bilibili用户接口分析

## 用户页面入口

**https://space.bilibili.com/{uid}**   
自己写完才发现现成的轮子 , 感激不尽 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md    
/x/space 下的api限流最严重, 大概150/5min就会限流, 携带登录信息的cookie会好一些

    基本信息 
        https://api.bilibili.com/x/space/wbi/acc/info?mid={uid}
            必须带wts w_rid字段验证 , ua有时会验证, 带一个合法的即可
            部分ip访问 需要cookie中 buvid3被验证
                # 最下面说明buvid3获取方式
        字段分析(只说明重要字段) :
            mid : uid
            name : 名称
            sex : 性别 男/女 保密
            face : 头像
            sign : 个人简介
            rank : 用户权限等级 大部分为10000 普通会员
            level : 等级 0-6
            jointime : 入站时间? 本接口只有0
            coins : 硬币数 , 只能看自己的 默认0
            fans_badge fans_medal 粉丝徽章 不爬
            official : 官方认证信息
                role : 0-9等 
                title
                desc
                type : 是否认证 -1 无, 0 个人, 1 机构
            vip : 大会员信息
                type : 0无, 1月会员, 2年以上会员
                status : 状态 0无, 1有效
                due_date : 截止日期
                label.text : 大会员文本 (年度大会员|十年大会员...)
            nameplate : 勋章信息
            birthday : 生日 MM-DD
            school : 学校 很少有人写 不爬
            tags : 个人标签 字符串列表 没什么标准 不爬

        曲线救国 通过直播间获得up信息
            https://api.live.bilibili.com/live_user/v1/Master/info?uid={uid}
            优点: 几乎无限流 缺点: 信息缺失
            info 基本信息
                uid : uid
                uname : 名称
                face : 头像
                gender : 性别 -1 保密, 0 女, 1 男
                official_verify 认证信息
                    type : -1无 , 0 个人认证 , 1 机构认证
                    desc : 认证描述
            exp 主播直播等级信息 不重要
            follower_num : 主播粉丝数
            room_news : 直播间信息
            room_id : 直播间id

    关注数 粉丝数信息
        https://api.bilibili.com/x/relation/stat?vmid={uid}
        字段分析 :
            following : 关注数
            follower : 粉丝数

    播放数 获赞数信息
        https://api.bilibili.com/x/space/upstat?mid={uid}
        字段分析:
            archive.view : 播放数
            article.view : 文章阅览数
            likes : 获赞数

    投稿信息 订阅信息
        https://api.bilibili.com/x/space/navnum?mid={uid}
        字段分析:
            video : 视频数
            article : 专栏数
            album : 相簿数
            audio : 音频数
            bangumi : 追番数
            cinema : 追剧数
            channel : 合集和列表
            favourite : 收藏夹
            tag : 订阅标签数

    充电信息
        https://api.bilibili.com/x/ugcpay-rank/elec/month/up?up_mid={uid}
        字段分析:
            count : 本月充电
            total_count : 总数
            total : 也是总数

    uid分析
        10位及之前的uid为顺序生成
        16位uid生成规则未知 , 比较分散 , 并且多为新用户, 放弃爬取

    游客获取cookie中的buvid3和buvid4属性
        # 逆向参考BiliWbi类 , 一个类似uuid的数据, 只要合法即可
        接口 https://api.bilibili.com/x/frontend/finger/spi   
        {"code":0,"data":{"b_3":"65F6A82B-DB6C-1B13-9D7D-D2DD17C3D26986443infoc","b_4":"530CBDDF-EA9E-5871-A18E-FC24C32899BA86443-023110220-oRXBPz1sNw5ZQHkb+gth7w=="},"message":"ok"}

## 多用户详细信息接口
    https://api.vc.bilibili.com/account/v1/user/cards?uids=uid1,uid2,uid3
    参数: uids: uid列表 最多50个
    验证: 可能需要cookie中携带SESSDATA #登录用户 
    字段解析: 
        code : 
            0成功, -400 请求错误, 600006 参数错误,  600007 超过数量限制
            600003 主站返回数据为空 # 访问过快触发限流??
        data : 用户数据列表
            详细字段参考 基本信息接口 基本一致
