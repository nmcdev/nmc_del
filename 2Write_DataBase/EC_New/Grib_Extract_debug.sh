
./compile.sh

iupdate=0
sBegin_date=20190309  #$(date --date="today" +"%Y%m%d")
sEnd_date=20190309    #$(date --date="today" +"%Y%m%d")
sBegin_FTime=204
sEnd_FTime=204
# sIn_Main_Path="/vdisk2/zxq/DataBase/"
# sOut_Main_Path="/vdisk2/zxq/DataBase_xj/"

# sBegin_hour=08
# python3 Grib_Extract.pyc -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime

sBegin_hour=20
python3 Grib_Extract.pyc -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime 

