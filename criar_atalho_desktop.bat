@echo off
title Criar Atalhos do KinSync
echo Criando atalho na Area de Trabalho...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $desktop = [System.Environment]::GetFolderPath('Desktop'); $s = $ws.CreateShortcut(\"$desktop\KinSync.lnk\"); $s.TargetPath = '%~dp0KinSync.exe'; $s.WorkingDirectory = '%~dp0'; $s.IconLocation = '%~dp0kinsync.ico'; $s.Description = 'KinSync — Kin do Dia'; $s.Save(); Write-Host 'Atalho criado na Area de Trabalho com sucesso!'"
pause
