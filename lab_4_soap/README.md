## Dependências
* Java 8
* Maven (MacOS - brew install maven / Ubuntu - apt-get install mvn)

## Execução
* Execute:
```
$ cd server/
$ ./mvnw spring-boot:run
```

* Em outro terminal execute os slaves:
```
$ cd client_slave
$ ./mvnw spring-boot:run
```

* Em outro terminal execute o master:
```
$ cd client_slave
$ ./mvnw spring-boot:run
```

* Quando perguntar o tamanho das matrizes insira como no exemplo:
```
2 2
```

* Então digite as LINHAS da matriz A como no exemplo:
```
1 2
2 3
```

* E depois as COLUNAS da matriz B como no exemplo, no caso a matriz é:
```
1 2
2 3
```
```
1 2
2 3
```

* Espere e o resultado irá ser printado na tela
