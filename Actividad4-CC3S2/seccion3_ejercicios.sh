#!/bin/bash
grep root /etc/passwd
sed 's/dato1/secreto/' datos.txt > nuevo.txt
awk -F: '{print $1}' /etc/passwd | sort | uniq
printf "hola\n" | tr 'a-z' 'A-Z' | tee mayus.txt
find /tmp -mtime -5 -type f
ls /etc | grep conf | sort | tee lista_conf.txt | wc -l
grep -Ei 'error|fail' evidencias/sesion.txt | tee evidencias/hallazgos.txt
