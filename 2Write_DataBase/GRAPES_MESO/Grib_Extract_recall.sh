
./compile.sh

iupdate=0
sBegin_date=20200105  #$(date --date="today" +"%Y%m%d")
sEnd_date=20200109    #$(date --date="today" +"%Y%m%d")
sBegin_FTime=0
sEnd_FTime=33
# sIn_Main_Path="/u01/zxq/GMOSRR_Result/1DownLoad_Data/"
# sOut_Main_Path="/vdisk2/zxq/DataBase2/"
#-iph $sIn_Main_Path  -oph $sOut_Main_Path

ayBegin_hour=(2 5 8 11 14 17 20)
for sBegin_hour in ${ayBegin_hour[@]}; do
{
  echo $sBegin_date $sEnd_date $sBegin_hour $sBegin_FTime $sEnd_FTime
  python3 Grib_Extract.pyc -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime
}
done


                        