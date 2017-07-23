# Scripts-for-HM (Windows)
[Python][py] scripts for [HM][hevc] [run, analyze, ...]  

注：所有脚本只适用于Python 3以上  
准备工作：日志处理时需提前安装[xlwt][xls]  

[py]:https://www.python.org/downloads/
[hevc]:http://www.hevc.info/
[xls]:https://pypi.python.org/pypi/xlwt
  
## Run HM:  
用来测试HM编码器，可以一次启动所有编码程序（对应每个测试序列的每个测试点---码率点或QP点），生成对应的编码日志，码流，
以及重建yuv

## Run logs:  
用来提取编码结果，从给定日志文件夹下提取出每个日志的summary关键数据，如码率、PSNR、编码时间、以及额外自定义指标，输出到表格

## Run frame:  
用来提取某一编码日志中所有帧的结果，如每一帧的POC、帧类型、bits、PSNR，以及额外自定义指标，输出到表格


# How to run HM encoder:

下图是run HM 文件夹结构：  
![fig1]  
其中每个子文件夹的作用如下：  

**cfg**：此文件夹是对应HM工程下的配置文件夹，只需原封不动复制到此根目录下，编码中编码器配置文件，以及序列配置文件均可在此文件夹中找到，
并且在编码时不需要作任何修改  
**config**：此文件夹保存有最常用的和脚本配套的配置文件，实际编码时只需将里面的config.txt拷贝至外层根目录，并作对应修改即可，但不可重命名  
![fig2]  

**exe**：此文件夹存放要测试的编码器exe文件，建议为release版，且在本地debug测试无误  
**result**：此文件夹为编码输出结果文件夹，需提前建好。所有编码日志文件会在result\\当次编码文件目录\\logs\\子文件夹下，码流bin和重建yuv
会在result\\当次编码文件目录\\yuvbin\\子文件夹下  
**HM_cmd.py**：为编码脚本文件，所有配置准备就绪后，即可双击启动所有编码。若一次要启动的数量很多，需查看机器cpu和内存是否足够，
建议此时换用实验室配置较高的机器  


[fig1]: images/1.PNG "fig1" { width:auto; max-width:90% }
[fig2]: images/2.png "fig2" { width:auto; max-width:90% }

**下面主要讲一下如何修改 config.txt：**  

下图为config.txt内容：  
![fig3]  

**1. 参数区**  

identifier：在此行中添加此次编码的简要方法说明  
exe path：指定此次编码的编码器  
cfg1 path：指定编码器配置文件  
cfg2 path：指定序列配置文件路径  
seq path：指定源编码序列路径  
result path：指定输出结果总路径，每运行一次编码，会在该结果目录下新建自己的结果文件夹  
extra cmd：指定额外特别需要加入的编码命令，码控和QP已在脚本中包含，# 表示无  
mode：指定需要的编码模式，1：码控；0：QP

**2. 序列区**  
1. testing seq and rate: 表示开始     
2. \*\*\*end\*\*\*：表示结束  
3. 每组序列要以class: xxx开始，表示序列路径下改组序列的目录名（必须一致）  
4. 每组序列要以###表示结束  
5. 测试序列的组数，以及每组要测试的序列可任意添加   
6. 每个序列此处的序列名是该序列的全名去掉后缀所得，后跟四个码率点(kbps)或QP点  
7. 序列路径下的每个序列必须以下划线间隔的方式命名，且第一个下划线之前的部分必须与该序列的cfg目录下的序列配置名一致，
HM序列默认符合，无需更改

**注：**  
1. 此config.txt中参数区与序列区内不要无故添加空行，与图例保持一致  
2. 所有路径需要在末尾（针对目录）加上反斜杠  
3. cfg1 cfg2的路径一般取默认，无需改变  
4. 所有特定标记请勿改变  
5. 编码时，脚本会在输出目录result\\下新建当前编码子目录，相应的config.txt会自动从根目录剪切至此目录下，另外会生成一个参数解析日志，
以及一个readme.txt，可自行向此文件内添加本次编码的说明。另外，编码时会自动在此目录下生成编码日志目录logs\\以及码流目录yuvbin\\，用于
存放编码日志，码流文件以及重建yuv  

[fig3]: images/3.png "fig3" { width:auto; max-width:90%;}

# How to extract important data from logs:
下图是run logs 文件夹结构：  
![fig4]  
config.txt是配置文件  

**下面主要讲解config.txt的配置：**  

![fig5]  

logs path：指定要提取数据的日志路径  
output path：指定输出表格的路径，为空表示当前路径  
adding item：指定编码器额外添加的自定义指标，如果有多个以空格分开  
\*\*\*end\*\*\*：表示结束  

**注：**  
1. 所有路径需要在末尾（针对目录）加上反斜杠  
2. 可查看输出示例   

[fig4]: images/4.PNG "fig4" { width:auto; max-width:90% }
[fig5]: images/5.PNG "fig5" { width:auto; max-width:90% }

# How to extract data of each frame:

下图是run frame 文件夹结构：  
![fig6]  
config.txt是配置文件  

**下面主要讲解config.txt的配置：**  

![fig7]  

logs path：指定要提取数据的单个日志，一般置于该目录logs子目录下  
output path：指定输出表格的路径，为空表示当前路径  
adding item：指定编码器额外添加的自定义指标，如果有多个以空格分开  
\*\*\*end\*\*\*：表示结束  

**注：**  
1. 所有路径需要在末尾（针对目录）加上反斜杠  
2. 可查看输出示例  

[fig6]: images/6.PNG "fig5" { width:auto; max-width:90% }
[fig7]: images/7.PNG "fig7" { width:auto; max-width:90% }
