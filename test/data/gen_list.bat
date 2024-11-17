rem Generate a list of function calls for each content.xml file

set _genfile=update_all.bat
del %_genfile%
for /F "tokens=*" %%l in ('dir content.xml /s /b') do echo update.py "%%l" >> %_genfile%
popd
