@echo off
rem Final render: resumes after a power cut. Removes empty placeholder frames first.
cd /d %USERPROFILE%\blender-forest
for %%F in (render\final_2k\*.png) do if %%~zF==0 del "%%F"
"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b scene\forest.blend --python scripts\look.py --python scripts\render_final.py > render\final_render.log 2>&1
