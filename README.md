# fortgeschrittene\_Methoden\_der\_Bioinformatik

Um auf das Repo zuzugreifen, könnt ihr entweder ein Personal Access Token erstellen (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) oder einen ssh key für github machen (ich empfehle letzteres).

* Dazu müsst ihr in einer shell eingeben: ssh-keygen -t ed25519 -C "your\_email@example.com"
* Das erzeugt ein Schlüsselpaar in \~/.ssh
* Ladet \~/.ssh/id\_ed25519.pub in github hoch unter Settings → SSH and GPG keys → New SSH key
* Eventuell müsst ihr noch in \~/.ssh/config folgende Zeilen hinzufügen:
Host github.com
User git
HostName github.com
IdentityFile \~/.ssh/NAME\_EURES\_PRIVATE\_KEY\_FILE
IdentitiesOnly yes
* Dann könnt ihr das repo mit git clone git@github.com:Maxisman/fortgeschrittene\_Methoden\_der\_Bioinformatik.git klonen
