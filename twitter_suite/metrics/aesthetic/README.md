# Reference
https://github.com/christophschuhmann/improved-aesthetic-predictor

## Aesthetic server:
检查一个文件夹(以及子文件夹)里的图片, 并定期计算aesthetic score;

检查到文件夹里有新图片时会计算新图的分数, 保存到根部录下aes_score.csv里

requirements:
```
opencv-python
click
```

use: 
- 如果要使用命令行, 把`main()`上面的click decorator取消注释;
- 每隔(300)秒, 更新一次`<dir>`里的文件:
- 设置间隔时间: `-i <interval>`
```bash
python get_aesthetics.py -d <dir> 
```