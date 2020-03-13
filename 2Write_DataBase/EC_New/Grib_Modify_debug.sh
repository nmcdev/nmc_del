
./compile.sh

iupdate=0
sBegin_date=20160101  #$(date --date="today" +"%Y%m%d")
sEnd_date=201600101    #$(date --date="today" +"%Y%m%d")
sBegin_FTime=000
sEnd_FTime=000
sIn_Main_Path="/vdisk2/zxq/DataBase/"
sOut_Main_Path="/vdisk2/zxq/DataBase/"

sBegin_hour=08
python3 Grib_Modify.py -ndel -u $iupdate -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour -bfh $sBegin_FTime -efh $sEnd_FTime \
                       -iph $sIn_Main_Path  -oph $sOut_Main_Path