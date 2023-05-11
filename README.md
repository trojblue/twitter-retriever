# twitter-retriever
salad bar doesn't exi--

瞎写的, 用来:
1. 从指定twitter用户得到关注列表



## TXT

[illustration2023](https://illustration.media/about): `bin/twitter-artists-illust2023.txt`

[100人展season13](https://www.eshi100.com/season13/index.html#Artist): `bin/twitter-artists-100nin2023.txt`



## One-liners

从`file.html`文件提取所有twitter handles:
```powershell
Get-Content file.html | Select-String -AllMatches '(?<=twitter\.com/)\w+' | Select-Object -ExpandProperty Matches | Select-Object -ExpandProperty Value | Out-File -Encoding utf8 handles.txt
```


