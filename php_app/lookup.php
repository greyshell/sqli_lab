<?php
global $dev_env, $db_config;
error_reporting(E_ALL ^ E_WARNING);
require('config.php');

// Set the server name based on the environment
if ($dev_env === 'local') {
    $servername = "127.0.0.1";
} else {
    $servername = "mariadb";
}

// Use database credentials from config.php
$username = $db_config['username'];
$password = $db_config['password'];
$dbname   = $db_config['dbname'];

// Initialize variables for the form
$input_username = "";
$address = "";
$uid = "";
$error = "";
$success = false;
$query = "";
$formSubmitted = false;

// Create connection
$db = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($db->connect_error) {
    $error = "Connection failed: " . $db->connect_error;
}

function lookupAddress($db, $input_username) {
    // Initialize return variables
    $result = array(
        'success' => false,
        'address' => '',
        'uid' => '',
        'error' => '',
        'query' => ''
    );

    // VULNERABLE QUERY - Direct insertion of user input without sanitization
    $query = "SELECT uid, address FROM tbl_php_users WHERE username = '$input_username'";
    $result['query'] = $query;

    try {
        // Execute the query
        $queryResult = $db->query($query);

        if ($queryResult && $queryResult->num_rows > 0) {
            // Fetch data
            $row = $queryResult->fetch_assoc();
            $result['uid'] = $row["uid"];
            $result['address'] = $row["address"];

            $result['success'] = true;
        } else {
            $result['error'] = "No user found or query error";
        }
    } catch (Exception $e) {
        $result['error'] = "Query exception: " . $e->getMessage();
    }

    return $result;
}

// Process form submission
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["username"])) {
    $formSubmitted = true;
    $input_username = $_POST["username"];

    if (!empty($input_username)) {
        $lookupResult = lookupAddress($db, $input_username);

        $success = $lookupResult['success'];
        $address = $lookupResult['address'];
        $uid = $lookupResult['uid'];
        $error = $lookupResult['error'];
        $query = $lookupResult['query'];
    } else {
        $error = "Please enter a username";
    }
}

// Close database connection
$db->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Address Lookup</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: #D8000C;
            background-color: #FFBABA;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .success {
            background-color: #DFF2BF;
            padding: 15px;
            border-radius: 4px;
            margin: 20px 0;
        }
        .query-display {
            font-family: monospace;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            margin: 15px 0;
            overflow-x: auto;
            word-break: break-all;
        }
        .header {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
        .footer {
            margin-top: 20px;
            font-size: 0.8em;
            color: #666;
            text-align: center;
        }
        .result-label {
            font-weight: bold;
            margin-right: 5px;
        }
        .result-value {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h2>User Address Lookup System</h2>
        <p><em>Enter a username to find their address information</em></p>
    </div>

    <?php if (!empty($error)): ?>
        <div class="error"><?php echo htmlspecialchars($error); ?></div>
    <?php endif; ?>

    <!-- Form always displays -->
    <form method="post" action="">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" value="<?php echo htmlspecialchars($input_username); ?>" placeholder="Enter username">
        </div>
        <button type="submit">Look Up Address</button>
    </form>

    <?php if ($formSubmitted && $success): ?>
        <div class="success">
            <h3>User Information Found:</h3>

            <div class="result-item">
                <span class="result-label">Address:</span>
                <div class="result-value"><?php echo htmlspecialchars($address); ?></div>
            </div>

        </div>
    <?php endif; ?>

    <?php if (!empty($query)): ?>
        <div class="query-display">
            <p><strong>Debug Mode - SQL Query:</strong></p>
            <code><?php echo htmlspecialchars($query); ?></code>
        </div>
    <?php endif; ?>

    <div class="footer">
        <p>System Version 1.0 - Internal Use Only</p>
        <!-- Hidden comment for CTF players to find -->
        <!-- TODO: Fix security issues before production. Current implementation vulnerable to SQL injection! -->
    </div>
</div>
</body>
</html>