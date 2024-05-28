# -*- coding: utf-8 -*-
"""Copy of PaliGemma.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xBmU7VNDRXPjhctFiBHqimA446I0i6qe

# 🔥🔥🔥本项目代码由AI超元域频道制作，观看更多大模型微调视频请访问我的频道⬇
# 👉👉👉[我的哔哩哔哩频道](https://space.bilibili.com/3493277319825652)
# 👉👉👉[我的YouTube频道](https://www.youtube.com/@AIsuperdomain)

# 使用 🤗 transformers 来运行 PaliGemma 模型

PaliGemma 是 Google 发布的新型视觉语言模型。在这个笔记
中，我们将演示如何使用 🤗 transformers 进行 PaliGemma 的推理。
首先，由于我们需要使用最新版本的 🤗 transformers 及其他相关库，所以请使用更新标志来安装以下库。
"""

# !pip install -q -U accelerate bitsandbytes git+https://github.com/huggingface/transformers.git

import torch
import numpy as np
from PIL import Image
import requests

input_text = "What color is the flower that bee is standing on?"
input_text = "花上面是什么动物"
img_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/bee.JPG?download=true"
input_image = Image.open(requests.get(img_url, stream=True).raw)

"""[link text](https://)图片如下所示。

![](https://github.com/win4r/AISuperDomain/assets/42172631/7ded8001-ae5f-464d-bef0-dbda2eb5ed16)

你可以像下面这样加载 PaliGemma 模型和处理器。

1.   列表项
2.   列表项
"""

from transformers import AutoTokenizer, PaliGemmaForConditionalGeneration, PaliGemmaProcessor
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_id = "leo009/paligemma-3b-mix-224"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16)
processor = PaliGemmaProcessor.from_pretrained(model_id)

"""处理器会同时预处理图像和文本，因此我们将传递它们。

---

"""

inputs = processor(text=input_text, images=input_image,
                  padding="longest", do_convert_rgb=True, return_tensors="pt").to("cuda")
model.to(device)
inputs = inputs.to(dtype=model.dtype)

"""我们可以传入我们预处理过的输入。

> 添加引用块

"""

with torch.no_grad():
  output = model.generate(**inputs, max_length=496)

print(processor.decode(output[0], skip_special_tokens=True))

"""[link text](https://)## 以4比特加载模型

你还可以以4比特和8比特加载模型，在推理过程中可以节省内存。
首先，初始化 `BitsAndBytesConfig`。

"""

# from transformers import BitsAndBytesConfig
# import torch
# nf4_config = BitsAndBytesConfig(
#    load_in_4bit=True,
#    bnb_4bit_quant_type="nf4",
#    bnb_4bit_use_double_quant=True,
#    bnb_4bit_compute_dtype=torch.bfloat16
# )

# """:现在我们将重新加载模型，但将上述对象作为 `quantization_config` 传入。

# """

# from transformers import AutoTokenizer, PaliGemmaForConditionalGeneration, PaliGemmaProcessor
# import torch

# device="cuda"
# model_id = "leo009/paligemma-3b-mix-224"
# model = PaliGemmaForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.bfloat16,
#                                                           quantization_config=nf4_config, device_map={"":0})
# processor = PaliGemmaProcessor.from_pretrained(model_id)

# with torch.no_grad():
#   output = model.generate(**inputs, max_length=496)

# print(processor.decode(output[0], skip_special_tokens=True))

# """# 🔥🔥🔥本项目代码由AI超元域频道制作，观看更多大模型微调视频请访问我的频道⬇
# # 👉👉👉[我的哔哩哔哩频道](https://space.bilibili.com/3493277319825652)
# # 👉👉👉[我的YouTube频道](https://www.youtube.com/@AIsuperdomain)
# """