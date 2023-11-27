-- Vehicles Table
CREATE TABLE Vehicles (
    VehicleID INT PRIMARY KEY,
    Make VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    LicensePlate VARCHAR(20),
    Type VARCHAR(50),
    SittingCapacity INT,
    Status VARCHAR(50)
);

-- Users Table (Includes Drivers, Maintenance Personnel, Fueling person, and Admins)
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    Surname VARCHAR(50),
    Password VARCHAR(50),  -- Should be encrypted
    Role VARCHAR(50),      -- Can be 'Driver', 'Maintenance', 'Admin', 'FuelingPerson'
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(Email),
    UNIQUE(PhoneNumber)
);

-- Drivers Table
CREATE TABLE Drivers (
    DriverUserID INT,
    VehicleID INT,
    FOREIGN KEY (DriverUserID) REFERENCES Users(UserID),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID),
    UNIQUE (DriverUserID),
    UNIQUE (VehicleID)
);

-- Admins Table
CREATE TABLE Admins (
    AdminUserID INT,
    FOREIGN KEY (AdminUserID) REFERENCES Users(UserID),
    UNIQUE (AdminUserID)
);

-- Maintenance Table
CREATE TABLE MaintenancePersonnel (
    MaintenanceUserID INT,
    FOREIGN KEY (MaintenanceUserID) REFERENCES Users(UserID),
    UNIQUE (MaintenanceUserID)
);

CREATE TABLE FuelingPerson (
    FuelingPersonUserID INT,
    GasStationName VARCHAR(50),
    FOREIGN KEY (FuelingPersonUserID) REFERENCES Users(UserID),
    UNIQUE (FuelingPersonUserID)
)

-- Maintenance Records Table
CREATE TABLE MaintenanceRecords (
    RecordID INT PRIMARY KEY,
    VehicleID INT,
    MaintenanceUserID INT,
    ServiceType VARCHAR(50),
    Date DATE,
    Cost DECIMAL(10,2),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID),
    FOREIGN KEY (MaintenanceUserID) REFERENCES Users(UserID)
);

-- Fuel Records Table
CREATE TABLE FuelRecords (
    RecordID INT PRIMARY KEY,
    VehicleID INT,
    DriverUserID INT,
    FuelDate DATE,
    AmountOfFuel DECIMAL(10,2),
    TotalCost DECIMAL(10,2),
    GasStationName VARCHAR(50),
    FuelingPersonName VARCHAR(50),
    FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID),
    FOREIGN KEY (DriverUserID) REFERENCES Users(UserID)
);

-- Routes Table
CREATE TABLE Routes (
    RouteID INT PRIMARY KEY,
    DriverUserID INT,
    StartLocation VARCHAR(100),
    EndLocation VARCHAR(100),
    Status VARCHAR(50),
    FOREIGN KEY (DriverUserID) REFERENCES Users(UserID)
);
