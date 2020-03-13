# -*- coding: gb18030 -*-

import os
import sys
import math
import warnings
warnings.simplefilter(action='ignore', category=(FutureWarning,RuntimeWarning))
import pygrib
import datetime
import numpy as np
from multiprocessing  import Pool, cpu_count

for i in range(1,10):
  sRoot_Path = os.path.join(*[".."]*i)
  lib_path=os.path.join(sRoot_Path,"lib","pylib")
  if os.path.exists(lib_path):
    break
sys.path.append(lib_path)

import Module_MyFunction           as MMyfun
import Module_Arguments            as MArg
import Module_Global_Variable      as MGV
import Module_Global_Path          as MGP
import Module_2Write_DataBase      as M2WD
import Module_Obs_DataBase         as MObsDB


#主程序
if __name__=='__main__':

  #获取参数
  cls_arg = MArg.Class_Arguments(step="S2_Obs")
  args=cls_arg.dArgs(dspt=__file__)

  #当前工作路径
  sCurrent_Path=os.getcwd()
  #根据文件夹确定参数
  ltwork=sCurrent_Path.split(os.sep)

  #cpu核数 
  in_cpu_core = cpu_count()-1
  
  #实例化
  cls_myfun = MMyfun.Class_MyFunction()
  cls_gv    = MGV.Class_Global_Variable(iDebug=0)
  cls_gp    = MGP.Class_Global_Path()
  cls_s2wd  = M2WD.Class_EC_2Write_DataBase()
  cls_obsdb = MObsDB.Class_Obs_DataBase()

  #全局路径
  cls_gp.dRead_Global_Path_ini(sRoot_Path)
  
  #格点实况数据库参数
  cls_obsdb.dRObs_Grid_ini(sRoot_Path, cls_gv.sObs_Grid_file)
  
  #切割格点区域
  if args.grid_name is None:
    sOut_main_path = cls_obsdb.sObs_Main_Path
    sIn_main_path = os.path.join(cls_gp.sResult_Main_Path,cls_gv.S1_dir,ltwork[-1])
  else:
    sIn_main_path = cls_obsdb.sObs_Main_Path
    cls_obsdb.dRObs_Grid_ini(".", args.grid_name,lrd_head=False)
    sOut_main_path = os.path.join(cls_gp.sResult_Main_Path, ltwork[-2], ltwork[-1])
  #区域
  ltArea = [cls_obsdb.latlon_info.lat_start, cls_obsdb.latlon_info.lat_end, 
            cls_obsdb.latlon_info.lon_start, cls_obsdb.latlon_info.lon_end] #(南北西东)
    
  #输入输出路径检查 
  if sIn_main_path.strip()==sOut_main_path.strip():
    print("Error:"+sIn_main_path.strip()+" == "+sOut_main_path.strip())
    sys.exit()
  
  #时间函数(BJ)
  ltdates = cls_myfun.ddates_between_two_date(args.begin_date, args.end_date, args.if_period)
  iN_day = len(ltdates)
  
  #日期循环
  for idy, sdate in enumerate(ltdates):
    #实况变量循环
    ltcycle=[]
    for sObs_name in args.obs_info:
      for sObs_type in args.obs_info[sObs_name]:
        sObs_type_lower=sObs_type.lower()
        seach_date = sdate
        #时效
        if sObs_type_lower=="hour_inst":                                   #逐时瞬时量
          sobs_fname=cls_obsdb.dobs_file_name(0, args.begin_hour, args.end_hour, sday_hour=sObs_type_lower[0:4], suffix=".GRB2")
          print(sObs_name+"_"+sObs_type, str(idy)+":"+seach_date+" "+args.sbegin_hour+"_"+args.send_hour)
        elif sObs_type_lower in ["hour_01accu","hour_min","hour_max"]:     #逐时累积量或最大最小
          if args.end_hour==0:
            ibegin_hour=23
            iend_hour=24
            seach_date=(datetime.datetime.strptime(sdate,'%Y%m%d')-datetime.timedelta(days=1)).strftime('%Y%m%d')
          else:
            iend_hour=args.end_hour
            ibegin_hour=iend_hour-1
          sobs_fname=cls_obsdb.dobs_file_name(0, ibegin_hour, iend_hour, sday_hour="span", suffix=".GRB2")
          print(sObs_name+"_"+sObs_type, str(idy)+":"+seach_date+" "+f"{ibegin_hour:02d}"+"_"+f"{iend_hour:02d}")
        elif (sObs_type_lower=="day_max" or sObs_type_lower=="day_min"):   #逐日
          #风没有日最小
          if sObs_type_lower in ["day_min"] and sObs_name.lower()=="wind": continue
          #根据起报时间获取
          if args.begin_hour<8 or args.begin_hour>=20 :
            sobs_fname=cls_obsdb.dobs_file_name(20, 0, 24, sday_hour=sObs_type_lower[0:3], suffix=".GRB2")
            print(sObs_name+"_"+sObs_type, str(idy)+":"+seach_date+" "+"20_20")
          elif 8<=args.begin_hour and args.begin_hour<20:
            sobs_fname=cls_obsdb.dobs_file_name(8, 0, 24, sday_hour=sObs_type_lower[0:3], suffix=".GRB2")
            print(sObs_name+"_"+sObs_type, str(idy)+":"+seach_date+" "+"08_08")
          else:
            continue
        #输入文件绝对路径
        sIn_sub_path  = os.path.join(sIn_main_path, seach_date[0:4], seach_date, sObs_name, sObs_type)
        sIn_abs_path  = os.path.join(sIn_sub_path, sobs_fname)
        #输出文件绝对路径
        sOut_sub_path  = os.path.join(sOut_main_path, seach_date[0:4], seach_date, sObs_name, sObs_type)
        if os.path.exists(sIn_abs_path) and (not os.path.exists(sOut_sub_path)):os.makedirs(sOut_sub_path)
        sOut_abs_path = os.path.join(sOut_sub_path,sobs_fname)
        if os.path.exists(sOut_abs_path):
          fsize = os.path.getsize(sOut_abs_path)  #获取新数据大小(bytes)
          #删除错误文件
          if fsize<=1.0:
            try:
              os.remove(sOut_abs_path)
            except OSError as e:
              print("Failed with:", e.strerror)
              print("Error code:", e.code)
          else:
            if args.update==0: continue #存在&0就不用更新
        if sObs_name.lower()=="visibility":
          cls_obsdb.dObs_Grid_Extract(sIn_abs_path, sOut_abs_path, ltArea, ldel_raw=args.no_delete, changeDecimalPrecision=3)
        else:
          cls_obsdb.dObs_Grid_Extract(sIn_abs_path, sOut_abs_path, ltArea, ldel_raw=args.no_delete)
          
    # ltcycle.append([sIn_abs_path,sOut_abs_path,ltArea,False])
    # #多个要素并行
    # pool = Pool(processes = iN_Process)
    # pool_result = pool.map(cls_s2wd.dmulti_Extract, ltcycle)
    # pool.close()
    # pool.join()

  #程序运行结束时间
  cls_myfun.dPrint_run_time()
  
