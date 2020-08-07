pyinstaller.exe -i resources\\app.ico --name x-boardConfigurator --distpath bin main.py
xcopy resources bin\resources\ /E /H /K
xcopy configs bin\configs\ /E /H /K
rmdir build /s /q
del x-boardConfigurator.spec

