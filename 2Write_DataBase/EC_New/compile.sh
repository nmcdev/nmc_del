Cur_Dir=$(pwd)

#系统根路径
for n in $(seq 1 10); do
{
sys_root_path=$(printf "%0.s../" $(seq 1 $(($n-1))))".."
if [ -d $sys_root_path/"lib/pylib" ];then
  break
fi
}
done

cd $sys_root_path/lib/pylib
python3 Compiling_Program.pyc $Cur_Dir


