import sqlite3
from pathlib import Path

def create_database(db_path: Path) -> None:
    """
    Create the SQLite database and tables if they do not exist.

    Parameters:
    - db_path (Path): The path to the SQLite database.

    Returns:
    - None
    """
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Execute the SQL commands to create tables with corrected data types
    # and constraints
    cur.executescript(
        """
        -- Create the User table
        CREATE TABLE IF NOT EXISTS User (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            RoleName TEXT NOT NULL,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Password TEXT NOT NULL,
            FailedLoginAttempts INTEGER DEFAULT 0,
            AccountLockTime DATETIME
        );

        -- Create the EmploymentData table
        CREATE TABLE IF NOT EXISTS EmploymentData (
            DataID INTEGER PRIMARY KEY AUTOINCREMENT,
            RegionName TEXT,
            Year INTEGER,
            OccupationType TEXT,
            Gender TEXT,
            EmploymentPercentage FLOAT,
            MarginOfErrorPercentage FLOAT,
            CONSTRAINT unique_employment_data UNIQUE (
                EmploymentPercentage,
                MarginOfErrorPercentage,
                RegionName,
                Gender,
                OccupationType,
                Year
            )
        );

        -- Create the PolicyRecommendation table
        CREATE TABLE IF NOT EXISTS PolicyRecommendation (
            PolicyID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            DisparityID INTEGER NOT NULL,
            PolicyRating INTEGER,
            PolicyDescription TEXT,
            FOREIGN KEY (UserID) REFERENCES User(UserID)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (DisparityID) REFERENCES Disparity(DisparityID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the PolicyFeedback table
        CREATE TABLE IF NOT EXISTS PolicyFeedback (
            FeedbackID INTEGER PRIMARY KEY AUTOINCREMENT,
            PolicyID INTEGER NOT NULL,
            UserID INTEGER NOT NULL,
            FeedbackText TEXT,
            FormattingDetails TEXT,
            FOREIGN KEY (PolicyID) REFERENCES PolicyRecommendation(PolicyID)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (UserID) REFERENCES User(UserID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the SavedConfigurations table
        CREATE TABLE IF NOT EXISTS SavedConfigurations (
            ConfigurationID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ConfigurationName TEXT,
            FOREIGN KEY (UserID) REFERENCES User(UserID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the ConfigurationRegion table
        CREATE TABLE IF NOT EXISTS ConfigurationRegion (
            ConfigurationID INTEGER NOT NULL,
            RegionName TEXT NOT NULL,
            FOREIGN KEY (ConfigurationID) REFERENCES SavedConfigurations(
                ConfigurationID
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (RegionName) REFERENCES EmploymentData(RegionName)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the ConfigurationYear table
        CREATE TABLE IF NOT EXISTS ConfigurationYear (
            ConfigurationID INTEGER NOT NULL,
            Year INTEGER NOT NULL,
            FOREIGN KEY (ConfigurationID) REFERENCES SavedConfigurations(
                ConfigurationID
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (Year) REFERENCES EmploymentData(Year)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the ConfigurationOccupationType table
        CREATE TABLE IF NOT EXISTS ConfigurationOccupationType (
            ConfigurationID INTEGER NOT NULL,
            OccupationType TEXT NOT NULL,
            FOREIGN KEY (ConfigurationID) REFERENCES SavedConfigurations(
                ConfigurationID
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (OccupationType) REFERENCES EmploymentData(
                OccupationType
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the ConfigurationDisparityType table
        CREATE TABLE IF NOT EXISTS ConfigurationDisparityType (
            ConfigurationID INTEGER NOT NULL,
            DisparityType TEXT NOT NULL,
            FOREIGN KEY (ConfigurationID) REFERENCES SavedConfigurations(
                ConfigurationID
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (DisparityType) REFERENCES Disparity(DisparityType)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );

        -- Create the Disparity table
        CREATE TABLE IF NOT EXISTS Disparity (
            DisparityID INTEGER PRIMARY KEY AUTOINCREMENT,
            ConfigurationID INTEGER NOT NULL,
            UserID INTEGER NOT NULL,
            DisparityType TEXT NOT NULL,
            DisparityValue FLOAT NOT NULL,
            FOREIGN KEY (ConfigurationID) REFERENCES SavedConfigurations(
                ConfigurationID
            )
                ON UPDATE CASCADE
                ON DELETE CASCADE,
            FOREIGN KEY (UserID) REFERENCES User(UserID)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Define the path to the SQLite database
    db_path = Path(__file__).parent.joinpath("employment_data.db")

    create_database(db_path)