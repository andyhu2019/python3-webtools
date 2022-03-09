import os,re

#获取当前目录下所有文件名及目录名
def pri_all_file(dir):
    names = os.listdir(dir) 
    li = []
    extension = ['.shtml','.html','.htm'] #定义要查找的文件类型
    for name in names:
        full_name = os.path.join(dir,name) #拼接成完整路径
        if os.path.isdir(full_name):
            #li.append(full_name)
            li.extend(pri_all_file(full_name)) #递归遍历子目录下文件及目录，并一次性加入原列表中
        else:
            #print(full_name)
            if os.path.splitext(name)[-1] in extension: #取文件扩展名进行比较
                li.append(full_name)
    return li

#将列表中的内容一行行写入文件
def write_result_file(result):
    #行分隔符
    ls = os.linesep
    #结果日志文件名
    filename = "result.txt" #相对路径,文件在.py文件所在的目录中
    try:
        fobj = open(filename,'w')
    except IOError as e:
        print("*** file open error:",e)
    else:
        fobj.writelines('%s%s' % (txt,ls) for txt in result)
        fobj.close()

#仅当本python模块直接执行时，才执行如下语句，若被别的python模块引入，则不执行
if __name__ == "__main__":
    dir_name = '/wwwroot' #定义要查找的文件夹
    keyword = ['张三' ,'李四'] #定义要查找的关键词
    findfilelist = [] #找到的文件列表
    filelist = pri_all_file(dir_name)
    for filepath in filelist:
        f = open(filepath, encoding='utf-8')
        try:
            t = f.read()
        except:
            f = open(filepath, encoding='gbk', errors='ignore')
            t = f.read()
        f.close()
        pattern = re.compile('<body[\s\S]*?</body>', re.IGNORECASE) #定义一个取出body内容的正则表达式，忽略大小写
        result = pattern.findall(t)  #进行匹配，找到所有满足条件的
        content = "".join(result) #列表转化为字符串
        if len(content) != 0:
            for k in keyword: #循环关键词
                if content.find(k) != -1:
                    print('\r[%s] %s' % (k,filepath))
                    findfilelist.append('['+k + '] ' + filepath) #找到则输出文件地址
                    # if os.path.isfile(filepath): #判断是否是为文件（文件是否存在）
                    #     os.rename(filepath, filepath + '_bak') #修改文件名
        
        print('\r%s' % (filepath), end = '')
    
    write_result_file(findfilelist) #将查找结果写入result.txt文件中

