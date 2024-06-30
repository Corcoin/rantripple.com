<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $to = "bwesson82@gmail.com"; // Your email address where you want to receive messages
    $subject = "Message from Contact Form";
    $name = $_POST['name'];
    $from = $_POST['email'];
    $message = $_POST['message'];

    // Compose the email message
    $email_message = "Name: $name\n";
    $email_message .= "Email: $from\n";
    $email_message .= "Message:\n$message";

    // Additional headers
    $headers = "From: $from\r\n";
    $headers .= "Reply-To: $from\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    // Send email
    if (mail($to, $subject, $email_message, $headers)) {
        echo '<p style="color: green;">Message sent successfully!</p>';
    } else {
        echo '<p style="color: red;">Failed to send message. Please try again later.</p>';
    }
}
?>
