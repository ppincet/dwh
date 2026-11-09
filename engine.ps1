<#
.SYNOPSIS
#>

$EnvFilePath = Join-Path $PSScriptRoot ".env"

function Load-EnvFile {
    param ([string]$Path)
    Get-Content $Path -Encoding UTF8 | ForEach-Object {
            $line = $_.Trim()
            if ($line -eq '' -or $line.StartsWith('#')) {
                return
            }
            if ($line.Contains('=')) {
                $parts = $line.Split('=', 2)
                $name  = $parts[0].Trim()
                $value = $parts[1].Trim().Trim('"').Trim("'")
                [Environment]::SetEnvironmentVariable($name, $value, [System.EnvironmentVariableTarget]::Process)
            }
        }
}

Load-EnvFile -Path $EnvFilePath
$SmtpServer  = $env:SMTP_SRVR
$SmtpPort    = [int]$env:SMTP_PORT
$SmtpUser    = $env:SMTP_USR
$SmtpPass    = $env:SMTP_PWD

Write-Host "smtp_srv : $SmtpServer"
Write-Host "smtp_usr : $SmtpUser"
Write-Host "smtp_pwd : $SmtpPass"

$SecurePassword = ConvertTo-SecureString $SmtpPass -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($SmtpUser, $SecurePassword)
$MailTo = $SmtpUser
$MailSubject = 'Tst'
    try {
        Send-MailMessage -SmtpServer $SmtpServer -Port $SmtpPort -Credential $Credential -UseSsl -From $SmtpUser -To $MailTo -Subject $MailSubject -Encoding ([System.Text.Encoding]::UTF8)
    }
    catch {
        Write-Error "Не удалось отправить email: $_"
    }