# Pusha o DistributedOrderSystem e atualiza o ponteiro no CursoClaude,
# depois pusha o CursoClaude também.
# Uso: .\scripts\update-distributed.ps1

$root = "$PSScriptRoot\.."

# 1. Push do DistributedOrderSystem
Set-Location "$root\DistributedOrderSystem"
git push

# 2. Volta para a raiz e atualiza o ponteiro do submodule
Set-Location $root
git submodule update --remote
git add DistributedOrderSystem
git commit -m "chore: atualiza submodule DistributedOrderSystem"
git push
