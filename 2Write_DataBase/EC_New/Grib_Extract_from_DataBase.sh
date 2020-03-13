
./compile.sh

iupdate=0
sBegin_date=20190220  #$(date --date="today" +"%Y%m%d")
sEnd_date=$(date --date="today" +"%Y%m%d")
sBegin_FTime=000
sEnd_FTime=240

sBegin_hour=08
python3 Grib_Extract_from_DataBase.pyc -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime

sBegin_hour=20
python3 Grib_Extract_from_DataBase.pyc -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime 

