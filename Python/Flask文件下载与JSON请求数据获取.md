---
title: Flask文件下载与JSON请求数据获取
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

## 文件与base64编码字符串的转换
以图片文件为例，将图片转换为base64编码字符串以json格式的post数据请求至服务端，文件与base64编码字符串转换方式如下：

### 文件转base64
```
def image_to_base64(filepath):
    """
    :param filepath: 文件路径
    :return:
    """
    # 转为二进制格式
    with open(filepath, "rb") as f:
        data = str(base64.b64encode(f.read()), "utf-8")
        # 转换为bytes对象
        base64_data = bytes(data, "utf-8")
        return data 
```

### base64转文件
```

# base64转换成image
def base64_to_image(filepath, data):
    """
    :param filepath: 转换后的文件路径，包含文件名
    :param data: base64字符串数据
    :return:
    """

    fh = open(filepath, "wb")
    fh.write(base64.b64decode(data))                # 转换为image文件
    fh.close()
 
 
```

## requests使用post请求发送base64文件
```

def image_to_base64(filename, path="E:\\script", **kwargs):
    """
    :param filename: image文件名
    :param path: image存放路径
    :param kwargs: 参数prefix(转换base64后需要加上的前缀)
    :return:
    """
    path = join(path, filename)
    # 转为二进制格式
    with open(path, "rb") as f:
        data = str(base64.b64encode(f.read()), "utf-8")

        # 转换为bytes对象
        base64_data = bytes(data, "utf-8")
    return data


def get_qr_code_color(img_path_1):
    url = "http://192.168.1.127:5000/qrcode/color/recognition"
    with open(img_path_1, "rb") as f:  # 转为二进制格式
        base64_img = str(base64.b64encode(f.read()), "utf-8")  # 使用base64进行加密
    data = {'file': base64_img}
    try:
        resp = requests.post(url, json.dumps(data))
    except Exception:
        return '{"code":"4004","msg":"server connection error"}'
    return resp.text
```

## flask接收base64字符串数据并转换文件
```
@app.route('/qrcode/color/recognition', methods=['POST'])
def qr_code_color_recog():
    """
    二维码颜色界定

    Returns:
            an http response with json data formatted like blow:
            {
                "code":"2001",
                "msg":"green"
            }

            code 4001 : the QR code not exists
            code 3001 : the QR code is invalidated
            code 5000 : unknown error
    """
    start_time = time.time()
    # 获取前端POST请求传过来的json数据
    data = json.loads(request.get_data(as_text=True))
    # 获取图片base64编码数据
    img_data = base64.b64decode(data['file'])
    # 图片文件临时存放位置，如不存在则创建
    img_dir = f'{current_path}/temp'
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    img_name = f'{uuid.uuid1().hex}.jpg'
    img_path = join(img_dir, img_name)

    # 转换为image
    with open(img_path, "wb") as fb:
        fb.write(img_data)
    img_write_end_time = time.time()
    print(f"图片数据保存时间 : {img_write_end_time - start_time}")
```
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。