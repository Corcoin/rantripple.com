USE MyDatabase;

CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    UserName NVARCHAR(50),
    Email NVARCHAR(100),
    BirthDate DATE
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    UserID INT,
    OrderDate DATETIME,
    TotalAmount DECIMAL(10, 2),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
INSERT INTO Users (UserID, UserName, Email, BirthDate)
VALUES (1, 'John Doe', 'john.doe@email.com', '1990-05-15');

INSERT INTO Orders (OrderID, UserID, OrderDate, TotalAmount)
VALUES (101, 1, '2024-06-30 10:00:00', 150.00);

-- Select all users
SELECT * FROM Users;

-- Select orders with user information
SELECT Orders.OrderID, Users.UserName, Orders.OrderDate, Orders.TotalAmount
FROM Orders
INNER JOIN Users ON Orders.UserID = Users.UserID;
-- Update user email
UPDATE Users
SET Email = 'john.doe.new@email.com'
WHERE UserID = 1;
-- Delete order
DELETE FROM Orders
WHERE OrderID = 101;
-- Drop a table
DROP TABLE Orders;

-- Drop the database
DROP DATABASE MyDatabase;
