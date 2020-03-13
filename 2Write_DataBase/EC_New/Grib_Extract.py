# -*- coding: gb18030 -*-

import os
import sys
import math
import getopt
import pygrib
import datetime
import numpy as np
from multiprocessing  import Pool, cpu_count

for i in range(1,3):
  sRoot_Path = os.path.join(*[".."]*i)
  lib_path=os.path.join(sRoot_Path,"lib","pylib")
  #print(os.path.abspath(lib_path))
  if os.path.exists(lib_path):break
sys.path.append(lib_path)

import Module_Arguments            as MArg
import Module_MyFunction           as MMyfun
import Module_Model_Info           as MModel
import Module_Global_Path          as MGP
import Module_2Write_DataBase      as M2WD


#主程序
if __name__=='__main__':

  #当前工作路径
  sCurrent_Path=os.getcwd()
  
  #cpu核数 
  in_cpu_core = cpu_count()-1
  
  #根据文件夹确定参数
  ltwork=sCurrent_Path.split(os.sep)
  # 模式名 区域
  sModel_name,sRegion=ltwork[-1].split("_")

  #实例化
  cls_myfun = MMyfun.Class_MyFunction(0)
  cls_model = MModel.ModelInfo()
  cls_gp    = MGP.Class_Global_Path()
  cls_s2wd  = M2WD.Class_EC_2Write_DataBase(0)
  #获取参数
  cls_arg   = MArg.Class_Arguments(step="S2")
  args      = cls_arg.dArgs(dspt=__file__)

  #全局路径
  cls_gp.dRead_Global_Path_ini(sRoot_Path)
  
  #模式信息
  sIn_Abs_path = os.path.join(sRoot_Path, "Parameter", sModel_name, "_".join([sModel_name,sRegion,"Info.ini"]))
  cls_model.ParseIni(sIn_Abs_path)

  #输入路径
  if args.in_path is None:
    args.in_path = os.path.join(cls_gp.sResult_Main_Path,"1DownLoad_Data")
  
  #输入输出路径检查
  if args.out_path is not None:
    if args.in_path.strip()==args.out_path.strip():
      print("Error:"+args.in_path.strip()+" == "+args.out_path.strip())
      sys.exit()

  
  #切割格点区域
  if args.grid_name is None:
    ltArea = [cls_model.latlon_info.lat_start, cls_model.latlon_info.lat_end, 
              cls_model.latlon_info.lon_start, cls_model.latlon_info.lon_end]
  else:
    sIn_Abs_path = os.path.join(sRoot_Path, "Parameter", sModel_name, args.grid_name)
    latlon_info=cls_model.dGridini(sIn_Abs_path)
    ltArea = [latlon_info.lat_start, latlon_info.lat_end, latlon_info.lon_start, latlon_info.lon_end] #(南北西东)

  #找出预报时效
  ndy_fhours=np.array(cls_model.ltforecast_hours)
  mask=np.logical_and(args.begin_fhour<=ndy_fhours,ndy_fhours<=args.end_fhour)
  ltforecast_hours=ndy_fhours[mask].tolist()

  #时间函数(BJ)
  ltdates = cls_myfun.ddates_between_two_date(args.begin_date, args.end_date, 0)
  iN_day = len(ltdates)

  #最小线程数
  iN_Process  = np.min([len(ltforecast_hours),in_cpu_core]) 
  print("processes:",iN_Process)
  
  #日期循环
  for idy, seach_date in enumerate(ltdates):
    print(idy,":","_".join([seach_date,args.sbegin_hour]))
    #(北京时间)
    sBegin_Date_BJ = seach_date+args.sbegin_hour
    #(世界时间)
    sBegin_Date_UTC = cls_myfun.dBJT_to_UTC(sBegin_Date_BJ[0:4], sBegin_Date_BJ[4:6],\
                                            sBegin_Date_BJ[6:8], args.sbegin_hour)
    iyear_bj,  imonth_bj,  iday_bj, ihour_bj   = cls_myfun.ddate_hour_split_1(sBegin_Date_BJ)
    iyear_utc, imonth_utc, iday_utc, ihour_utc = cls_myfun.ddate_hour_split_1(sBegin_Date_UTC)
    #预报时效
    ltcycle=[]
    for ifrst_hour in ltforecast_hours:
      #print(idy,":","_".join([seach_date,args.sbegin_hour,"_%03d"%ifrst_hour]))
      #(世界时间)
      sForecast_Date_UTC = cls_myfun.dBefAftDate(iyear_utc, imonth_utc, iday_utc, ihour_utc,"Hour",ifrst_hour)
      #输入文件名                                        
      sIn_file_name = sBegin_Date_UTC+"_"+"%03d"%ifrst_hour+"_C1D"+sBegin_Date_UTC[4:10] +"00"+ sForecast_Date_UTC[4:10] + "001"
      #输入文件绝对路径
      sIn_Abs_Path = os.path.join(args.in_path,sModel_name+"_"+sRegion, sBegin_Date_BJ[0:4],
                                  sBegin_Date_BJ[0:8]+"_"+args.sbegin_hour, sIn_file_name)
      #输出文件绝对路径
      if args.out_path==None:
        sDB_Main_Path = cls_model.GetDisk(seach_date)
      else:
        if args.out_path.strip()=="":
          sDB_Main_Path = cls_model.GetDisk(seach_date)
        else:
          sDB_Main_Path = args.out_path
      sOut_Sub_Path = os.path.join(sDB_Main_Path, sModel_name+"_"+sRegion, sBegin_Date_BJ[0:4],
                                   sBegin_Date_BJ[0:8]+"_"+args.sbegin_hour)
      if os.path.exists(sIn_Abs_Path) and (not os.path.exists(sOut_Sub_Path)):os.makedirs(sOut_Sub_Path)
      sOut_Abs_Path = os.path.join(sOut_Sub_Path,sIn_file_name)
      # print(sIn_Abs_Path)
      # print(sOut_Abs_Path)
      #增加0时刻01分的预报场
      if ifrst_hour==0:
        sIn_file_name1 = sIn_file_name[:-2]+"11"
        #输入文件绝对路径
        sIn_Abs_Path1 = os.path.join(args.in_path,sModel_name+"_"+sRegion, sBegin_Date_BJ[0:4],
                                    sBegin_Date_BJ[0:8]+"_"+args.sbegin_hour, sIn_file_name1)
        sOut_Abs_Path1 = os.path.join(sOut_Sub_Path,sIn_file_name1)
        #检查输出文件大小判断是否更新
        if os.path.exists(sOut_Abs_Path1):
          fsize = os.path.getsize(sOut_Abs_Path1)
          #删除错误文件
          if fsize<=1.0:
            try:
              os.remove(sOut_Abs_Path1)
            except OSError as e:
              print("Failed with:", e.strerror)
              print("Error code:", e.code)
        if not os.path.exists(sOut_Abs_Path1):
          ltcycle.append([sIn_Abs_Path1,sOut_Abs_Path1,ltArea,args.no_delete])
      #检查输出文件大小判断是否更新
      if os.path.exists(sOut_Abs_Path):
        fsize = os.path.getsize(sOut_Abs_Path)
        #删除错误文件
        if fsize<=1.0:
          try:
            os.remove(sOut_Abs_Path)
          except OSError as e:
            print("Failed with:", e.strerror)
            print("Error code:", e.code)
        else:
          if args.update==0: continue #存在&0就不用更新
      ltcycle.append([sIn_Abs_Path,sOut_Abs_Path,ltArea,args.no_delete])
      # #获取原始数据大小
      # if os.path.exists(sIn_Abs_Path): 
        # fRaw_size,sRaw_unit=cls_myfun.dGet_FileSize(sIn_Abs_Path)
      #数据提取
      # cls_s2wd.dS2_Extract(sIn_Abs_Path,sOut_Abs_Path,ltArea,args.no_delete)
      # #获取新数据大小
      # if os.path.exists(sOut_Abs_Path): 
        # fNew_size,sNew_unit=cls_myfun.dGet_FileSize(sOut_Abs_Path)
      # if os.path.exists(sIn_Abs_Path) and os.path.exists(sOut_Abs_Path):
        # print(fRaw_size,sRaw_unit,"==>",fNew_size,sNew_unit)
    #多个时次并行
    pool = Pool(processes = iN_Process)
    pool_result = pool.map(cls_s2wd.dmulti_Extract, ltcycle)
    pool.close()
    pool.join()

  #程序运行结束时间
  cls_myfun.dPrint_run_time()
  
