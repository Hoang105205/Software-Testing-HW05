# Seed pending orders so Workflow 4 has transactional data (uses test user + real cart/checkout).
# Also (re)writes jmeter/data/orders.csv with the freshly created pending order ids.
param([int]$Count = 150)
$ErrorActionPreference = "Stop"
$base = "http://localhost:3000"

$login = Invoke-RestMethod -Uri "$base/api/login" -Method POST -ContentType "application/json" `
    -Body '{"email":"test@eshop.com","password":"Test1234!"}'
$hdr = @{ Authorization = "Bearer $($login.token)" }
Write-Output "TEST USER LOGIN: OK role=$($login.user.role)"

$products = Invoke-RestMethod -Uri "$base/api/products" -Headers $hdr
$p = if ($products -is [array]) { $products[0] } else { $products }
Write-Output "PRODUCT: id=$($p.id) name=$($p.name) price=$($p.price)"

for ($i = 1; $i -le $Count; $i++) {
    # fresh cart each iteration
    Invoke-RestMethod -Uri "$base/api/cart" -Method POST -Headers $hdr -ContentType "application/json" `
        -Body (@{ id = $p.id; name = $p.name; price = $p.price; quantity = 1 } | ConvertTo-Json) | Out-Null
    $co = Invoke-RestMethod -Uri "$base/api/checkout" -Method POST -Headers $hdr -ContentType "application/json" `
        -Body '{"total_amount": 0, "shipping_address": "123 Le Loi, Q1, TP.HCM"}'
    if ($i % 25 -eq 0 -or $i -eq $Count) { Write-Output "...$i/$Count orders created (last orderId=$($co.orderId))" }
}

# verify with admin token
$admin = Invoke-RestMethod -Uri "$base/api/login" -Method POST -ContentType "application/json" `
    -Body '{"email":"admin@eshop.com","password":"Admin123!"}'
$orders = Invoke-RestMethod -Uri "$base/api/admin/orders" -Headers @{ Authorization = "Bearer $($admin.token)" }
$orders | Group-Object status | ForEach-Object { Write-Output "ADMIN SEES status[$($_.Name)]=$($_.Count)" }

# export pending ids to the workflow-data CSV consumed by JMeter
$csvPath = Join-Path (Split-Path $PSScriptRoot -Parent) "data\orders.csv"
$pendingIds = $orders | Where-Object status -eq "pending" | Select-Object -ExpandProperty id
"order_id" | Set-Content -Path $csvPath -Encoding ascii
$pendingIds | Add-Content -Path $csvPath -Encoding ascii
Write-Output "CSV WRITTEN: $csvPath ($($pendingIds.Count) pending ids)"
