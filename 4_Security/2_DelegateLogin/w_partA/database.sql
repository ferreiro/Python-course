BEGIN TRANSACTION;
CREATE TABLE Questions (id INTEGER PRIMARY KEY, author VARCHAR(50), title VARCHAR(200), body TEXT, time datetime, tags VARCHAR(200));
INSERT INTO Questions VALUES(1,'pepe','Listas en Python','Me gustaria saber como construir listas en Python','2013-06-14 12:00:42','listas, Python');
INSERT INTO Questions VALUES(2,'ana','Diccionarios','Qué es exactamente un diccionario? Cómo se construyen en Python','2012-03-19 11:54:23','diccionarios, Python, programación');
INSERT INTO Questions VALUES(3,'pepe','Mejor manera de programar','Vim o Emacs?','2015-12-27 16:40:43','Editor, programacion');
CREATE TABLE Replies (
	id INTEGER PRIMARY KEY,
	author VARCHAR(50),
	body TEXT,
	time DATETIME,
	question_id INTEGER,
	FOREIGN KEY (question_id) REFERENCES Questions(id)
);
INSERT INTO Replies VALUES(1,'josefa','Con corchetes!!! Ejemplos de listas son [1,2,3] y [True, False, 3.0]','2015-12-27 15:25:17',1);
INSERT INTO Replies VALUES(2,'josefa','Se me olvidó comentar que también se generan con el constructor list()','2015-12-27 15:26:32',1);
COMMIT;
