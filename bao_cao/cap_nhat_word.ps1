# Mở báo cáo bằng Microsoft Word, cập nhật mục lục / danh mục hình / danh mục bảng, lưu lại và xuất PDF.
# Chạy (từ thư mục gốc repo): powershell -ExecutionPolicy Bypass -File bao_cao\cap_nhat_word.ps1
#
# Ghi chú (đã thử nghiệm):
#  - Mở CHỈ ĐỌC rồi "Lưu thành" file tạm, sau đó thay file gốc: mở để ghi qua COM có thể treo vì
#    hộp thoại ẩn "file đang được dùng".
#  - Không gọi TableOfContents.UpdatePageNumbers(): lệnh này làm Word treo. Thay bằng Update() hai lượt
#    (lượt 2 để số trang đúng sau khi chính mục lục đã chiếm thêm trang).
#  - Chạy trong Start-Job có giới hạn thời gian để không bao giờ treo vô hạn.
$ErrorActionPreference = "Stop"
$dir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$docx = Join-Path $dir "BaoCao_DiemThi2026_KTXH.docx"
$pdf  = Join-Path $dir "BaoCao_DiemThi2026_KTXH.pdf"
$tmp  = Join-Path $env:TEMP "BaoCao_tmp_$([guid]::NewGuid().ToString('N')).docx"
$log  = Join-Path $env:TEMP "BaoCao_word_log.txt"
Remove-Item $log -ErrorAction SilentlyContinue
Get-ChildItem $dir -Force -Filter '~$*' -ErrorAction SilentlyContinue | Remove-Item -Force

$job = Start-Job -ArgumentList $docx, $pdf, $tmp, $log {
    param($docx, $pdf, $tmp, $log)
    function L($m) { Add-Content -Path $log -Value ("{0:HH:mm:ss} {1}" -f (Get-Date), $m) -Encoding UTF8 }
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false; $w.DisplayAlerts = 0
    $d = $w.Documents.Open($docx, $false, $true, $false); L "mo file"
    foreach ($pass in 1, 2) {
        foreach ($toc in $d.TablesOfContents) { $toc.Update() }
        $d.Repaginate()
        L "cap nhat muc luc luot $pass"
    }
    L "so trang: $($d.ComputeStatistics(2))"
    $d.ExportAsFixedFormat($pdf, 17); L "xuat PDF"
    $d.SaveAs2($tmp, 16); L "luu file"
    $d.Close(0); $w.Quit(); L "xong"
}
$ok = Wait-Job $job -Timeout 240
Stop-Job $job -ErrorAction SilentlyContinue; Remove-Job $job -Force
Get-Content $log -Encoding UTF8
# dọn các tiến trình Word do script tạo ra (chỉ tiến trình tự động hóa, không đụng Word người dùng đang mở)
Get-CimInstance Win32_Process -Filter "Name='WINWORD.EXE'" |
    Where-Object { $_.CommandLine -like '*/Automation*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
if (-not $ok -or -not (Test-Path $tmp)) { throw "Word không hoàn thành trong 240 giây" }
Move-Item -Force $tmp $docx
"Đã cập nhật: $docx"
