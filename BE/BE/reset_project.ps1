# ================================
# Django Project Initialization Script (Windows PowerShell)
# ================================

Write-Host "⚙ Deleting database file..."
Remove-Item -Path "..\db.sqlite3" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".\db.sqlite3" -Force -ErrorAction SilentlyContinue

Write-Host "⚙ Deleting migration files..."
Get-ChildItem -Recurse -Include *.py -Path *\migrations\* |
Where-Object { $_.Name -ne "__init__.py" } |
Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✅ Migrations cleaned"

Write-Host "`n⚙ Creating new migrations..."
python manage.py makemigrations

Write-Host "`n⚙ Applying migrations to database..."
python manage.py migrate

# Write-Host "`n🚀 Creating superuser"
# python manage.py createsuperuser

# Write-Host "`n🎉 All operations completed successfully! You can now use the fresh database."
