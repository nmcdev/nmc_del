sBegin_date=$(date --date="today" +"%Y%m%d")
sEnd_date=$(date --date="today" +"%Y%m%d")

#当前hour,同时去除前面有0
inow_Hour=$(date --date="today" +"%H" | sed 's/\<0//g') 
#0-5: 20BJ  12UTC
if [[ 0 -le $inow_Hour ]] && [[ $inow_Hour -le 5 ]]; then
  sBegin_date=$(date -d "1 days ago" +%Y%m%d)
  sEnd_date=$(date -d "1 days ago" +%Y%m%d)
  sBegin_hour=20
fi
#6-11: 2BJ  18UTC
if [[ 6 -le $inow_Hour ]] && [[ $inow_Hour -le 11 ]]; then
  sBegin_hour=2
fi
#12-17:08BJ 00UTC
if [[ 12 -le $inow_Hour ]] && [[ $inow_Hour -le 17 ]]; then
  sBegin_hour=8
fi
#18-23: 14BJ 06UTC
if [[ 18 -le $inow_Hour ]] && [[ $inow_Hour -le 23 ]]; then
  sBegin_hour=14
fi

python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour