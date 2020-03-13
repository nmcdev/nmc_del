
#当前hour,同时去除前面有0
inow_Hour=$(date --date="today" +"%H" | sed 's/\<0//g')

# for inow_Hour in $(seq 0 23); do
# {

#2-4个小时后下载(2 5 11 14 17)其中1个起报时刻的资料 
ayBegin_hour=(2 14)
for sBegin_hour in ${ayBegin_hour[@]}; do
{
  ((bias=$inow_Hour-$sBegin_hour))
  if [[ 0 -le $bias ]] && [[ $bias -le 6 ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias
    sBegin_date=$(date --date="0 day" +"%Y%m%d")
    sEnd_date=$(date --date="0 day" +"%Y%m%d")
    python3 Grib_Extract.pyc  -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
  else
    if [[ $bias -le 0 ]]; then
      echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias"<=0"
    else
      echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias">=6"
    fi
  fi
}
done

#08点
sBegin_hour=8
((bias=$inow_Hour-$sBegin_hour))
if [[ 3 -le $bias ]] && [[ $bias -le 6 ]]; then
  sBegin_date=$(date --date="0 day" +"%Y%m%d")
  sEnd_date=$(date --date="0 day" +"%Y%m%d")
  python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
else
  if [[ $bias -lt 0 ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias"<=0"
  elif [[ 0 -le $bias ]] && [[ $bias -lt 3  ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias"<3"
  elif [[ $bias -gt 6 ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias">6"
  fi
fi

#20点
sBegin_hour=20
((bias=$inow_Hour-$sBegin_hour))
if [[ $bias -lt 0 ]];then
 ((bias=$bias+24))
fi
if [[ 3 -le $bias ]] && [[ $bias -le 6 ]]; then
  sBegin_date=$(date --date="-1 day" +"%Y%m%d")
  sEnd_date=$(date --date="-1 day" +"%Y%m%d")
  #python3 Grib_Extract.pyc -bd $sBegin_date -ed $sEnd_date -bh $sBegin_hour
else
  if [[ $bias -lt 0 ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias"<=0"
  elif [[ 0 -le $bias ]] && [[ $bias -lt 3  ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias"<3"
  elif [[ $bias -gt 6 ]]; then
    echo "Begin_hour:"$sBegin_hour, "Now_time:"$inow_Hour, "bias:"$bias">6"
  fi
fi

# for inow_Hour in $(seq 0 23); do
# {
# }
# done