#该脚本是为了删除格点实况中某些错误的文件夹

begin_date="2019-01-01"
end_date="2019-12-27"

echo "date: "$begin_date" to "$end_date

#日期循环
beg_s=`date -d "$begin_date" +%s`
end_s=`date -d "$end_date" +%s`
while [ "$beg_s" -le "$end_s" ];do
  ted=`date -d @$beg_s +"%Y%m%d"`;
  echo $ted
  #格点路径
  #spath='/data/zxq/mosrr/DataBase/Observation_site/'${ted:0:4}'/'${ted}'/Precipitation/Hour_Inst'
  #站点路径
  spath='/data/zxq/mosrr/DataBase/Observation_site/'${ted:0:4}'/Precipitation/Hour_Inst'
  #文件夹存在 删除
  if [ -d $spath ];then
    rm -rf $ted $spath
  fi
  beg_s=$((beg_s+86400)); #日期增加1天(24h=86400秒)
done


