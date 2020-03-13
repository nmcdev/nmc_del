


#nohup /vdisk2/zxq/GMOSRR/2Write_DataBase/Obs_Grid/Obs_Rain_Accu_recall.sh >> /vdisk2/zxq/GMOSRR/2Write_DataBase/Obs_Grid/log.txt 2>&1 &
#ps -ef | grep "Obs_Rain_Accu_recall.sh"


current_path=$(cd "$(dirname "$0")"; pwd)
cd $current_path

./compile.sh

sBegin_date="20191101"  #$(date -d "1 days ago" +%Y%m%d)
sEnd_date="20200131"    #$(date -d "0 days ago" +%Y%m%d)
iupdate=0


# py=/vdisk2/zxq/Program_files/python3.6/bin/python3
python3 Obs_Rain_Accu.py  -u $iupdate -bd $sBegin_date -ed $sEnd_date







