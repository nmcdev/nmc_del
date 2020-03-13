
./compile.sh

iupdate=0
sBegin_date=20200201  #$(date --date="today" +"%Y%m%d")
sEnd_date=20200309    #$(date --date="today" +"%Y%m%d")
ayBegin_hour=(2 08 14 20)      #bj时(02 08 14 20)
sBegin_FTime=3
sEnd_FTime=36
threads=6
# sIn_Main_Path="/u01/zxq/GMOSRR_Result/1DownLoad_Data/"
# sOut_Main_Path="/vdisk2/zxq/DataBase2/"
#-iph $sIn_Main_Path  -oph $sOut_Main_Path


for sBegin_hour in ${ayBegin_hour[@]}; do
{
  echo $sBegin_date $sEnd_date $sBegin_hour $sBegin_FTime $sEnd_FTime
  python3 Grib_Extract.pyc -u $iupdate -thr $threads -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime
}
done

