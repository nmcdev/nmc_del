
inow_HM=$(date --date="today" +"%H")


python3 Obs_Rain_Accu.pyc

#补充前1天
if [[ $inow_HM==11 ]] | [[ $inow_HM==23 ]]; then
sBegin_date=$(date -d "1 days ago" +%Y%m%d)
sEnd_date=$(date -d "1 days ago" +%Y%m%d)
python3 Obs_Rain_Accu.pyc -bd $sBegin_date -ed $sEnd_date
fi









