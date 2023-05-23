# twitter-retriever
salad bar doesn't exi--

## jobs:
1. 从指定twitter用户得到关注列表
2. 从twitter handle下载所有图片
3. 根据规则筛图
4. (todo) 产生webdataset格式的streaming dataset

## use:
见ipynb文件, 或者./twitter_suite下单个文件的`__main__`函数





## One-liners

从`file.html`文件提取所有twitter handles:
```powershell
Get-Content file.html | Select-String -AllMatches '(?<=twitter\.com/)\w+' | Select-Object -ExpandProperty Matches | Select-Object -ExpandProperty Value | Out-File -Encoding utf8 handles.txt
```


