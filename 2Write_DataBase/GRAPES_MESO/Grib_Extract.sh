
#当前hour,同时去除前面有0
inow_Hour=$(date --date="today" +"%H" | sed 's/\<0//g')

#2-4个小时后下载(2 5 11 14 17)其中1个起报时刻的资料 
ayBegin_hour=(2 5 11 14 17)
for bias in $(seq 2 4); do
{
  ibegin=$(($inow_Hour-$bias))
  #echo $ibegin $bias
  if [[ " ${ayBegin_hour[@]} " =~ " ${ibegin} " ]] ; then
    echo $inow_Hour, $ibegin
    sBegin_date=$(date --date="0 day" +"%Y%m%d")
    sEnd_date=$(date --date="0 day" +"%Y%m%d")
    sBegin_hour=${ibegin}
    python3 Grib_Extract.pyc  -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
  fi
}
done

#23点
aybhour=(1 2 3)
if [[ " ${aybhour[@]} " =~ " ${inow_Hour} " ]] ; then  #判断字符串是否存在于数组中
  echo $inow_Hour, 23
  sBegin_date=$(date --date="-1 day" +"%Y%m%d")
  sEnd_date=$(date --date="-1 day" +"%Y%m%d")
  sBegin_hour=23
  python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
fi

#08点
aybhour=(12 13)
if [[ " ${aybhour[@]} " =~ " ${inow_Hour} " ]] ; then
  echo $inow_Hour, 08
  sBegin_date=$(date --date="0 day" +"%Y%m%d")
  sEnd_date=$(date --date="0 day" +"%Y%m%d")
  sBegin_hour=08
  python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
fi

#20点
aybhour=(0 1)
if [[ " ${aybhour[@]} " =~ " ${inow_Hour} " ]] ; then
  echo $inow_Hour, 20
  sBegin_date=$(date --date="-1 day" +"%Y%m%d")
  sEnd_date=$(date --date="-1 day" +"%Y%m%d")
  sBegin_hour=20
  python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
fi
