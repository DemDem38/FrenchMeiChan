function Install-JRE {
    # Définition des paramètres pour l'installation silencieuse
    $installerArgsJRE = "/s INSTALLDIR=`"C:\Program Files\Java\jre-1.8`""
    
    if (Test-Path -Path "C:\Program Files\Java\jre-1.8") {
        Write-Host "The JRE package already exist"
        return
    }
    # Téléchargement du fichier d'installation du JRE (remplacez l'URL par celle appropriée)
    $url = "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248242_ce59cff5c23f4e2eaf4e778a117d4c5b"
    $outputFileJRE = "$env:TEMP\jreInstaller.exe"

    Write-Host "Download JRE 1.8..."
    Invoke-WebRequest -Uri $url -OutFile $outputFileJRE

    Write-Host "JRE Installation..."
    Start-Process -FilePath $outputFileJRE -ArgumentList $installerArgsJRE -Wait

    Write-Host "Remove Installer file for JRE"
    Remove-Item -Path $outputFileJRE -Force

    # Spécifiez le chemin d'installation du JRE
    $jrehome = "C:\Program Files\Java\jre-1.8"
    # Vérifiez si la variable d'environnement existe déjà
    $existingPathJRE = [System.Environment]::GetEnvironmentVariable("JRE_HOME")
    if ($existingPathJRE -eq $jrehome) {
        Write-Host "The environment variable for the JRE already exist"
    }
    else {
        [System.Environment]::SetEnvironmentVariable("JRE_HOME", $jrehome, "Machine")
        Write-Host "The environment variable for the JRE has been added successfully."
    }

}


function Install-JDK {
    # Définition des paramètres pour l'installation silencieuse
    $installerArgsJDK = "/s INSTALLDIR=`"C:\Program Files\Java\jdk-20`""

    if (Test-Path -Path "C:\Program Files\Java\jdk-20") {
        Write-Host "The JDK package already exist"
        return
    }

    # Téléchargement du fichier d'installation du JRE (remplacez l'URL par celle appropriée)
    $url = "https://download.oracle.com/java/20/latest/jdk-20_windows-x64_bin.exe"
    $outputFileJDK = "$env:TEMP\jdkInstaller.exe"

    Write-Host "Download JDK..."
    Invoke-WebRequest -Uri $url -OutFile $outputFileJDK

    Write-Host "JDK Installation..."
    Start-Process -FilePath $outputFileJDK -ArgumentList $installerArgsJDK -Wait

    Write-Host "Remove Installer file for JDK"
    Remove-Item -Path $outputFileJDK -Force

    # Spécifiez le chemin d'installation du JDK
    $javaHome = "C:\Program Files\Java\jdk-20"
    $existingPath = [System.Environment]::GetEnvironmentVariable("JAVA_HOME")
    if ($existingPath -eq $javaHome) {
        Write-Host "The environment variable for the JRE already exist"
    }
    else {
        [System.Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "Machine")
        Write-Host "The environment variable for the JDK has been added successfully."
    }

 
}
function Install-OPENJDK {
   if (Test-Path -Path "C:\jdk-20.0.1") {
        Write-Host "The OpenJDK package already exist"
        return
    }

    # Téléchargement du fichier d'installation du zip OpenJDK (remplacez l'URL par celle appropriée)
    $url = "https://download.java.net/java/GA/jdk20.0.1/b4887098932d415489976708ad6d1a4b/9/GPL/openjdk-20.0.1_windows-x64_bin.zip"
    $outputFile = "$env:TEMP\Installer.zip"

    Write-Host "Téléchargement du fichier d'installation du OPENJDK..."
    Invoke-WebRequest -Uri $url -OutFile $outputFile

    $CFolder = [Environment]::GetFolderPath("C:\")
    Expand-Archive -Path $outputFile -DestinationPath $CFolder -Force

    # Spécifiez le chemin d'installation du OPENJDK
    $javaHome = "C:\jdk-20.0.1" 
    # Vérifiez si la variable d'environnement existe déjà
    $existingPath = [System.Environment]::GetEnvironmentVariable("JAVA_HOME")
    if ($existingPath -eq $javaHome) {
        Write-Host "La variable d'environnement pour le OPENJDK existe déjà."
    }
    else {
        [System.Environment]::SetEnvironmentVariable("JAVA_HOME", $javaHome, "Machine")
        $oldpath = [System.Environment]::GetEnvironmentVariable("Path", "Machine") 
        $oldpath += ";c:\jdk-20.0.1\bin"
        [System.Environment]::SetEnvironmentVariable("Path", $oldpath, "Machine")
        Write-Host "La variable d'environnement pour le OPENJDK a été ajoutée avec succès."
    }

}

function DownloadTomcat {
    if (Test-Path -Path "C:\tomcat") {
        Write-Host "Tomcat folder already exist"
    }else {
        #Téléchargement du fichier d'installation du zip OpenJDK (remplacez l'URL par celle appropriée)
        $url = "http://www27.cs.kobe-u.ac.jp/~masa-n/mmd/apache-tomcat-9.0.37-windows-x64-mmd.zip"
        $outputFile = "$env:TEMP\tomcat.zip"
        Write-Host "Téléchargement du fichier d'installation du Tomcat..."
        Invoke-WebRequest -Uri $url -OutFile $outputFile
        #Find the C:\ folder
        $CFolder = [Environment]::GetFolderPath("C:\")
        #Unzip in the C:\
        Expand-Archive -Path $outputFile -DestinationPath $CFolder -Force
    }

}

function RunTomcat {
    Write-Host "Run Tomcat..."
    [System.Environment]::SetEnvironmentVariable("CATALINA_HOME", "C:\tomcat", "Machine")
    [System.Environment]::SetEnvironmentVariable("CATALINA_BASE", "C:\tomcat", "Machine")
    cmd.exe -/c "C:\tomcat\bin\startup.bat"
}

function MMDAgentInstall { 
    if (Test-Path -Path "C:\tomcat") {
        Write-Host "MMDAgent already exist"
    }else {
        # Téléchargement du fichier d'installation du zip OpenJDK (remplacez l'URL par celle appropriée)
        $url = "http://www27.cs.kobe-u.ac.jp/~masa-n/mmd/MMDAgent.zip"
        $outputFile = "$env:TEMP\mmdagent.zip"
        Write-Host "Téléchargement du fichier d'installation du MMDAgent..."
        Invoke-WebRequest -Uri $url -OutFile $outputFile
        $DesktopPath = [Environment]::GetFolderPath("Desktop")
        Expand-Archive -Path $outputFile -DestinationPath $DesktopPath -Force
    }
}

function RunMMDAgent {
    C:\Users\kenjiro\Desktop\MMDAgent_win32-1.4\MMDAgent.exe C:\Users\kenjiro\Desktop\MMDAgent_Mei\MMDAgent_Example.mdf
    Start-Sleep -seconds 40
    Invoke-WebRequest -Uri "http://localhost:8080/axis2/services/MMDAgentProxyService/doMotion?motion=bye"
}


Install-JRE
Install-JDK
Install-OPENJDK
DownloadTomcat
MMDAgentInstall
RunTomcat
RunMMDAgent