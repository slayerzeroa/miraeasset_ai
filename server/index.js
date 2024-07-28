// 실행: 터미널에 node index.js 입력 (server 폴더에서 실행)
const express = require("express");
const fs = require("fs");
const dotenv = require("dotenv");
const mariadb = require("mariadb");
const cors = require("cors");

const app = express();
const path = require("path");

dotenv.config({ path: path.resolve(__dirname, "../.env") });

// Extract database configuration from environment variables
const db_host = process.env.DB_ADDRESS;
const db_user = process.env.DB_USER;
const db_password = process.env.DB_PASSWORD;
const db_database = process.env.DB_NAME;

// Create a MariaDB connection pool
const pool = mariadb.createPool({
  host: db_host,
  user: db_user,
  password: db_password,
  database: db_database,
  connectionLimit: 5,
});

app.use(cors());

// Root URL GET request
app.get("/", (req, res) => {
  res.send("Welcome to the server!!");
});

// Fetch all data
app.get("/customer", (req, res) => {
  const results = [];
  pool
    .getConnection()
    .then((conn) => {
      conn
        .query("SELECT * FROM customer")
        .then((rows) => {
          rows.forEach((row) => {
            results.push(row);
          });
          res.json(results);
        })
        .finally(() => {
          conn.release();
        });
    })
    .catch((err) => {
      console.error("Database connection error:", err);
      res.status(500).json({ error: "Failed to connect to database" });
    });
});

// Fetch all data
app.get("/youtube", (req, res) => {
  const results = [];
  pool
    .getConnection()
    .then((conn) => {
      conn
        .query("SELECT * FROM youtube")
        .then((rows) => {
          rows.forEach((row) => {
            results.push(row);
          });
          res.json(results);
        })
        .finally(() => {
          conn.release();
        });
    })
    .catch((err) => {
      console.error("Database connection error:", err);
      res.status(500).json({ error: "Failed to connect to database" });
    });
});

// Fetch all data
app.get("/pb", (req, res) => {
  const results = [];
  pool
    .getConnection()
    .then((conn) => {
      conn
        .query("SELECT * FROM pb")
        .then((rows) => {
          rows.forEach((row) => {
            results.push(row);
          });
          res.json(results);
        })
        .finally(() => {
          conn.release();
        });
    })
    .catch((err) => {
      console.error("Database connection error:", err);
      res.status(500).json({ error: "Failed to connect to database" });
    });
});

// Fetch all data
app.get("/news", (req, res) => {
  const results = [];
  pool
    .getConnection()
    .then((conn) => {
      conn
        .query("SELECT * FROM news")
        .then((rows) => {
          rows.forEach((row) => {
            results.push(row);
          });
          res.json(results);
        })
        .finally(() => {
          conn.release();
        });
    })
    .catch((err) => {
      console.error("Database connection error:", err);
      res.status(500).json({ error: "Failed to connect to database" });
    });
});

const PORT = 5556;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
