@echo off
echo Fixing Prometheus Configuration...

echo Step 1: Backing up current config
copy prometheus.yml prometheus-backup-current.yml

echo Step 2: Using minimal configuration
copy prometheus-minimal.yml prometheus.yml

echo Step 3: Stopping Prometheus
docker-compose stop prometheus
docker-compose rm -f prometheus

echo Step 4: Starting Prometheus with new config
docker-compose up -d prometheus

echo Step 5: Waiting for startup...
timeout /t 10

echo Step 6: Checking container status
docker-compose ps prometheus

echo Step 7: Showing recent logs
docker-compose logs --tail=10 prometheus

echo.
echo Testing Prometheus endpoint...
curl -s http://localhost:9090 >nul 2>&1
if %errorlevel% equ 0 (
    echo SUCCESS: Prometheus is responding!
    echo Access it at: http://localhost:9090
) else (
    echo Prometheus is still starting up or has issues
    echo Check logs with: docker-compose logs prometheus
)

pause
