# -*- coding: utf-8 -*-

'''
    WSDetector v1.0
    Author: Frank
    Email: fr4nk404@gmail.com
'''

from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from upload.model_test import predict_rnn
from upload.model_test import load_one_flle
from upload.model_test import format_size
from upload.model_test import get_md5

import hashlib
import sys
import os
#import numpy as np
import tflearn
from tflearn.data_utils import to_categorical, pad_sequences
# Create your views here.
class DisplayView(View):
    """登录验证"""
    # get方式获取index页面
    def get(self, request):
         
        return render(request, 'index.html', {})
     
    # 用户提交表单，返回主页
    def post(self, request):
        """提交表单"""
        #请求方法为post时，进行处理
        if request.method =="POST":
            #获取上传的文件，如果没有文件，默认为none
            File=request.FILES.get("myfile",None)
            if File is None:
                #return HttpResponse("no files for upload")
                return render(request, 'index.html', {})
            else:
                #打开特定的文件进行二进制的写操作
                filename='%s%s'%(settings.MEDIA_ROOT,File.name)
                print(filename)
                with open(filename,'wb+') as f:
                    #分块写入文件
                    for chunk in File.chunks():
                        f.write(chunk)
                
                #模型预测
                str1=predict_rnn(load_one_flle(filename))

                #返回结果
                print(filename)
                upfilname=File.name
                print(upfilname)
                #返回大小
                size = os.path.getsize(filename)
                upfilsize=format_size(size)
                print(upfilsize)
                #返回md5
                upfilmd5= get_md5(filename)
                print(upfilmd5)
                
                return render(request, 'result.html', {"filname":upfilname,"filsize":upfilsize,"filmd5":upfilmd5,"resu":str1})
        else:
            return render(request,'index.html',{})
