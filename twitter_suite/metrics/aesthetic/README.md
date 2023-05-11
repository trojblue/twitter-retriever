# Reference
https://github.com/christophschuhmann/improved-aesthetic-predictor

## Aesthetics:
检查一个文件夹(以及子文件夹)里的图片, 并计算aesthetic score;

检查到文件夹里有新图片时会计算新图的分数, 保存到根部录下metrics.csv里

requirements:
```
opencv-python
click
```

use: 
见notebook，或者复制 bin/sac%2Blogos%2Bava1-l14-linearMSE.pth到这个目录然后：
```bash
python get_aesthetics.py
```
