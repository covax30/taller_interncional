<?php
  // 1. Configuración de tu correo
  $receiving_email_address = 'karoltalerolopez@gmail.com';

  // 2. Verificar que los datos existan
  if(isset($_POST['name']) && isset($_POST['email'])) {
    
    $name = $_POST['name'];
    $email = $_POST['email'];
    $subject = $_POST['subject'] ?: "Nuevo mensaje de T.I.M Web";
    $message = $_POST['message'];
    $phone = isset($_POST['phone']) ? $_POST['phone'] : 'No proporcionado';

    // 3. Preparar el cuerpo del correo
    $email_body = "Has recibido un nuevo mensaje desde el sitio web de Taller Internacional de Motores.\n\n".
                  "Nombre: $name\n".
                  "Email: $email\n".
                  "Teléfono: $phone\n".
                  "Mensaje:\n$message";

    // 4. Cabeceras (Para que puedas responder directamente al cliente)
    $headers = "From: contacto@tu-dominio.com\r\n"; // Aquí va un correo de tu hosting
    $headers .= "Reply-To: $email\r\n";

    // 5. Enviar
    if(mail($receiving_email_address, $subject, $email_body, $headers)) {
      echo "OK"; // Importante: Las plantillas de BootstrapMade buscan el "OK" para mostrar el mensaje de éxito
    } else {
      echo "Error: No se pudo enviar el mensaje.";
    }
  } else {
    echo "Error: Datos incompletos.";
  }
?>