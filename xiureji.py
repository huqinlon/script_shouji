# 目标网址：https://www.xiurenb.com

# 导入库
import time, os, requests
from lxml import etree
from urllib import parse

# 定义请求头

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'
	}

# 格式化列表
img_list = []
url_list = []
page_list = []

# 编码输入数据
human_unencode = input('Enter the human_name:')
human_encode = parse.quote(human_unencode)

# 编码后索引url
url_human = 'https://www.xiurenb.com/plus/search/index.asp?keyword=' + str(human_encode) + '&searchtype=title'

# 获取指定人物写真集列表页数
res_first = requests.get(url=url_human, headers=headers)
tree_first = etree.HTML(res_first.text)
Num_first = len(tree_first.xpath('/html/body/div[3]/div[1]/div/div/ul/div[3]/div/div[2]/a'))
print(f'Page_total:{Num_first}')

# 获取指定页数的每个写真集的url并写入列表
i = input('Enter the PageNumber:')
print(f'Getting the page-{i}...')
res_human = requests.get(url_human + '&p=' + str(i))
tree_human = etree.HTML(res_human.text)
jihe_human = tree_human.xpath('/html/body/div[3]/div[1]/div/div/ul/div[3]/div/div[1]/div/div[1]/h2/a/@href')
for page in jihe_human:
    page_list.append(page)
time.sleep(2)

# 获取每个写真集的全部图片
for Page_Num in page_list:
	url = 'https://www.xiurenb.com' + str(Page_Num)
	Num_res = requests.get(url=url, headers=headers)
	Num_tree = etree.HTML(Num_res.text)
	Num = len(Num_tree.xpath('/html/body/div[3]/div/div/div[4]/div/div/a'))
	url_list.append(url)
	for i in range(1, int(Num) - 2):
		url_other = url[:-5] + '_' + str(i) +'.html'
		url_list.append(url_other)
	# 获取所有图片url
	for url_img in url_list:
		res = requests.get(url=url_img, headers=headers)
		tree = etree.HTML(res.text)
		img_src = tree.xpath('/html/body/div[3]/div/div/div[5]/p/img/@src')
		for img in img_src:
			img_list.append(img)
		time.sleep(0.5)
	# 创建保存目录
	res = requests.get(url=url_list[0], headers=headers)
	res.encoding = 'utf-8'
	tree = etree.HTML(res.text)
	path_name = tree.xpath('/html/body/div[3]/div/div/div[1]/h1//text()')[0][11:]
	print(path_name)
	if not os.path.exists(f'C:/Users/liu/Pictures/{human_unencode}'):
		os.mkdir(f'C:/Users/liu/Pictures/{human_unencode}')
	the_path_name = f'C:/Users/liu/Pictures/{human_unencode}/' + path_name
	if not os.path.exists(the_path_name):
		os.mkdir(the_path_name)
		# 保存图片数据
		num = 0
		for j in img_list:
			img_url = 'https://www.xiurenb.com' + j
			img_data = requests.get(url=img_url, headers=headers).content
			img_name = img_url.split('/')[-1]
			finish_num = str(num) + '/' + str(len(img_list))
			with open(f'C:/Users/liu/Pictures/{human_unencode}/' + path_name + '/' + img_name, 'wb') as f:
				print(f'Downloading the img:{img_name}/{finish_num}')
				f.write(img_data)
				f.close()
			num += 1
			time.sleep(0.5)
		# 再次格式化列表
		img_list = []
		url_list = []
	else:
		print('gone>>>')
		# 再次格式化列表
		img_list = []
		url_list = []

# 输出结束提示
print('Finished!')
