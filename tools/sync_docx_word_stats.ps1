param(
    [Parameter(Mandatory = $true)]
    [string]$DocxPath
)

$ErrorActionPreference = 'Stop'

function Set-XmlTextByLocalName {
    param(
        [Parameter(Mandatory = $true)] [xml]$Xml,
        [Parameter(Mandatory = $true)] [string]$LocalName,
        [Parameter(Mandatory = $true)] [string]$Value
    )
    $node = $Xml.SelectSingleNode("//*[local-name()='$LocalName']")
    if ($null -ne $node) {
        $node.InnerText = $Value
    }
}

$resolved = (Resolve-Path -LiteralPath $DocxPath).Path

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $null
try {
    $doc = $word.Documents.Open($resolved, $false, $true)
    $doc.Repaginate()
    $stats = [ordered]@{
        Words = [string]$doc.ComputeStatistics(0)
        Lines = [string]$doc.ComputeStatistics(1)
        Pages = [string]$doc.ComputeStatistics(2)
        Characters = [string]$doc.ComputeStatistics(3)
        Paragraphs = [string]$doc.ComputeStatistics(4)
        CharactersWithSpaces = [string]$doc.ComputeStatistics(5)
    }
    $doc.Close($false)
    $doc = $null
}
finally {
    if ($null -ne $doc) {
        $doc.Close($false)
    }
    $word.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$tmpPath = "$resolved.tmp"
if (Test-Path -LiteralPath $tmpPath) {
    Remove-Item -LiteralPath $tmpPath -Force
}

$source = [System.IO.Compression.ZipFile]::Open($resolved, [System.IO.Compression.ZipArchiveMode]::Read)
$dest = [System.IO.Compression.ZipFile]::Open($tmpPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($entry in $source.Entries) {
        $newEntry = $dest.CreateEntry($entry.FullName, [System.IO.Compression.CompressionLevel]::Optimal)
        $inStream = $entry.Open()
        $outStream = $newEntry.Open()
        try {
            if ($entry.FullName -eq 'docProps/app.xml') {
                $reader = New-Object System.IO.StreamReader($inStream, [System.Text.Encoding]::UTF8, $true)
                $xmlText = $reader.ReadToEnd()
                $reader.Close()
                [xml]$xml = $xmlText
                foreach ($key in $stats.Keys) {
                    Set-XmlTextByLocalName -Xml $xml -LocalName $key -Value $stats[$key]
                }
                Set-XmlTextByLocalName -Xml $xml -LocalName 'Application' -Value 'Microsoft Word'
                Set-XmlTextByLocalName -Xml $xml -LocalName 'Company' -Value 'Samsung Electronics'
                $writerSettings = New-Object System.Xml.XmlWriterSettings
                $writerSettings.Encoding = New-Object System.Text.UTF8Encoding($false)
                $writerSettings.Indent = $false
                $writer = [System.Xml.XmlWriter]::Create($outStream, $writerSettings)
                $xml.Save($writer)
                $writer.Close()
            }
            else {
                $inStream.CopyTo($outStream)
            }
        }
        finally {
            $inStream.Dispose()
            $outStream.Dispose()
        }
    }
}
finally {
    $source.Dispose()
    $dest.Dispose()
}

Move-Item -LiteralPath $tmpPath -Destination $resolved -Force

[pscustomobject]$stats | ConvertTo-Json -Compress
