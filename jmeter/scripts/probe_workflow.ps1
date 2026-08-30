# Live verification of Workflow 4 endpoints against kb claims (run once)
$ErrorActionPreference = "Stop"
$base = "http://localhost:3000"

# 1. Auth-heavy: POST /api/login (admin)
$login = Invoke-RestMethod -Uri "$base/api/login" -Method POST -ContentType "application/json" `
    -Body '{"email":"admin@eshop.com","password":"Admin123!"}'
$token = $login.token
Write-Output "LOGIN: OK | token len=$($token.Length) | user=$($login.user.email) role=$($login.user.role)"
$hdr = @{ Authorization = "Bearer $token" }

# 2. Read-heavy part A: GET /api/admin/orders
$orders = Invoke-RestMethod -Uri "$base/api/admin/orders" -Headers $hdr
$count = if ($orders -is [array]) { $orders.Count } else { 1 }
$sample = if ($orders -is [array]) { $orders[0] } else { $orders }
Write-Output "ADMIN ORDERS: OK | count=$count | fields=$($sample.PSObject.Properties.Name -join ',')"

# status distribution + pending ids for the state-transition CSV
if ($orders -is [array]) {
    $orders | Group-Object status | ForEach-Object { Write-Output "  status[$($_.Name)]=$($_.Count)" }
    $pending = ($orders | Where-Object status -eq "pending" | Select-Object -First 8 -ExpandProperty id) -join ","
    Write-Output "  pending ids (first 8): $pending"
}

# 3. Read-heavy part B: GET /api/orders/:id (use first order id)
$oid = if ($orders -is [array]) { $orders[0].id } else { $orders.id }
$detail = Invoke-RestMethod -Uri "$base/api/orders/$oid" -Headers $hdr
Write-Output "ORDER DETAIL: OK | id=$($detail.id) status=$($detail.status)"

# 4. Transactional: PUT /api/admin/orders/:id/status — only touch a pending order,
#    and only if at least 2 pending exist (keep one untouched for the CSV)
$pendingList = if ($orders -is [array]) { @($orders | Where-Object status -eq "pending") } else { @() }
if ($pendingList.Count -ge 2) {
    $probeId = $pendingList[0].id
    $upd = Invoke-RestMethod -Uri "$base/api/admin/orders/$probeId/status" -Method PUT `
        -Headers $hdr -ContentType "application/json" -Body '{"status":"confirmed"}'
    Write-Output "STATUS PUT: OK | order $probeId pending->confirmed"
    # verify the new state persisted
    $re = Invoke-RestMethod -Uri "$base/api/orders/$probeId" -Headers $hdr
    Write-Output "STATUS VERIFY: order $probeId now=$($re.status)"
} else {
    Write-Output "STATUS PUT: SKIPPED - fewer than 2 pending orders (found $($pendingList.Count)). Need DB reset or fresh orders before runs."
}
