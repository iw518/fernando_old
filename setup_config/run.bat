::����activate.bat�к���:end��䣬�ʽ��������index.pyִ�������뵽activate.bat��
@Echo Off

color 2e
Title ����
:begin
cls
Echo ��ѡ����Ҫ�Ĳ���
Echo     1 ������վ
Echo     2 ���Ի���
Echo     3 �˳�

Set current_dir=e:\pythonweb\py344
Pushd %current_dir%

Set /P Choice= ������������ѡ��Ҫ���еĲ������� ��Ȼ�󰴻س���
If not "%Choice%"=="" (
  If "%Choice%"=="1" Scripts\activate_flask.bat
  If "%Choice%"=="2" (cmd /k "Scripts\activate_test.bat"
)
  If "%Choice%"=="3" EXIT
)
pause>nul
goto :begin