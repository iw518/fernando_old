::由于activate.bat中含有:end语句，故将最后启动index.py执行语句加入到activate.bat中
@Echo Off

color 2e
Title 命令
:begin
cls
Echo 请选择需要的操作
Echo     1 运行网站
Echo     2 测试环境
Echo     3 退出

Set current_dir=e:\pythonweb\py344
Pushd %current_dir%

Set /P Choice= 　　　　　请选择要进行的操作数字 ，然后按回车：
If not "%Choice%"=="" (
  If "%Choice%"=="1" Scripts\activate_flask.bat
  If "%Choice%"=="2" (cmd /k "Scripts\activate_test.bat"
)
  If "%Choice%"=="3" EXIT
)
pause>nul
goto :begin