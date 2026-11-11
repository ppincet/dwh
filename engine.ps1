<#
.SYNOPSIS
#>

$EnvFilePath = Join-Path $PSScriptRoot ".env"
$LogDir = Join-Path $PSScriptRoot "logs"
$LogFile = Join-Path $LogDir "etl_engine.log"
$MaxFileSizeMB = 10


function Write-EtlLog {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [ValidateSet("INFO", "WARNING", "ERROR")]
        [string]$Level = "INFO"
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
 
    Write-Host $LogEntry

    # Ротация лога при превышении лимита
    $fileLen = [long](Get-Item $LogFile).Length
    $maxBytes = [long]($MaxFileSizeMB * 1MB)
    
    Write-Host "DEBUG EXPR: fileLen($fileLen) gt maxBytes($maxBytes) = $($fileLen -gt $maxBytes)"

    if (($filelen -gt $maxbytes)) {
        Write-Host "inside rotation"
        $ArchiveName = Join-Path $LogDir "etl_engine_$(Get-Date -Format 'yyyyMMdd_HHmmss').zip"
        $TempLog = "$LogFile.tmp"
        Move-Item $LogFile $TempLog -Force
        Compress-Archive -Path $TempLog -DestinationPath $ArchiveName -Force
        Remove-Item $TempLog -Force
    }

    try {
        Write-Host "inside adding"
        Add-Content -Path $LogFile -Value $LogEntry -Encoding UTF8 -ErrorAction Stop
    } catch {
        Write-Error "Не удалось записать лог в файл: $_"
    }
}

function Load-EnvFile {
    param ([string]$Path)
    if (Test-Path $Path) {
        Get-Content $Path -Encoding UTF8 | ForEach-Object {
            $line = $_.Trim()
            if ($line -eq '' -or $line.StartsWith('#')) { return }
            if ($line.Contains('=')) {
                $parts = $line.Split('=', 2)
                $name  = $parts[0].Trim()
                $value = $parts[1].Trim().Trim('"').Trim("'")
                [Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::Process)
            }
        }
    }
}


Load-EnvFile -Path $EnvFilePath

$SmtpServer  = $env:SMTP_SRVR
$SmtpPort    = [int]$env:SMTP_PORT
$SmtpUser    = $env:SMTP_USR
$SmtpPass    = $env:SMTP_PWD

$SecurePassword = ConvertTo-SecureString $SmtpPass -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($SmtpUser, $SecurePassword)
$MailTo = 'vashkevich.pavel@santa.by'
$MailSubject = 'Tst'

Write-EtlLog -Message "Старт проверки отправки почты" -Level "INFO"

try {
    $pyOutput = .venv/bin/python3 src/etl.py daily --log-level DEBUG # 2>&1
    if ($LASTEXITCODE -ne 0) {
        $errMsg = "etl process failed: $pyOutput"
        # Write-EtlLog -Message $errMsg -Level "ERROR"    
    }
    # Send-MailMessage -SmtpServer $SmtpServer -Port $SmtpPort -Credential $Credential -UseSsl -From $SmtpUser -To $MailTo -Subject $MailSubject -Encoding ([System.Text.Encoding]::UTF8)
    # Write-EtlLog -Message "email was sent" -Level "INFO"
}
catch {
    $errMsg = "email sending failed: $_"
    Write-EtlLog -Message $errMsg -Level "ERROR"
    throw $_
}