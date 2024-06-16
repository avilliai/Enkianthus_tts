import asyncio
import json
import random

import httpx
import requests
import websockets as websockets

fireflySpeaker = ['消沉的患者_ZH', '九条孝行_JP', '岩夫_EN', '芷巧_EN', '阿扎尔_EN', '芙萝拉_JP', '花火_ZH', '萨姆_EN', '邓恩_JP', '轰大叔_ZH',
                  '重佐_JP', '希儿_ZH', '希露瓦_ZH', '捕头_EN', '一之濑明日奈', '珐露珊母亲_JP', '长生_ZH', '铁尔南_JP', '理村爱理', '柴田_JP',
                  '可可利亚_EN', '艾伯特_JP', '阿圆_JP', '流萤_EN', '舍利夫_EN', '耕一_ZH', '米卡_EN', '埃洛伊_EN', '科尔特_ZH', '裁判_EN',
                  '戴因斯雷布_EN', '高善_JP', '狮子堂泉', '托帕&账账_ZH', '埃舍尔_ZH', '空井咲', '接笏_ZH', '佐天泪子', '百闻_JP', '杰帕德_JP',
                  '柊千里_JP', '博来_EN', '消沉的患者_JP', '田铁嘴_JP', '梦主_EN', '娜塔莎_JP', '阿守_ZH', '娜比雅_ZH', '镜流_ZH', '珊瑚_EN',
                  '昆钧_JP', '朔次郎_EN', '琳妮特_JP', '木木_JP', '查尔斯_ZH', '紫月季_EN', '留云借风真君_ZH', '莫娜_ZH', '克雷薇_ZH',
                  '霍夫曼_ZH', '净砚_EN', '桑博_EN', '弗洛朗_JP', '埃斯蒙德_JP', 'shajinma_ZH', '艾伦_EN', '甘雨_EN', '停云_JP',
                  '拉赫曼_JP', '海妮耶_JP', '羽生田千鹤_JP', '莲见（体操服）', '卡莉娜_JP', '罗莎莉亚_ZH', '隐书_ZH', '金人会长_EN', '观众_JP',
                  '大隆_EN', '凯西娅_JP', '木木_EN', '深渊使徒_EN', '秋泉红叶', '丹吉尔_ZH', '卢卡奇_JP', '温迪_ZH', '室笠朱音(茜)', '慧心_JP',
                  '老章_JP', 'shajinma_EN', '拉赫曼_ZH', '大慈树王_ZH', '夏洛蒂_ZH', '小野寺_JP', '皮特_JP', '今谷三郎_JP', '广大_JP',
                  '星_ZH', '林尼_ZH', '坎蒂丝_ZH', '吴船长_ZH', '胡尚_EN', '浅黄睦月', '公司的业务员代表_JP', '若叶日向', '乌宰尔_JP', '萨赫哈蒂_EN',
                  '斯科特_ZH', '法拉娜_ZH', '朝颜花江', '宏达_EN', '芙宁娜_ZH', '霄老大_EN', '甘雨_JP', '娜德瓦_ZH', '宁禄_JP', '贝雅特丽奇_JP',
                  '螺丝咕姆_JP', '雷泽_EN', '恕筠_EN', '金忽律_ZH', '帕维耶_EN', '间宵时雨', '巨大谜钟_EN', '黑泽京之介_ZH', '菲谢尔_ZH',
                  '阿山婆_JP', '萨姆_ZH', '砂金_JP', '舍利夫_ZH', '绮良良_ZH', '赛索斯_JP', '上杉_JP', '炒冷饭机器人_ZH', '巴达维_ZH',
                  '宫子（泳装）', '杜吉耶_EN', '秤亚津子', '古关忧', '将司_EN', '黛比_JP', '玛吉_JP', '丽莎_ZH', '维利特_EN', '知贵_JP',
                  '记忆中的声音_ZH', '夜兰_ZH', '木南杏奈_EN', '凯亚_ZH', '韵宁_EN', '巴尔塔萨_JP', '波提欧_JP', '忧（泳装）', '丹羽_EN', '老高_EN',
                  '戴因斯雷布_ZH', '乔瓦尼_ZH', '日奈（泳装）', '角楯花凛', '阿汉格尔_ZH', '钱德拉_JP', '才羽桃井', '莫塞伊思_JP', '光之_JP', '幻胧_ZH',
                  '立本_EN', '河和静子', '娜塔莎_EN', '波提欧_EN', '讨嫌的小孩_ZH', '科林斯_ZH', '北斗_JP', '烟绯_EN', '班尼特_ZH', '安静的宾客_JP',
                  '劳维克_JP', '琴_JP', '黑天鹅_JP', '丹恒•饮月_EN', '药王秘传魁首_ZH', '黛比_ZH', '辛焱_EN', '丹枢_EN', '重云_ZH',
                  '木南杏奈_ZH', '毗伽尔_JP', '卡卡瓦夏的姐姐_EN', '莱欧斯利_ZH', '黑田_ZH', '柯莱_EN', '造物翻译官_JP', '艾伯特_EN', '小野寺_ZH',
                  '徐六石_ZH', '葵_ZH', '罗刹_EN', '鹤城（泳装）', '雅各_JP', '响（应援团）', '凯西娅_EN', '札齐_ZH', '副警长_ZH', '荒谷_EN',
                  '九条裟罗_ZH', '瑞安维尔_JP', '接笏_EN', '罗莎莉亚_JP', '维格尔_EN', '裁判_JP', '新之丞_EN', '若心_JP', '温和的声音_ZH',
                  '布洛克_JP', '菲谢尔_JP', '神里绫人_JP', '立本_ZH', '沙扎曼_ZH', '卡波特_ZH', '深渊法师_JP', '重佐_ZH', '琳琅_JP',
                  '维多利亚_EN', '尚博迪克_EN', '宛烟_ZH', '鹿野院平藏_ZH', '博士_JP', '费迪南德_JP', '伊莎朵_ZH', '莎拉_EN', '老戴_JP',
                  '拉齐_JP', '削月筑阳真君_JP', '绮良良_JP', '小乐_ZH', '芙卡洛斯_EN', '玻瑞亚斯_ZH', '安柏_JP', '博来_ZH', '伯恩哈德_ZH',
                  '锭前纱织', '斯薇塔_ZH', '夏彦', '加拉赫_JP', '砂糖_ZH', '法赫尔_JP', '法哈德_EN', '白露_EN', '阿扎木_EN', '提纳里_EN',
                  '商人_EN', '瓦尔特_JP', '瓦乐瑞娜_ZH', '加福尔_JP', '莺儿_EN', '毗伽尔_EN', '海芭夏_ZH', '胡尚_ZH', '劳伦斯_ZH', '毗伽尔_ZH',
                  '白术_EN', '杰娜姬_JP', '芹香（正月）', '胡尚_JP', '小乐_JP', '派蒙_EN', '真_JP', '元太_EN', '瑶瑶_JP', '狐妖_JP',
                  '捕快_ZH', '阿尔卡米_EN', '老孟_JP', '安西_EN', '赤司纯子', '皮特_ZH', '桐生桔梗', '阿祇_ZH', '薇若妮卡_EN', '菲米尼_EN',
                  '西衍先生_EN', '刻薄的小孩_JP', '半夏_EN', '警长_JP', '札齐_EN', '石头老板_JP', '老孟_ZH', '大肉丸_ZH', '符玄_EN', '古谷升_JP',
                  '贝雅特丽奇_EN', '卡萝蕾_EN', '佩拉_JP', '花角玉将_EN', '桂乃芬_ZH', '贝雅特丽奇_ZH', '凯西娅_ZH', '埃斯蒙德_EN', '杜吉耶_JP',
                  '胡桃_ZH', '蒂埃里_JP', '纳菲斯_JP', '琳琅_EN', '嘉义_ZH', '温世玲_JP', '今谷佳祐_JP', '肢体评委_EN', '伊利亚斯_JP', '扇喜葵',
                  '劳维克_ZH', '那维莱特_ZH', '卡莉娜_ZH', '香菱_ZH', '齐米亚_JP', '迪娜泽黛_EN', '岩明_ZH', '阿鸠_JP', '马姆杜_JP', '面具_EN',
                  '北斗_ZH', '纳比尔_EN', '歌蒂_JP', '伯恩哈德_JP', '塞萨尔的日记_JP', '稻生_EN', '卡芙卡_ZH', '罗刹_JP', '年长的患者_JP',
                  '玲可_ZH', '往昔的回声_JP', '筑梦师_EN', '卡莉娜_EN', '安西_JP', '年长的患者_ZH', '萨赫哈蒂_ZH', '阿仁_JP', '常九爷_JP',
                  '塞萨尔的日记_ZH', '发抖的流浪者_EN', '阿雩_EN', '奥泰巴_ZH', '久利须_EN', '朔次郎_JP', '莎拉_ZH', '小仓澪_ZH', '菲米尼_ZH',
                  '丹花伊吹', '巴达维_EN', '迈蒙_EN', '阿伟_EN', '音濑小玉', '托帕&账账_JP', '萍姥姥_ZH', '巴穆恩_EN', '白石歌原', '厨子_EN',
                  '悠策_EN', '萨齐因_EN', '妮露_JP', '狐妖_EN', '阿蕾奇诺_EN', '水羽三森', '浮游风蕈兽·元素生命_ZH', '阿守_JP', '元太_ZH',
                  '福尔茨_ZH', '狐妖_ZH', '星期日_JP', '安武_EN', '阿来_ZH', '北村_JP', '唐娜_ZH', '纳菲斯_EN', '白洲梓', '妮露_ZH',
                  '楠楠_JP', '拍卖会工作人员_JP', '布洛妮娅_EN', '陆行岩本真蕈·元素生命_EN', '刻晴_EN', '笼钓瓶一心_EN', '枫原万叶_JP', '深渊法师_ZH',
                  '刃_ZH', '卡维_EN', '欧菲妮_ZH', '长生_JP', '鹿野院平藏_JP', '天叔_EN', '浮烟_ZH', '马姆杜_ZH', '漱玉_JP', '伊萨克_EN',
                  '楚仪_JP', '考特里亚_JP', '古田_EN', '宇泽玲纱', '新之丞_ZH', '华劳斯_JP', '星稀_EN', '宁禄_ZH', '梅里埃_JP', '迪肯_JP',
                  '长生_EN', '丹羽_JP', '闲云_ZH', '希格雯_ZH', '洛恩_EN', '厨子_JP', '奇妙的船_EN', '消沉的患者_EN', '莫里斯_JP', '帕姆_EN',
                  '老高_JP', '时（兔女郎）', '明曦_JP', '阿斯法德_JP', '维卡斯_JP', '三田_EN', '式大将_ZH', '拉伊德_EN', '辛焱_JP', '迪希雅_ZH',
                  '筑梦师_ZH', '卡布斯_ZH', '托马_ZH', '芭芭拉_ZH', '星稀_ZH', '塔杰·拉德卡尼_JP', '丹恒_ZH', '绿芙蓉_EN', '谢赫祖拜尔_ZH',
                  '西衍先生_JP', '梦主_JP', '歌蒂_ZH', '库塞拉_JP', '大辅_EN', '波洛_ZH', '巴哈利_EN', '卡卡瓦夏_EN', '贝努瓦_EN', '老芬奇_ZH',
                  '辛克尔_JP', '霍夫曼_EN', '布尔米耶_JP', '公输师傅_ZH', '玛文_EN', '被俘的信徒_JP', '慈祥的女声_ZH', '恶龙_ZH', '回声海螺_ZH',
                  '埃勒曼_EN', '真理医生_ZH', '爱德华医生_ZH', '奇妙的船_ZH', '药子纱绫', '法赫尔_EN', '神里绫华_EN', '埃泽_ZH', '昆恩_JP',
                  '夏妮_ZH', '陆景和', '信博_JP', '科玫_JP', '言笑_JP', '罗莎莉亚_EN', '旁白_ZH', '嘉明_EN', '伊丝黛莱_ZH', '伊原木好美',
                  '玛达赫_ZH', '卡布斯_JP', '凯瑟琳_JP', '康纳_EN', '青镞_ZH', '罗巧_EN', '鬼方佳代子', '久岐忍_ZH', '稻生_JP', '厨子_ZH',
                  '猎犬家系成员_EN', '卯师傅_EN', '行秋_ZH', '浮游水蕈兽·元素生命_JP', '塞琉斯_EN', '久岐忍_EN', '埃泽_EN', '乌维_EN', '柊千里_ZH',
                  '行秋_EN', '马姆杜_EN', '花火_EN', '今谷香里_JP', '阿基维利_JP', '垃垃撕圾_ZH', '保姆_JP', '拉格沃克•夏尔•米哈伊尔_EN',
                  '瓦乐瑞娜_EN', '舒翁_JP', '天雨亚子', '莺儿_ZH', '有乐斋_EN', '捕快_EN', '剑阵中的声音_EN', '玥辉_EN', '斑目百兵卫_JP',
                  '阿蕾奇诺_ZH', '赛索斯_EN', '诗筠_EN', '商人_ZH', '大和田_JP', '塔里克_EN', '艾文_ZH', '吉莲_EN', '砂金_ZH', '阿慈谷日富美',
                  '希格雯_JP', '月雪宫子', '优菈_ZH', '公主_EN', '维多克_EN', '拉齐_ZH', '理查_JP', '希儿_EN', '行秋_JP', '钟表小子_JP',
                  '重云_JP', '阿幸_EN', '界种科科员_JP', '藿藿_EN', '钟表匠_JP', 'asideb_EN', '里卡尔_EN', '塔杰·拉德卡尼_ZH', '埃勒曼_JP',
                  '小钩晴', '卡玛尔_JP', '商华_ZH', '帕斯卡_EN', '银枝_ZH', '米凯_ZH', '嚣张的小孩_ZH', '达达利亚_JP', '塔杰·拉德卡尼_EN',
                  '加藤洋平_ZH', '蒂玛乌斯_ZH', '阿维丝_JP', '大慈树王_JP', '荒泷一斗_ZH', '鹿野奈奈_EN', '史瓦罗_EN', '常九爷_EN', '阿往_ZH',
                  '克拉拉_ZH', '绘星_EN', '杜拉夫_ZH', '引导员_JP', '塞塔蕾_JP', '露子_JP', '夜兰_JP', '银狼_JP', '伊洁贝儿_JP', '竺子_ZH',
                  '阿夫辛_EN', '伊落玛丽', '荒泷一斗_JP', '荒泷一斗_EN', '阿雩_JP', '石头老板_ZH', '白露_JP', '旅行者_ZH', '亚卡巴_ZH',
                  '九条镰治_ZH', '萨福万_JP', '苍老的声音_JP', '百识_JP', '陸八魔阿露', '霄翰_EN', '小川_JP', '西瓦尼_ZH', '花冈柚子', '冰室濑名',
                  '吴船长_EN', '勘解由小路紫', '克洛琳德_ZH', '素裳_JP', '青镞_JP', '拉赫曼_EN', '爱贝尔_EN', '艾米绮_ZH', '伊萨克_ZH',
                  '伊利亚斯_EN', '安托万_JP', '维多利亚_ZH', '阿泰菲_EN', '达达利亚_EN', '安静的宾客_ZH', '陆行岩本真蕈·元素生命_JP', '青雀_ZH',
                  '侯章_ZH', '诺艾尔_JP', '星期日_EN', '帕维耶_ZH', '界种科科员_EN', '伽吠毗陀_EN', '智树_ZH', '暮夜剧团团长_JP', '魔女N_JP',
                  '斯万_JP', '银杏_ZH', '戴派_EN', '维尔芒_EN', '慧心_ZH', '沃特林_JP', '阿佩普_EN', '艾尔海森_JP', '女士_ZH',
                  '拉格沃克•夏尔•米哈伊尔_ZH', '枫_JP', '博士_ZH', '温迪_JP', '梅里埃_ZH', '绮珊_EN', '琳妮特_EN', '辛克尔_EN', '柴田_EN',
                  '天见和香', '阿扎尔_JP', '芭芭拉_JP', '莱依拉_JP', '莱昂_JP', '艾丝妲_ZH', '葛瑞丝_JP', '松烟_JP', '珊瑚宫心海_ZH', '钱德拉_EN',
                  '乐平波琳_EN', '埃舍尔_JP', '玥辉_JP', '阿守_EN', '贾拉康_JP', '阿巴图伊_ZH', '拉伊德_ZH', '艾薇拉_EN', '宵宫_ZH', '女声_EN',
                  '布洛妮娅_ZH', '黄泉_ZH', '安托万_EN', '玛塞勒_JP', '慈祥的女声_JP', '卢卡_JP', '恕筠_JP', '薇娜_EN', '阿尼斯_JP', '夏洛蒂_EN',
                  '阿贝多_EN', '丝柯克_EN', '迪娜泽黛_JP', '砂糖_EN', '卡维_JP', '御坂美琴', '羽沼真琴', '阿祇_EN', '年长的患者_EN', '神里绫华_ZH',
                  '维多利亚_JP', '维尔芒_ZH', '柊千里_EN', '玛乔丽_JP', '那维莱特_EN', '坎蒂丝_EN', '重佐_EN', '雷泽_JP', '库斯图_JP', '寒鸦_ZH',
                  '天目十五_JP', '焦躁的丹鼎司医士_EN', '副警长_JP', '燕翠_EN', '初音未来', '空_ZH', '莫塞伊思_EN', '艾米绮_JP', '猎犬家系成员_ZH',
                  '莱提西娅_JP', '巴穆恩_ZH', '纳比尔_ZH', '法伊兹_EN', '刻薄的小孩_ZH', '诗筠_JP', '钟表匠_ZH', '千织_EN', '祖莉亚·德斯特雷_JP',
                  '华劳斯_ZH', '慈祥的女声_EN', '塞塔蕾_ZH', '造物翻译官_EN', '艾丝妲_JP', '费迪南德_ZH', '徐六石_EN', '朱里厄_JP', '真白（泳装）',
                  '阿旭_JP', '萨齐因_ZH', '维格尔_ZH', '新之丞_JP', '维卡斯_ZH', '七七_JP', '侯章_JP', '茂才公_EN', '顺吉_EN', '田铁嘴_ZH',
                  '宏达_JP', '法拉娜_EN', '巴穆恩_JP', '茂才公_ZH', '奥兹_EN', '一平_ZH', '戒野美咲', '韦尔纳_ZH', '天叔_JP', '阿汉格尔_EN',
                  '小贩_JP', '隐书_EN', '珐露珊_ZH', '白老先生_EN', '萍姥姥_EN', '菜菜子_EN', '派蒙_ZH', '伊迪娅_JP', '迪尔菲_EN', '叶德_JP',
                  '伽吠毗陀_JP', '银狼_EN', '掘掘博士_EN', '嘉义_JP', '珐露珊_EN', '基娅拉_JP', '托帕&账账_EN', '兴修_JP', '焦躁的丹鼎司医士_ZH',
                  '唐娜_JP', '公输师傅_JP', '贡达法_JP', '艾丝妲_EN', '神智昏乱的云骑_EN', '祖莉亚·德斯特雷_ZH', '三月七_EN', '天目十五_EN',
                  '伦纳德_JP', '长门幸子_EN', '小组长_JP', '才羽绿', '嘉义_EN', '咲（泳装）', '露尔薇_EN', '旅行者_JP', '捕快_JP', '笼钓瓶一心_ZH',
                  '黑馆晴奈', '蒂埃里_ZH', '青雀_EN', '妮欧莎_JP', '加拉赫_ZH', '薇尔_ZH', '守护者的意志_JP', '莎塔娜_EN', '阿尼斯_ZH', '波洛_EN',
                  '迪娜泽黛_ZH', '芭芭拉_EN', '大毫_EN', '阿露（正月）', '卯师傅_ZH', '讨嫌的小孩_EN', '朱达尔_JP', '雷电将军_ZH', '银杏_JP', '下仓惠',
                  '藿藿_JP', '加萨尼_EN', '夏妮_EN', '停云_EN', '埃德_EN', '罗伊斯_EN', '维卡斯_EN', '特纳_JP', '卡布斯_EN', '玛乔丽_ZH',
                  '若藻（泳装）', '慧心_EN', '法哈德_JP', '有原则的猎犬家系成员_EN', '朋义_EN', '悠策_JP', '丹吉尔_EN', '翡翠_JP',
                  '拉格沃克•夏尔•米哈伊尔_JP', '西尔弗_JP', '大隆_JP', '暮夜剧团团长_EN', '江蓠_EN', '杰洛尼_JP', '面具_JP', '奥泰巴_EN', '菲谢尔_EN',
                  '艾丽_ZH', '爱贝尔_ZH', '大和田_ZH', '哲平_JP', '可莉_ZH', '绮良良_EN', '阮•梅_ZH', '宵宫_JP', '烟绯_JP', '埃泽_JP',
                  '乌宰尔_EN', '三月七_JP', '卡维_ZH', '阿佩普_ZH', '凝光_JP', '镜流_EN', '有原则的猎犬家系成员_ZH', '奥兹_JP', '费索勒_ZH',
                  '艾迪恩_JP', '鬼婆婆_EN', '诺艾尔_EN', '七七_EN', '艾莉丝_ZH', '圆堂志美子', '各务千寻', '卡波特_EN', '薇若妮卡_ZH', '埃勒曼_ZH',
                  '杜吉耶_ZH', '斯坦利_JP', '希格雯_EN', '被俘的信徒_ZH', '镜流_JP', '冒失的帕拉德_JP', '古山_JP', '银镜伊织', '斯坦利_EN',
                  '淮安_JP', '露子_ZH', '西拉杰_ZH', '伊庭_JP', '阿洛瓦_ZH', '景元_ZH', '阿往_JP', '严苛评委_ZH', '丝柯克_JP',
                  '七叶寂照秘密主_EN', '泽维尔_EN', '发抖的流浪者_JP', '金忽律_EN', '紫月季_ZH', '歌住樱子', '徐六石_JP', '莫塞伊思_ZH', '岩夫_ZH',
                  '阿尼斯_EN', '卯师傅_JP', '重云_EN', '木木_ZH', '阿基维利_EN', '菲约尔_ZH', '被俘的信徒_EN', '羽川莲见', '特纳_EN', '石头_EN',
                  '里卡尔_ZH', '巴哈利_ZH', '守月铃美', '岩夫_JP', '五郎_ZH', '信使_JP', '安守实里', '艾尔海森_EN', '艾莉丝_EN', '遥香（正月）',
                  '云叔_ZH', '村田_JP', '阿兰_ZH', '埃洛伊_ZH', '掇星攫辰天君_JP', '沃特林_ZH', '齐米亚_ZH', '埃德蒙多_EN', '亚卡巴_JP',
                  '枫原景春_JP', '温迪_EN', '瑞安维尔_EN', '斯薇塔_EN', '七叶寂照秘密主_JP', '凝光_ZH', '明曦_ZH', '昆钧_ZH', '梁沐_JP',
                  '科玫_EN', '阮•梅_EN', '迪希雅_EN', '长野原龙之介_EN', '鳄渊明里', '捕头_ZH', '迪卢克_JP', '茂才公_JP', '日富美（泳装）',
                  '德沃沙克_JP', '海芭夏_EN', '迪奥娜_EN', '可可利亚_ZH', '荒谷_ZH', '迪肯_EN', '埃德_ZH', '莺儿_JP', '寒腿叔叔_ZH', '德田_ZH',
                  '讨嫌的小孩_JP', '九条镰治_EN', '凯瑟琳_EN', '枫原万叶_ZH', '迪希雅_JP', '知更鸟_JP', '九条裟罗_JP', '伊草遥香', '安东尼娜_ZH',
                  '今谷香里_EN', '康纳_ZH', '巴达维_JP', '阿伟_JP', '雅各_ZH', '艾伦_ZH', '佩拉_EN', '星际和平播报_EN', '刀疤刘_EN',
                  '稻城萤美_ZH', '畅畅_EN', '木南杏奈_JP', '星际和平播报_ZH', '波提欧_ZH', '悠策_ZH', '里卡尔_JP', '凯瑟琳_ZH', '霄翰_JP',
                  '会场广播_EN', '贝努瓦_ZH', '瑶瑶_ZH', '玛格丽特_ZH', '男声_ZH', '洛伦佐_EN', '库塞拉的信件_JP', '嘉玛_EN', '安西_ZH',
                  '艾迪恩_ZH', '托克_EN', '阿贝多_JP', '青镞_EN', '葵_JP', '莱昂_ZH', '爱德琳_EN', '男声_EN', '克拉拉_EN', '姬子_EN',
                  '夏沃蕾_JP', '五郎_JP', '查尔斯_EN', '德拉萝诗_JP', '炒冷饭机器人_JP', '雕像_EN', '漱玉_EN', '净砚_JP', '寒鸦_JP',
                  '玻瑞亚斯_EN', '黑田_JP', '阿伟_ZH', '加福尔_ZH', '林尼_JP', '警长_EN', '奥列格_ZH', '古山_EN', '有乐斋_JP', '刻晴_ZH',
                  '居勒什_EN', '波洛_JP', '戈尔代_JP', '伊织（泳装）', '荧_EN', '阿斯法德_ZH', '阿扎木_JP', '信使_EN', '绍祖_JP', '恕筠_ZH',
                  '彦卿_ZH', '幻胧_JP', '阿夫辛_JP', '黄泉_EN', '炒冷饭机器人_EN', '罗伊斯_JP', '云堇_ZH', '冷漠的男性_JP', '铁尔南_ZH',
                  '西拉杰_EN', '若心_ZH', '巫女_JP', '阿娜耶_ZH', '阿金_EN', '卡莉露_JP', '蒂埃里_EN', '乾玮_JP', '女士_EN', '剑先鹤城',
                  '莱欧斯利_EN', '五郎_EN', '史瓦罗_JP', '肢体评委_JP', '巴列维_JP', '杜拉夫_JP', '嚣张的小孩_JP', '维利特_JP', '驭空_EN',
                  '恶龙_EN', '丹枢_ZH', '纯也_EN', '麦希尔_ZH', '菲约尔_EN', '雪衣_EN', '迪尔菲_ZH', '奥列格_EN', '阿巴图伊_JP', '侯章_EN',
                  '云堇_JP', '一平_JP', '阿拉夫_ZH', '伊庭_ZH', '塞萨尔的日记_EN', '久岐忍_JP', '浮游风蕈兽·元素生命_JP', '瓦乐瑞娜_JP', '古田_JP',
                  '神智昏乱的云骑_JP', '龙二_EN', '迪肯_ZH', '巨大谜钟_JP', '旅行者_EN', '拍卖师_ZH', '近卫南', '德沃沙克_ZH', '村田_EN',
                  '艾伯特_ZH', '言笑_ZH', '伯恩哈德_EN', '佩拉_ZH', '查宝_JP', '云叔_JP', '丹恒_EN', '寒腿叔叔_JP', '砂狼白子', '镜中人_JP',
                  '流萤_JP', '迈勒斯_JP', '长野原龙之介_JP', '砂糖_JP', '阿兰_JP', '北村_EN', '亚卡巴_EN', '赛诺_EN', '素裳_EN', '垃垃撕圾_EN',
                  '槌永日和', '三田_JP', '史瓦罗_ZH', '埃德_JP', '吴船长_JP', '翡翠_EN', '鬼婆婆_JP', '罗刹_ZH', '莱依拉_ZH', '蒂玛乌斯_JP',
                  '手岛_JP', '枫原景春_EN', '不破莲华', '捕头_JP', '娜维娅_ZH', '狼哥_JP', '玲可_EN', '派蒙_JP', '雪衣_ZH', '李丁_ZH',
                  '奥空绫音', '迈蒙_JP', '梓（泳装）', '夏沃蕾_ZH', '八重神子_EN', '梅里埃_EN', '乾玮_EN', '舒伯特_JP', '连烟_EN', '塞德娜_EN',
                  '嘉玛_ZH', '绘星_JP', '寒腿叔叔_EN', '界种科科员_ZH', '火宫千夏', '珠函_ZH', '望雅_ZH', '安静的宾客_EN', '信使_ZH',
                  '记忆中的声音_EN', '黑天鹅_EN', '美游（泳装）', '香菱_EN', '连烟_JP', '奥兹_ZH', '魈_EN', '宵宫_EN', '宁禄_EN', '法伊兹_ZH',
                  '稻城萤美_EN', '蒂玛乌斯_EN', '刻晴_JP', '忠诚的侍从_JP', '琴_EN', '姬木梅露', '龙二_JP', '一平_EN', '海妮耶_EN', '艾尔海森_ZH',
                  '连烟_ZH', '药王秘传魁首_JP', '白术_ZH', '小川_EN', '凯亚_JP', '驭空_JP', '玛达赫_JP', '甘雨_ZH', '阿来_JP', '怀疑的患者_ZH',
                  '库塞拉的信件_EN', '阿圆_ZH', '黑崎小雪', '塞塔蕾_EN', '旁白_JP', '驭空_ZH', '大慈树王_EN', '闲云_JP', '泽田_ZH', '纳西妲_ZH',
                  '邓恩_ZH', '白子（骑行）', '银狼_ZH', '海妮耶_ZH', '玛格丽特_JP', '法伊兹_JP', '掇星攫辰天君_ZH', '巴尔塔萨_EN', '悦_JP',
                  '法拉娜_JP', '帕姆_JP', '丰见小鸟', '望雅_EN', '艾洛迪_EN', '老戴_ZH', '朱城瑠美', '空_EN', '浣溪_ZH', '杰洛尼_EN',
                  '维尔德_JP', '笼钓瓶一心_JP', '虎克_ZH', '哲平_EN', '烟绯_ZH', '伦纳德_ZH', '可莉_EN', '艾洛迪_ZH', '九条孝行_EN',
                  '佳代子（正月）', '景元_JP', '天叔_ZH', '池仓玛丽娜', '宏达_ZH', '向导_JP', '迪卢克_EN', '正人_JP', '洛恩_JP', '阿尔卡米_ZH',
                  '悦_ZH', '伦纳德_EN', '科尔特_JP', '贝努瓦_JP', '老戴_EN', '玛达赫_EN', '千织_JP', '沙坎_EN', '卡莉露_ZH',
                  '浮游水蕈兽·元素生命_ZH', '瓦尔特_EN', '阿往_EN', '明星日鞠', '托马_JP', '莎拉_JP', '独孤朔_EN', '芙卡洛斯_ZH', '尤利安_JP',
                  '艾琳_ZH', '苍森美弥', '卡卡瓦夏_ZH', '若心_EN', '安东尼娜_JP', '柚岛夏', '卡西迪_ZH', '闲云_EN', '叶德_ZH', '符玄_ZH',
                  '拍卖师_JP', '迪奥娜_JP', '绿芙蓉_JP', '泽田_JP', '西拉杰_JP', '尤利安_ZH', '卡西迪_JP', '纯也_JP', '艾琳_EN', '白老先生_ZH',
                  '星稀_JP', '回声海螺_EN', '夏洛蒂_JP', '多莉_JP', '老芬奇_JP', '阿兰_EN', '阿圆_EN', '丹恒•饮月_JP', '托帕_EN', '飞鸟马时',
                  '赛诺_JP', '雅各_EN', '拍卖会工作人员_ZH', '库斯图_ZH', '大肉丸_JP', '松浦_JP', '伊德里西_EN', '科尔特_EN', '帕斯卡_JP',
                  '理水叠山真君_ZH', '斯科特_EN', '留云借风真君_EN', '阿娜耶_EN', '深渊使徒_ZH', '斯嘉莉_ZH', '冥火大公_ZH', '西衍先生_ZH', '卓也_EN',
                  '爱德华医生_EN', '李丁_JP', '钟表小子_ZH', '卓也_ZH', '阿扎尔_ZH', '流浪者_EN', '传次郎_EN', '尤苏波夫_ZH', '春原心奈',
                  '威严的男子_EN', '孟迪尔_JP', '帕维耶_JP', '鲁哈维_EN', '艾薇拉_ZH', '狼哥_EN', '阿佩普_JP', '托帕_JP', '石头_ZH', '赛诺_ZH',
                  '马洛尼_EN', '埃洛伊_JP', '卡卡瓦夏的姐姐_JP', '龙二_ZH', '星际和平播报_JP', '星_EN', '萨赫哈蒂_JP', '米卡_JP', '苍老的声音_EN',
                  '埃尔欣根_EN', '阿蕾奇诺_JP', '商人_JP', '米沙_ZH', '塞琉斯_ZH', '魔女N_EN', '将司_JP', '贾拉康_ZH', '鹫见芹奈', '杜拉夫_EN',
                  '尚博迪克_JP', '巴蒂斯特_ZH', '星期日_ZH', '丹羽_ZH', '芹奈（圣诞）', '神里绫华_JP', '今谷香里_ZH', '公主_JP', '黄泉_JP',
                  '优香（体操服）', '戴因斯雷布_JP', '埃尔欣根_JP', '光之_ZH', '春原瞬', '丽莎_EN', '阿贝多_ZH', '淮安_EN', '玻瑞亚斯_JP', '副警长_EN',
                  '守护者的意志_ZH', '莱斯格_JP', '砂金_EN', '木村_ZH', '独眼小僧_EN', '三月七_ZH', '稻城萤美_JP', '银枝_EN', '伊利亚斯_ZH',
                  '伊迪娅_ZH', 'asideb_ZH', '欧菲妮_JP', '尾巴_EN', '艾文_JP', '乌维_ZH', '真理医生_JP', '卡萝蕾_ZH', '昆钧_EN',
                  '阿山婆_EN', '丹枢_JP', '会场广播_ZH', '乔瓦尼_EN', '坎蒂丝_JP', '八重神子_JP', '维多克_JP', '福尔茨_JP', '春日椿', '巴沙尔_JP',
                  '艾莉丝_JP', '佐西摩斯_EN', '银杏_EN', '莱提西娅_EN', '老克_JP', '杏山和纱', '卡莉露_EN', '某人的声音_JP', '舒伯特_EN',
                  '阿洛瓦_EN', '静子（泳装）', '伊丝黛莱_EN', '德拉萝诗_ZH', '黑天鹅_ZH', '吉莲_ZH', '严苛评委_EN', '丹吉尔_JP', '科林斯_JP',
                  '姬子_JP', '筑梦师_JP', '老章_EN', '智树_JP', '理查_ZH', '大毫_ZH', '真理医生_EN', '吉莲_JP', '素裳_ZH', '白露_ZH',
                  '昆恩_EN', '梦主_ZH', '凝光_EN', '霞泽美游', '阿巴图伊_EN', '塞琉斯_JP', '往昔的回声_EN', '帕帕克_JP', '查尔斯_JP', '萍姥姥_JP',
                  '知更鸟_EN', '佩尔西科夫_JP', '贡达法_EN', '杰娜姬_EN', '荧_ZH', '维利特_ZH', '浮游水蕈兽·元素生命_EN', '李丁_EN', '枣伊吕波',
                  '劳伦斯_EN', '伊庭_EN', '迈勒斯_EN', '八重神子_ZH', '幻胧_EN', '冷漠的男性_EN', '纪香_JP', '巫女_ZH', '留云借风真君_JP',
                  '岩明_JP', '年幼的孩子_ZH', '枫原万叶_EN', '仲正一花', '流浪者_ZH', '多莉_ZH', '珠函_JP', '光之_EN', '百闻_EN', '黑塔_EN',
                  '景元_EN', '知易_EN', '佐西摩斯_ZH', '梦茗_JP', '枫香（正月）', '拍卖师_EN', '谢赫祖拜尔_EN', '黑塔_JP', '紫月季_JP', '耕一_JP',
                  '海芭夏_JP', '露子_EN', '怀疑的患者_JP', '虎克_JP', '阿来_EN', '纳比尔_JP', '伊丝黛莱_JP', '帕斯卡_ZH', '公输师傅_EN',
                  '青雀_JP', '手岛_ZH', '德田_JP', '申鹤_JP', '黑塔_ZH', '真_EN', '阿汉格尔_JP', '有原则的猎犬家系成员_JP', '卡萝蕾_JP',
                  '费索勒_JP', '阿娜耶_JP', '田铁嘴_EN', '年幼的孩子_EN', '黑见芹香', '岚姐_ZH', '阿祇_JP', '小鸟游星野', '埃尔欣根_ZH', '塔里克_ZH',
                  '克列门特_ZH', '魔女N_ZH', '弗洛朗_EN', '阿金_JP', '克洛琳德_JP', '伊莎朵_EN', '宛烟_JP', '胡桃_EN', '唐娜_EN', '静山真白',
                  '艾琳_JP', '乌维_JP', '纳西妲_JP', '珊瑚宫心海_EN', '平山_ZH', '温和的声音_EN', '松浦_EN', '米凯_EN', '菲尔汀_JP', '娜比雅_EN',
                  '金人会长_JP', '查宝_EN', '螺丝咕姆_ZH', '斯坦利_ZH', '博士_EN', '琴_ZH', '黑泽京之介_EN', '沃特林_EN', '西瓦尼_EN', '艾文_EN',
                  '岚姐_EN', '半夏_JP', '加藤洋平_JP', '克洛琳德_EN', '小川_ZH', '和香（温泉）', '托帕_ZH', '博来_JP', '库塞拉_EN', '沙扎曼_EN',
                  '维多克_ZH', '巫女_EN', '台词评委_EN', '娜比雅_JP', '舒蕾_JP', '早柚_ZH', '爱德琳_ZH', '娜维娅_EN', '露尔薇_ZH', '多莉_EN',
                  '芙卡洛斯_JP', '查宝_ZH', '勇美枫', '阿幸_ZH', '冒失的帕拉德_ZH', '鹿野院平藏_EN', '深渊法师_EN', '长门幸子_ZH', '费斯曼_ZH',
                  '斯万_EN', '狐坂若藻', '卡芙卡_EN', '天真的少年_JP', '雪衣_JP', '天童爱丽丝', '克拉拉_JP', '知易_ZH', '空_JP', '雷泽_ZH',
                  '金忽律_JP', '巴蒂斯特_JP', '舍利夫_JP', '九条镰治_JP', '诺艾尔_ZH', '寒鸦_EN', '嘉明_ZH', '石头_JP', '今谷三郎_EN',
                  '霄老大_JP', '叶德_EN', '莉莉安_JP', '娜塔莎_ZH', '克雷薇_JP', '螺丝咕姆_EN', '菲尔戈黛特_ZH', '怀疑的患者_EN', '桂乃芬_EN',
                  '莱依拉_EN', '韵宁_JP', '卡卡瓦夏的姐姐_ZH', '尾巴_JP', '乙花堇', '艾丽_JP', '塞德娜_JP', '燕翠_ZH', '西尔弗_ZH', '阿扎木_ZH',
                  '埃斯蒙德_ZH', '鲁哈维_JP', '德拉萝诗_EN', '自称渊上之物_JP', '霍夫曼_JP', '木村_JP', '德沃沙克_EN', '洛伦佐_ZH', '知更鸟_ZH',
                  '彦卿_EN', '铁尔南_EN', '妮露_EN', '迪奥娜_ZH', '阿晃_EN', '今谷佳祐_EN', '大肉丸_EN', '珊瑚宫心海_JP', '昌虎_EN', '立本_JP',
                  '一心传名刀_EN', '剑阵中的声音_ZH', '钟表匠_EN', '天目十五_ZH', '巨大谜钟_ZH', '左然', '温和的声音_JP', '阿晃_ZH', '焦躁的丹鼎司医士_JP',
                  '久利须_ZH', '玛乔丽_EN', '沙寅_ZH', '泽田_EN', '尾巴_ZH', '丹恒_JP', '回声海螺_JP', '晴霓_JP', '公主_ZH', '早濑优香',
                  '穹_EN', '冷漠的男性_ZH', '神里绫人_ZH', '雷电将军_JP', '米卡_ZH', '食蜂操祈', '小涂真纪', '阿夫辛_ZH', '小仓澪_JP', '高善_EN',
                  '埃舍尔_EN', '塞德娜_ZH', '阿鸠_EN', '朋义_ZH', '白术_JP', '夜兰_EN', '银枝_JP', '叶卡捷琳娜_JP', '艾丽_EN', '科拉莉_ZH',
                  '考特里亚_EN', '警觉的流浪者_JP', '费迪南德_EN', '斯嘉莉_JP', '桐藤渚', '帮派老大_ZH', '云堇_EN', '村田_ZH', '杰克_ZH',
                  '阿利娅_JP', '希露瓦_EN', '古山_ZH', '桑博_ZH', '七七_ZH', '夏沃蕾_EN', '弗洛朗_ZH', '克列门特_JP', '科拉莉_JP', '夏妮_JP',
                  '江蓠_JP', '那维莱特_JP', '安武_JP', '加萨尼_ZH', '绍祖_EN', '维尔德_ZH', '居勒什_ZH', '韵宁_ZH', '阿幸_JP', '葵_EN',
                  '商华_JP', '金人会长_ZH', '琳妮特_ZH', '阿丰_JP', '美甘尼禄', '莱昂_EN', '魈_ZH', '莱斯格_EN', '翡翠_ZH', '佐西摩斯_JP',
                  '贾拉康_EN', '科林斯_EN', '七叶寂照秘密主_ZH', '独孤朔_JP', '邓恩_EN', '浮烟_EN', '尤苏波夫_EN', '侍从丙_ZH', '古田_ZH',
                  '绿芙蓉_ZH', '佐城巴', '提纳里_ZH', '舒伯特_ZH', '芙萝拉_ZH', '有乐斋_ZH', '芷巧_JP', '莫弈', '知易_JP', '阿鸠_ZH',
                  '长野原龙之介_ZH', '居勒什_JP', '理水叠山真君_JP', '流萤_ZH', '早柚_EN', '乔瓦尼_JP', '久田泉奈', '琳琅_ZH', '铜花瞬', '广大_ZH',
                  '菲尔戈黛特_JP', '浮烟_JP', '晴霓_EN', '半夏_ZH', '圣园未花', '河童_JP', '林尼_EN', '式大将_EN', '维尔芒_JP', '睦月（正月）',
                  '博易_JP', '七尾_EN', '卢卡_EN', '卓也_JP', '小乐_EN', '今谷佳祐_ZH', '晴霓_ZH', '札齐_JP', '杰帕德_EN', 'asideb_JP',
                  '博易_EN', '柚子（女仆）', '纪芳_JP', '九条裟罗_EN', '停云_ZH', '漱玉_ZH', '信博_EN', '叶卡捷琳娜_EN', '莱斯格_ZH',
                  '祖莉亚·德斯特雷_EN', '平山_EN', '竺子_JP', '康纳_JP', '塔里克_JP', '伊德里西_ZH', '一心传名刀_JP', '朔次郎_ZH', '哈伦_JP',
                  '小野寺_EN', '传次郎_JP', '江蓠_ZH', '中务桐乃', '薇尔_JP', '一心传名刀_ZH', '尤苏波夫_JP', '冥火大公_JP', '独眼小僧_ZH',
                  '基娅拉_ZH', '朝比奈菲娜', '歌蒂_EN', '朱里厄_EN', '迈勒斯_ZH', '阿旭_ZH', '嘉玛_JP', '长门幸子_JP', '纯水精灵_EN', '望雅_JP',
                  '北斗_EN', '纳菲斯_ZH', '严苛评委_JP', '沙寅_JP', '阿洛瓦_JP', '诺尔伯特_JP', '辛焱_ZH', '乐平波琳_ZH', '芙宁娜_EN', '尾刃康娜',
                  '米沙_JP', '娜维娅_JP', '守护者的意志_EN', '克雷薇_EN', '贡达法_ZH', '可可利亚_JP', '维格尔_JP', '钟离_JP', '杰洛尼_ZH',
                  '芙萝拉_EN', '克列门特_EN', '柊慎介_JP', '加藤洋平_EN', '自称渊上之物_ZH', '削月筑阳真君_EN', '引导员_ZH', '轰大叔_JP', '远黛_ZH',
                  '娜德瓦_JP', '西瓦尼_JP', '风仓萌绘', '连河切里诺', '宛烟_EN', '广大_EN', '班尼特_JP', '花角玉将_ZH', '诗筠_ZH', '迈蒙_ZH',
                  '剑阵中的声音_JP', '考特里亚_ZH', '艾薇拉_JP', '加萨尼_JP', '白老先生_JP', '鬼怒川霞', '珐露珊_JP', '安柏_EN', '冒失的帕拉德_EN',
                  '牛牧朱莉', '和元泉艾米', '合欢垣吹雪', '特纳_ZH', '卡芙卡_JP', '帕梅拉_EN', '奇怪的云骑_EN', '远黛_JP', '镜中人_EN', '耕一_EN',
                  '阮•梅_JP', '基娅拉_EN', '玛吉_EN', '松浦_ZH', '桂乃芬_JP', '哈伦_EN', '老孟_EN', '鹿野奈奈_ZH', '费索勒_EN', '爱清枫香',
                  '纯水精灵_ZH', '雕像_JP', '玥辉_ZH', '暮夜剧团团长_ZH', '刀疤刘_JP', '上杉_EN', '奇怪的云骑_ZH', '花角玉将_JP', '羽生田千鹤_ZH',
                  '薇尔_EN', '歌原（应援团）', '优菈_JP', '凯亚_EN', '莫娜_EN', '莱欧斯利_JP', '法哈德_ZH', '德田_EN', '瓦尔特_ZH', '巴列维_EN',
                  '巴蒂斯特_EN', '旁白_EN', '杰克_EN', '桑博_JP', '艾米绮_EN', '劳维克_EN', '舒翁_EN', '奥列格_JP', '理水叠山真君_EN',
                  '钟表小子_EN', '柯莱_ZH', '千织_ZH', '薇若妮卡_JP', '博易_ZH', '娜德瓦_EN', '卡西迪_EN', '阿拉夫_JP', '星野（泳装）', '卡波特_JP',
                  '申鹤_EN', '小仓澪_EN', '爱贝尔_JP', '加拉赫_EN', '镜中人_ZH', '流浪者_JP', '托克_JP', '女声_JP', '嘉良_ZH', '葛瑞丝_EN',
                  '斯薇塔_JP', '拉齐_EN', '格莉莎_JP', '葛瑞丝_ZH', '药王秘传魁首_EN', '冥火大公_EN', '明日奈（兔女郎）', '猫塚响', '穹_JP', '手岛_EN',
                  '深渊使徒_JP', '伽吠毗陀_ZH', '巴哈利_JP', '罗巧_JP', '穹_ZH', '帮派老大_EN', '造物翻译官_ZH', '珠函_EN', '独眼小僧_JP',
                  '嘉良_EN', '忠诚的侍从_EN', '韦尔纳_EN', '沙寅_EN', '岩明_EN', 'shajinma_JP', '鲁哈维_ZH', '麦希尔_EN', '莎塔娜_JP',
                  '老芬奇_EN', '刃_JP', '醉醺醺的宾客_ZH', '久利须_JP', '克罗索_JP', '伊莎朵_JP', '女士_JP', '年幼的孩子_JP', '虎克_EN',
                  '杰帕德_ZH', '爱德琳_JP', '克罗索_ZH', '伊德里西_JP', '维尔德_EN', '早柚_JP', '艾洛迪_JP', '记忆中的声音_JP', '明曦_EN', '千鸟满',
                  '阿诺德_JP', '钟离_EN', '朱特_JP', '百识_ZH', '露尔薇_JP', '阿山婆_ZH', '垃垃撕圾_JP', '霄老大_ZH', '米沙_EN', '十六夜野宫',
                  '菲米尼_JP', '皮特_EN', '加福尔_EN', '阿尔卡米_JP', '卡卡瓦夏_JP', '瑶瑶_EN', '齐米亚_EN', '欧菲妮_EN', '绘星_ZH', '珊瑚_JP',
                  '燕翠_JP', '阿诺德_EN', '朋义_JP', '辛克尔_ZH', '马洛尼_JP', '麦希尔_JP', '嚣张的小孩_EN', '布洛妮娅_JP', '哲平_ZH',
                  '独孤朔_ZH', '阿拉夫_EN', '小贩_EN', '拍卖会工作人员_EN', '阿斯法德_EN', '彦卿_JP', '理查_EN', '尼禄（兔女郎）', '空崎日奈',
                  '霄翰_ZH', '米凯_JP', '薇娜_JP', '提纳里_JP', '黑泽京之介_JP', '阿芬迪_EN', '劳伦斯_JP', '引导员_EN', '阿晃_JP', '轰大叔_EN',
                  '商华_EN', '萨齐因_JP', '克罗索_EN', '班尼特_EN', '钟离_ZH', '莱提西娅_ZH', '桑上果穗', '花凛（兔女郎）', '帕姆_ZH', '达达利亚_ZH',
                  '阿芬迪_JP', '梁沐_ZH', '藿藿_ZH', '小贩_ZH', '苍老的声音_ZH', '帕梅拉_JP', '台词评委_JP', '韦尔纳_JP', '科拉莉_EN', '嘉明_JP',
                  '希露瓦_JP', '星_JP', '百识_EN', '奇怪的云骑_JP', '浣溪_EN', '梁沐_EN', '恶龙_JP', '珊瑚_ZH', '赛索斯_ZH', '胡桃_JP',
                  '千世（泳装）', '刃_EN', '托马_EN', '白子（泳装）', '浦和花子', '下江小春', '魈_JP', '托克_ZH', '杰克_JP', '刻薄的小孩_EN',
                  '元太_JP', '泉奈（泳装）', '男声_JP', '芷巧_ZH', '阿灼_JP', '式大将_JP', '谢赫祖拜尔_JP', '管家奥斯威尔_JP', '智树_EN',
                  '佩尔西科夫_ZH', '伊萨克_JP', '卢卡_ZH', '隐书_JP', '丽莎_JP', '费斯曼_JP', '高善_ZH', '上杉_ZH', '丹恒•饮月_ZH', '淮安_ZH',
                  '生盐诺亚', '佩尔西科夫_EN', '黑田_EN', '奥泰巴_JP', '纳西妲_EN', '悦_EN', '萨姆_JP', '莫娜_JP', '阿旭_EN', '符玄_JP',
                  '阿灼_EN', '云叔_EN', '净砚_ZH', '费斯曼_EN', '泽维尔_JP', '柯莱_JP', '芙宁娜_JP', '荧_JP', '迪尔菲_JP', '福尔茨_EN',
                  '荒谷_JP', '乐平波琳_JP', '今谷三郎_ZH', '鹿野奈奈_JP', '爱德华医生_JP', '斯嘉莉_EN', '优菈_EN', '常九爷_ZH', '洛伦佐_JP',
                  '大毫_JP', '瑞安维尔_ZH', '申鹤_ZH', '神里绫人_EN', '玛格丽特_EN', '竺子_EN', '可莉_JP', '雷电将军_EN', '艾迪恩_EN',
                  '华劳斯_EN', '丝柯克_ZH', '希儿_JP', '百闻_ZH', '会场广播_JP', '舒蕾_EN', '掇星攫辰天君_EN', '香菱_JP', '尤利安_EN', '黛比_EN',
                  '平山_JP', '大和田_EN', '嘉良_JP', '发抖的流浪者_ZH', '迪卢克_ZH', '女声_ZH', '花火_JP', '阿雩_ZH', '玲可_JP', '斯科特_JP',
                  '安东尼娜_EN', '奇妙的船_JP', '罗伊斯_ZH', '纯也_ZH', '远黛_EN', '向导_EN', '木村_EN', '陆行岩本真蕈·元素生命_ZH', '拉伊德_JP',
                  '玛塞勒_ZH', '忠诚的侍从_ZH', '帮派老大_JP', '接笏_JP', '洛恩_ZH', '菜菜子_JP', '向导_ZH', '楚仪_EN', '警长_ZH', '库斯图_EN',
                  '绮珊_JP', '艾伦_JP', '削月筑阳真君_ZH', '沙坎_JP', '玛塞勒_EN', '言笑_EN', '姬子_ZH', '纯水精灵_JP', '玛吉_ZH',
                  '菲尔戈黛特_EN', '泽维尔_ZH', '浣溪_JP', '安柏_ZH', '伊迪娅_EN', '自称渊上之物_EN', '岚姐_JP', '沙扎曼_JP', '猎犬家系成员_JP',
                  '羽生田千鹤_EN', '大野月咏', '爱丽丝（女仆）']
async def translate(text,mode="ZH_CN2JA"):
    try:
        URL=f"https://api.pearktrue.cn/api/translate/?text={text}&type={mode}"
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(URL)
            #print(r.json()["data"]["translate"])
            return r.json()["data"]["translate"]
    except:
        print("文本翻译接口1失效")
        if mode!="ZH_CN2JA":
            return text
    try:
        url=f"https://findmyip.net/api/translate.php?text={text}&target_lang=ja"
        r=requests.get(url=url,timeout=10)
        return r.json()["data"]["translate_result"]
    except:
        print("翻译接口2调用失败")
    try:
        url=f"https://translate.appworlds.cn?text={text}&from=zh-CN&to=ja"
        r = requests.get(url=url, timeout=10,verify=False)
        return r.json()["data"]
    except:
        print("翻译接口3调用失败")
    return text
class TTS:
    def __init__(self, Cookie):
        self.headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.modelscope.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Cookie": Cookie}
    def listSpeakers(self):
        return ["BT","塔菲","阿梓","otto","丁真","星瞳","东雪莲","嘉然","孙笑川","亚托克斯","文静","鹿鸣","奶绿","七海","恬豆","科比"],fireflySpeaker
    async def tts(self,text="",speaker="阿梓",path="./tts.wav",autoTranslate=True):
        if speaker in ["BT","塔菲","阿梓","otto","丁真","星瞳","东雪莲","嘉然","孙笑川","亚托克斯","文静","鹿鸣","奶绿","七海","恬豆","科比"]:
            if text == "" or text == " ":
                text = "哼哼"
            if speaker == "阿梓":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azusa-Bert-VITS2-2.3/gradio/file="
            elif speaker == "otto":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/otto-Bert-VITS2-2.3/gradio/file="
            elif speaker == "塔菲":
                speaker = "taffy"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Taffy-Bert-VITS2/gradio/file="
            elif speaker == "星瞳":
                speaker = "XingTong"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/XingTong-Bert-VITS2/gradio/file="
            elif speaker == "丁真":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/DZ-Bert-VITS2-2.3/gradio/file="
            elif speaker == "东雪莲":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Azuma-Bert-VITS2-2.3/gradio/file="
            elif speaker == "嘉然":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Diana-Bert-VITS2-2.3/gradio/file="
            elif speaker == "孙笑川":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/SXC-Bert-VITS2/gradio/file="
            elif speaker == "鹿鸣":
                speaker = "Lumi"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Lumi-Bert-VITS2/gradio/file="
            elif speaker == "文静":
                speaker = "Wenjing"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Wenjing-Bert-VITS2/gradio/file="
            elif speaker == "亚托克斯":
                speaker = "Aatrox"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Aatrox-Bert-VITS2/gradio/file="
            elif speaker == "奶绿":
                speaker = "明前奶绿"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/LAPLACE-Bert-VITS2-2.3/gradio/file="
            elif speaker == "七海":
                speaker = "Nana7mi"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Nana7mi-Bert-VITS2/gradio/file="
            elif speaker == "恬豆":
                speaker = "Bekki"
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Bekki-Bert-VITS2/gradio/file="
            elif speaker == "科比":
                url = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/run/predict"
                newurp = "https://www.modelscope.cn/api/v1/studio/xzjosh/Kobe-Bert-VITS2-2.3/gradio/file="
            data = {
                "data": [text, speaker, 0.5, 0.5, 0.9, 1, "auto", None, "Happy", "Text prompt", "", 0.7],
                "event_data": None,
                "fn_index": 0,
                "dataType": ["textbox", "dropdown", "slider", "slider", "slider", "slider", "dropdown", "audio", "textbox",
                             "radio", "textbox", "slider"],
                "session_hash": "xxosa6k69g"
            }

            headers = self.headers

            #print(p)

            #headers="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
            async with httpx.AsyncClient(timeout=200,headers=headers) as client:
                r = await client.post(url, json=data)
                newurl = newurp + r.json().get("data")[1].get("name")

                async with httpx.AsyncClient(timeout=200,headers=headers) as client:
                    r = await client.get(newurl)
                    with open(path, "wb") as f:
                        f.write(r.content)
                    return path
        elif speaker in fireflySpeaker:
            if speaker.endswith("_ZH"):
                pass
            else:
                if autoTranslate:
                    text = await translate(text)
            # os.system("where python")
            # p = random_str() + ".mp3"
            # p = "data/voices/" + p
            p = path
            uri = "wss://fs.firefly.matce.cn/queue/join"
            session_hash = "1fki0r8hg8mj"

            async with websockets.connect(uri) as ws:
                # 连接后发送的第一次请求
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                await ws.send(json.dumps(
                    {"data": [speaker], "event_data": None, "fn_index": 1, session_hash: "1fki0r8hg8mj"}))
                while True:
                    message = await ws.recv()
                    print("Received '%s'" % message)
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        ibn = data["output"]["data"][0]
                        exampletext = data["output"]["data"][1]
                        break
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                await ws.send(
                    json.dumps({"data": [ibn], "event_data": None, "fn_index": 2, "session_hash": "1fki0r8hg8mj"}))
                while True:
                    message = await ws.recv()
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        for item in data["output"]["data"]:
                            if item and "name" in item and "/tmp/gradio/" in item["name"]:
                                # 提取文件的路径
                                example = item["name"]
                                # print(f"这里是请求结果：{example}")
                                break
                        break
            async with websockets.connect(uri) as ws:
                await ws.send(json.dumps({"fn_index": 4, "session_hash": session_hash}))
                # 连接后发送的第二次请求
                await ws.send(json.dumps({"data": [text, True, {"name": f"{example}",
                                                                "data": f"https://fs.firefly.matce.cn/file={example}",
                                                                "is_file": True, "orig_name": "audio.wav"},
                                                   exampletext, 0, 90, 0.7, 1.5, 0.7, speaker],
                                          "event_data": None, "fn_index": 4, "session_hash": "1fki0r8hg8mj"}))

                # 等待并处理服务器的消息
                while True:
                    message = await ws.recv()
                    print("Received '%s'" % message)
                    data = json.loads(message)
                    # 当消息中包含 'name' 并且是所需文件路径时
                    if "output" in data and "data" in data["output"]:
                        for item in data["output"]["data"]:
                            if item and "name" in item and "/tmp/gradio/" in item["name"]:
                                # 提取文件的路径
                                file_path = item["name"]
                                # 拼接 URL
                                full_url = f"https://fs.firefly.matce.cn/file={file_path}"
                                break
                        break
                async with httpx.AsyncClient(timeout=200) as client:
                    r = await client.get(full_url)
                    with open(p, "wb") as f:
                        f.write(r.content)
                    return p

