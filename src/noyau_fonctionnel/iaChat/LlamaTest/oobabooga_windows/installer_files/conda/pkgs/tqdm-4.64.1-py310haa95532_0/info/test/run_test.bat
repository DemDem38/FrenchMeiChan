



pip check
IF %ERRORLEVEL% NEQ 0 exit /B 1
tqdm --help
IF %ERRORLEVEL% NEQ 0 exit /B 1
tqdm -v
IF %ERRORLEVEL% NEQ 0 exit /B 1
pytest -k "not tests_perf and not test_pipes and not test_as_completed"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
