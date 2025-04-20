create table Artifact_Set(
ID INT  primary key,
Name varchar(15)  not null,
BonusID INT,
FOREIGN KEY (BonusID) REFERENCES Artifact_Bonus(ID)
);