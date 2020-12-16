@echo off
:loop
echo.
set /p "part=Which part do you want to run? (1-4)"
if %part%==1 (
	cd Part1
	echo Running Part 1:
	echo.
	python game.py
	cd ..
) else (
if %part% EQU 2 (
	cd Part2
	echo Running Part 2:
	echo.
	python impostors.py
	cd ..
) else (
if %part% EQU 3 (
	cd Part3
	echo Running Part 3:
	echo.
	python pathfinding.py
	cd ..
) else (
if %part% EQU 4 (
	cd Part4
	echo Running Part 4:
	echo.
	python shortest_path.py
	cd ..
))))
goto loop