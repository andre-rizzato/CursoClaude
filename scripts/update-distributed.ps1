# Atualiza o submodule DistributedOrderSystem para o commit mais recente
# e registra a mudança no CursoClaude.
# Uso: .\scripts\update-distributed.ps1

Set-Location "$PSScriptRoot\.."

git submodule update --remote
git add DistributedOrderSystem
git commit -m "chore: atualiza submodule DistributedOrderSystem"
