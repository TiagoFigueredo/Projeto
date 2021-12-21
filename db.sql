/*
Seja bem-vindo a base de dados mais básica criada sozinha by me (com ajuda de muitas dúvidas postadas no StackOverflow rs):
Tiago Figueredo Silva
Número Mecanográfico: UP202000612
*/

CREATE DATABASE IF NOT EXISTS WINCOR;
USE WINCOR;

DROP TABLE IF EXISTS OPERADOR, ARTIGO, CLIENTE,
MATRICULA,CLIENTE_MATRICULA,TRANSACAO,ESTOQUE,FATURA,
DEVOLUCAO_ARTIGO,ADICIONA_ARTIGO,TURNO,HAS;



CREATE TABLE OPERADOR(
    NumOP INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(128),
    Salario INT 
);
INSERT INTO OPERADOR(Nome,Salario) VALUES
('Joao',800),
('Maria',700),
('Carlos',800),
('José',800),
('Tiago Figueredo',800),
('Marcelo Carneiro',1200),
('Carlos Silveira',300),
('Ariel',1200),
('Gabriele',800),
('Lucas',800),
('Guilherme',800),
('Nuno',599),
('Ney',800),
('Nilza',900),
('Joe Biden',1000),
('Donald Trump',800);

CREATE TABLE ARTIGO(
    CodBarra INT PRIMARY KEY,
    Nome VARCHAR(128),
    Preco INT NOT NULL 
);
INSERT INTO ARTIGO(CodBarra,Nome,Preco) VALUES
(1021,'Lapis',5),
(1260,'Bola',10),
(1496,'TV',100),
(1721,'Radio',99),
(1913,'Mouse',12),
(1561,'Teclado',16),
(1587,'TV Amarela',100),
(1386,'Freezer',200),
(1980,'Jerrican',1),
(1536,'Relogio',77),
(1745,'Fone',124),
(1013,'Relogio Prata',77),
(1323,'TV Vermelha',100),
(1771,'Lapis',5);

CREATE TABLE CLIENTE(
    Nif INT PRIMARY KEY,
    Nome VARCHAR(128) NOT NULL,
    Cidade VARCHAR(32) NOT NULL,
    Rua VARCHAR(32) NOT NULL,
    CodPostal VARCHAR(32) NOT NULL,
    Complemento VARCHAR(32)
);
INSERT INTO CLIENTE(Nif,Nome,Cidade,Rua,CodPostal,Complemento) VALUES
(1947198566,'Idola Palmer','Pakistan','426-5300 Ut Street','84344',NULL),
(1189251915,'Isabelle Lott','Italy','2161 Adipiscing Rd.','3132 WK','3 ANDAR 1FRT'),
(1882769124,'Jarrod Boyle','Brazil','Ap #790-4879 Fusce Rd.','575681',NULL),
(1858717088,'Kessie Barber','Indonesia','6194 In St.','3276',NULL),
(1002863315,'Hayfa Brewer','Mexico','1307 Vitae Road','51252-48887',NULL),
(1770672376,'Eleanor Rosario','Italy','Ap #286-3563 Sagittis Street','3213',NULL),
(1613765380,'Ross Odom','Austria','647-2984 Aliquam Road','827360','2DIR'),
(1735592232,'Herrod Nixon','Italy','Ap #974-6450 Dictum Av.','32878',NULL),
(1426806485,'Tara Francis','Colombia','324-4618 Congue, St.','10187',NULL),
(1932789593,'Kirk Miranda','Netherlands','P.O. Box 480, 3622 Neque. Rd.','2148',NULL),
(1412447186,'Iris Mcfarland','Australia','Ap #682-5694 Dapibus Rd.','322628','APT 103'),
(1538062849,'Seth Stokes','Poland','8543 Faucibus St.','2625','ANDAR -1'),
(1445612268,'Keelie Phelps','India','Ap #567-7159 Metus. Av.','2885',NULL),
(1070124089,'Elijah Osborne','Belgium','Ap #705-5787 Iaculis Ave','38362',NULL),
(1271359027,'Karly Mitchell','Australia','Ap #114-4475 Lacinia Ave','53732',NULL),
(1412447185,'Iris Mcfarland','Australia','Ap #682-5694 Dapibus Rd.','322628',NULL),
(1538762849,'Seth Stokes','Poland','8543 Faucibus St.','2625',NULL),
(1435612268,'Keelie Phelps','India','Ap #567-7159 Metus. Av.','2885','TERREO'),
(1670124089,'Elijah Osborne','Belgium','Ap #705-5787 Iaculis Ave','38362',NULL),
(1271359017,'Karly Mitchell','Australia','Ap #114-4475 Lacinia Ave','53732',NULL),
(1311109734,'Bethany Steele','Vietnam','508-3357 Diam Ave','27502',NULL),
(1834237709,'Astra Cox','Costa Rica','P.O. Box 550, 3863 Id Ave','40143','2DIR'),
(1462914457,'Elton Rosales','Colombia','Ap #725-8091 Luctus Ave','77664',NULL),
(1630534411,'Kyra Winters','Canada','784-1269 Volutpat. Street','48972',NULL),
(1374638382,'Harding Moran','Italy','Ap #970-7848 Ut, Rd.','818600',NULL),
(1756927929,'Zeph Flores','Pakistan','Ap #646-6457 Vehicula Road','20804',NULL),
(1333540778,'Cole Melton','Brazil','Ap #541-9434 Vestibulum Av.','58658','5 ANDAR'),
(1290189012,'Suki Russo','Belgium','P.O. Box 348, 3236 Et, Av.','757248',NULL),
(1525771570,'Chiquita Giles','Costa Rica','Ap #519-6984 Facilisis Av.','J3K 4P7',NULL),
(1885293504,'Alika Tanner','Belgium','430-5890 Nulla Street','9474',NULL);

CREATE TABLE MATRICULA(
    Codigo VARCHAR(9) PRIMARY KEY,
    Pais VARCHAR(20)
);
INSERT INTO MATRICULA(Codigo,Pais) VALUES
('SL.05.SN','France'),
('DX.56.VL','Costa Rica'),
('ZT.57.YM','Belgium'),
('VS.32.IK','India'),
('RU.71.JV','Netherlands'),
('IT.71.XL','Russian Federation'),
('MI.66.DK','Nigeria'),
('XB.19.QS','New Zealand'),
('HK.95.OJ','New Zealand'),
('HX.80.VA','Turkey'),
('EF.50.PV','Costa Rica'),
('CM.68.PM','India'),
('BV.37.YA','India'),
('IV.07.PX','India'),
('PH.19.ET','Costa Rica');

CREATE TABLE CLIENTE_MATRICULA(
    id_matricula VARCHAR(9),
    id_cliente INT NOT NULL,
    PRIMARY KEY(id_matricula,id_cliente),
    FOREIGN KEY(id_matricula) REFERENCES MATRICULA(Codigo),
    FOREIGN KEY(id_cliente) REFERENCES CLIENTE(Nif)
);
INSERT INTO CLIENTE_MATRICULA(id_matricula,id_cliente) VALUES
('SL.05.SN',1885293504),
('BV.37.YA',1525771570),
('PH.19.ET',1290189012),
('MI.66.DK',1333540778),
('VS.32.IK',1271359017),
('IV.07.PX',1538762849),
('XB.19.QS',1885293504),
('DX.56.VL',1290189012),
('EF.50.PV',1290189012);

CREATE TABLE TRANSACAO(
    NumTransacao INT PRIMARY KEY,
    Hora datetime DEFAULT NOW()
);
INSERT INTO TRANSACAO (NumTransacao) VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8);

CREATE TABLE ESTOQUE(
    CodBarra INT PRIMARY KEY,
    FOREIGN KEY(CodBarra) REFERENCES ARTIGO(CodBarra),
    Quantidade INT,
    PrecoTotal INT DEFAULT NULL
); 
INSERT INTO ESTOQUE(CodBarra,Quantidade) VALUES
(1021,5),
(1260,1),
(1496,10),
(1721,NULL),
(1913,2),
(1561,16),
(1587,3),
(1386,7),
(1980,9),
(1536,NULL),
(1745,12),
(1013,7),
(1323,1),
(1771,5);
UPDATE ESTOQUE t1
INNER JOIN (SELECT a.CodBarra,a.Preco*e.Quantidade as PrecoTotal FROM ARTIGO a INNER JOIN ESTOQUE e ON a.CodBarra = e.CodBarra) t2 ON t1.CodBarra = t2.CodBarra
SET t1.PrecoTotal = t2.PrecoTotal;
/* Para conseguirmos colocar o PrecoTotal no estoque. 
   O Select de dentro vai criar uma tabela t2 associando o codBarra com o preto total
   Depois passamos para a tabela ESTOQUE todas as referencias iguais (usamos o CodBarra para essa comparacao, por isso quando crio a t2 uso o a.CodBarra)   
*/

CREATE TABLE FATURA(
    Nif INT NOT NULL,
    NumTransacao INT NOT NULL,
    PRIMARY KEY(Nif,NumTransacao),
    FOREIGN KEY(Nif) REFERENCES CLIENTE(Nif),
    FOREIGN KEY(NumTransacao) REFERENCES TRANSACAO(NumTransacao)
);
INSERT INTO FATURA(Nif,NumTransacao) VALUES
(1613765380,1),
(1070124089,2),
(1630534411,3),
(1525771570,4),
(1947198566,5),
(1462914457,6),
(1189251915,7);

CREATE TABLE ADICIONA_ARTIGO(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    CodBarra INT NOT NULL,
    NumTransacao INT NOT NULL,
    FOREIGN KEY(CodBarra) REFERENCES ARTIGO(CodBarra),
    FOREIGN KEY(NumTransacao) REFERENCES TRANSACAO(NumTransacao),
    Quantidade INT NOT NULL DEFAULT 1
);
INSERT INTO ADICIONA_ARTIGO(CodBarra,NumTransacao,Quantidade) VALUES
(1021,1,1),
(1260,1,1),
(1013,2,1),
(1536,3,1),
(1913,4,1),
(1021,4,3),
(1021,4,2),
(1260,4,1),
(1386,5,10),
(1323,6,1),
(1980,6,6),
(1913,6,1),
(1021,7,5);

CREATE TABLE DEVOLUCAO_ARTIGO(
    ID INT PRIMARY KEY NOT NULL,
    NumTransacao INT NOT NULL,
    FOREIGN KEY(NumTransacao) REFERENCES TRANSACAO(NumTransacao)
);
  INSERT INTO DEVOLUCAO_ARTIGO(ID,NumTransacao) VALUES
(1,1),
(10,6),
(13,7);

DELETE FROM ADICIONA_ARTIGO WHERE ID IN (SELECT ID FROM DEVOLUCAO_ARTIGO);
/* Apagar todos os artigos devolvidos que foram adicionados a uma transação*/
CREATE TABLE TURNO(
    NTurno INT NOT NULL,
    NumTransacao INT NOT NULL,
    NumOP INT NOT NULL,
    PRIMARY KEY(NTurno,NumOP,NumTransacao),
    FOREIGN KEY(NumTransacao) REFERENCES TRANSACAO(NumTransacao),
    FOREIGN KEY(NumOP) REFERENCES OPERADOR(NumOP),
    Inicio DATETIME DEFAULT NOW()
);
INSERT INTO TURNO(NTurno,NumTransacao,NumOP) VALUES
(1,2,7),
(1,3,7),/* Perceba que no mesmo turno operador 7 realizou 2 transações*/
(2,1,3),/* O operador 3 só fez uma venda ! */
(3,7,5),
(3,6,5),
(4,4,7),/* O operador 7, voltou ao trabalho, mas em outro turno */
(4,5,7);
