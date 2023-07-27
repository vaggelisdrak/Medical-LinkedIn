/*=============== EMAIL JS ===============
const contactForm = document.getElementById('contact-form'),
contactMessage = document.getElementById('contact-message'),
contactUser = document.getElementById('contact-user')

var contactparams ={
    from_name: contactForm
}

const sendEmail = (e) =>{
    e.preventDefault()

    // Check if the field has a value
    if(contactUser.value === ''){
        // Add and remove color
        contactMessage.classList.remove('color-green')
        contactMessage.classList.add('color-red')

        // Show message
        contactMessage.textContent = 'You must enter your email ☝'
        
        // Remove message three seconds
        setTimeout(() => {
            contactMessage.textContent = ''
        }, 3000);
    }else{
        // serviceID - templateID - #form - publicKey
        emailjs.sendForm('service_z2utgo5', 'template_46id8mj', '#contact-form', 'yTDZt3BikMFhNx-Dh')
            .then(() => {
                // Show message and add color
                contactMessage.classList.add('color-green')
                contactMessage.textContent = 'You have successfully applied!'
                console.log('success')

                // Remove message after three seconds
                setTimeout(() => {
                    contactMessage.textContent = ''
                }, 3000);

            }, (error) => {
                alert('OOPS! SOMETHING HAS FAILED...', error)
                console.log(error)
            })

        // To clear the input field
        contactUser.value = ''
    }
}
contactForm.addEventListener('submit', sendEmail)*/
(function() {
      emailjs.init("yTDZt3BikMFhNx-Dh"); // Replace with your EmailJS user ID
    })();

function sendEmail() {
    event.preventDefault(); // Prevent form submission
    contactForm = document.getElementById('contact-form')

    // Get form values
    //var name = document.getElementById('name').value;
    var email = document.getElementById('contact-user').value;
    //var message = document.getElementById('message').value;

    // Create email parameters
    var params = {
    from_email: email
    };

    // Send the email
    emailjs.send("service_z2utgo5", "template_46id8mj", params)
    .then(function(response) {
        // Show message and add color
        contactMessage.classList.add('color-green')
        contactMessage.textContent = 'You have successfully applied!'
        console.log('success')

        // Remove message after three seconds
        setTimeout(() => {
            contactMessage.textContent = ''
        }, 3000);
        console.log("Email sent successfully!", response.status, response.text);
        alert("Email sent successfully!");
        document.getElementById('contact-form').reset(); // Reset form
    }, function(error) {
        console.log("Email failed to send.", error);
        alert("Email failed to send. Please try again later.");
    });
}