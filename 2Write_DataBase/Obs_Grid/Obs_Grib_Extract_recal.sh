#后台运行
#nohup /vdisk2/zxq/GMOSRR/2Write_DataBase/Obs_Grid/Obs_Grib_Extract_recal.sh >> /vdisk2/zxq/GMOSRR/2Write_DataBase/Obs_Grid/log.txt 2>&1 &

#自定义区域文件
#sfile_name="Obs_Grid.ini"
#-gn $sfile_name

#起报日期(北京时间)
ayBegin_hour=(01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24)
iupdate=0

#设定起始-结束日期(北京时间)
if [ $# == 2 ]; then
  begin_date=$1
  end_date=$2
else
  #自定义"格式为2017-04-04"
  begin_date="2019-11-01"
  end_date="2020-02-28"
fi
echo "date: "$begin_date" to "$end_date

#日期循环
beg_s=`date -d "$begin_date" +%s`
end_s=`date -d "$end_date" +%s`
while [ "$beg_s" -le "$end_s" ];do
  ted=`date -d @$beg_s +"%Y%m%d"`;
  #起报时循环
  for bh in ${ayBegin_hour[@]}; do
  {
    echo $ted,$bh
    python3 Obs_Grib_Extract.pyc -u $iupdate -ndel -bd $ted -ed $ted -bh $bh -eh $bh
  }
  done
  beg_s=$((beg_s+86400)); #日期增加1天(24h=86400秒)
done


