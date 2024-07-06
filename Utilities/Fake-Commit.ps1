Invoke-Expression "git add -A"
Invoke-Expression "git commit -m 'Fake commit'"
Invoke-Expression "git log -n 1"
Invoke-Expression "git reset --soft HEAD~1"