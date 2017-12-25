<?php

//grab named inputs from html then post to #thanks
if (isset($_POST['name'])) {
  $name = strip_tags($_POST['name']);
  $email = strip_tags($_POST['email']);
  $message = strip_tags($_POST['message']);

  require 'mail/PHPMailerAutoload.php';

  $mail = new PHPMailer;

  $mail->isSMTP();                                      // Set mailer to use SMTP
  $mail->Host = 'smtp.mailgun.org';  			// Specify main and backup SMTP servers
  $mail->SMTPAuth = true;                               // Enable SMTP authentication
  $mail->Username = 'auto@cswift.tk';		        // SMTP username
  $mail->Password = rtrim(file_get_contents('../lastfm-api-key.txt'));
  $mail->SMTPSecure = 'tls';                            // Enable TLS encryption, `ssl` also accepted
  $mail->Port = 587;                                    // TCP port to connect to

  $mail->setFrom($email, $name);
  $mail->addAddress('chandler@chandlerswift.com', 'Chandler Swift');     // Add a recipient
  $mail->addReplyTo($email, $name);

  $mail->isHTML(false);                                  // Set email format to non HTML

  $mail->Subject = 'ChandlerSwift.com Contact Form';
  $mail->Body    = "You have received a new message.\n".
"Name: ". strip_tags($_POST['name']). "\n".
"Email: $email\n".  
"Message:\n".
$message;

  if(!$mail->send()) {
      echo 'Message could not be sent.';
      echo 'Mailer Error: ' . $mail->ErrorInfo;
  } else {
      echo 'Message has been sent';
  }
}
