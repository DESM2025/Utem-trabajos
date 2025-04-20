create table characters(
ID INT  primary key,
Name varchar(15)  not null,
Primary_rol varchar(15)  not null,
Secundary_rol varchar(15)  not null,
Default_HP INT not null,
Default_ATQ INT not null,
Default_DEF INT not null,
Default_EM INT not null,
WeaponID INT,
ArtifactID INT,
FOREIGN KEY (ArtifactID) REFERENCES Artifact_Set(ID),
FOREIGN KEY (WeaponID) REFERENCES Weapon(ID)
);